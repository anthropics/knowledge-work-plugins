# Raw Recording

Access raw audio and video data from Zoom meetings and sessions for custom processing.

## Overview

Raw recording allows you to capture unprocessed audio and video frames directly from the SDK, enabling custom recording solutions, AI processing, and media pipelines.

## Platform Support

| Platform | Support Level | SDK |
|----------|---------------|-----|
| **Linux** | Primary | Meeting SDK, Video SDK |
| **Windows** | Primary | Meeting SDK, Video SDK |
| **macOS** | Primary | Meeting SDK, Video SDK |
| **iOS** | Light | Meeting SDK, Video SDK |
| **Android** | Light | Meeting SDK, Video SDK |
| **Web** | No native support | Use 3rd party browser recording; must call recording API for compliance notification |

## Desktop Platforms (Primary)

### Linux

```cpp
// Subscribe to raw audio
class AudioRawDataDelegate : public IZoomSDKAudioRawDataDelegate {
public:
    void onMixedAudioRawDataReceived(AudioRawData *data) override {
        // Format: 16-bit PCM, 16kHz or 32kHz, mono
        std::ofstream file("meeting.pcm", std::ios::binary | std::ios::app);
        file.write(data->GetBuffer(), data->GetBufferLen());
    }
};

// Subscribe to raw video
class VideoRawDataDelegate : public IZoomSDKRendererDelegate {
public:
    void onRawDataFrameReceived(YUVRawDataI420 *data) override {
        // Format: I420 (YUV 4:2:0) - contiguous planar data
        int width = data->GetStreamWidth();
        int height = data->GetStreamHeight();
        
        // Write raw YUV to file (can convert with ffmpeg later)
        yuvFile.write(data->GetYBuffer(), width * height);
        yuvFile.write(data->GetUBuffer(), (width/2) * (height/2));
        yuvFile.write(data->GetVBuffer(), (width/2) * (height/2));
    }
};

// Enable raw recording
auto recCtl = m_meetingService->GetMeetingRecordingController();
recCtl->StartRawRecording();

// Subscribe
GetAudioRawdataHelper()->subscribe(new AudioRawDataDelegate());
GetRawdataRendererHelper()->subscribe(userId, RAW_DATA_TYPE_VIDEO, new VideoRawDataDelegate());
```

**Playing/Converting Raw Files:**
```bash
# Play raw YUV video (adjust dimensions to match output)
ffplay -video_size 640x360 -pixel_format yuv420p -f rawvideo video.yuv

# Convert YUV to MP4
ffmpeg -video_size 640x360 -pixel_format yuv420p -f rawvideo -i video.yuv -c:v libx264 output.mp4

# Play raw PCM audio
ffplay -f s16le -ar 32000 -ac 1 audio.pcm

# Combine video + audio
ffmpeg -video_size 640x360 -pixel_format yuv420p -f rawvideo -i video.yuv \
       -f s16le -ar 32000 -ac 1 -i audio.pcm \
       -c:v libx264 -c:a aac -shortest output.mp4
```

### Windows

```cpp
// Same API as Linux
// Subscribe to raw data after joining meeting
auto* pRawDataHelper = GetAudioRawdataHelper();
pRawDataHelper->subscribe(new AudioRawDataDelegate());

auto* pVideoHelper = GetRawdataRendererHelper();
pVideoHelper->setRawDataResolution(ZoomSDKResolution_720P);
pVideoHelper->subscribe(userId, RAW_DATA_TYPE_VIDEO, new VideoRawDataDelegate());
```

### macOS

```swift
// Get raw data controller
let rawDataCtrl = ZoomSDK.shared().getRawDataController()

// Subscribe to audio
rawDataCtrl?.subscribeAudioRawData { audioData in
    // Process PCM audio
    let buffer = audioData.getBuffer()
    let length = audioData.getBufferLen()
}

// Subscribe to video
rawDataCtrl?.subscribeVideoRawData(forUser: userId) { videoData in
    // Process YUV frames
    let width = videoData.getStreamWidth()
    let height = videoData.getStreamHeight()
}
```

## Mobile Platforms (Light)

### iOS

Raw data access on iOS is more limited than desktop:

```swift
// Video raw data via ZoomVideoSDKVideoCanvas
let canvas = ZoomVideoSDKVideoCanvas()
canvas.delegate = self

// Implement delegate
func onRawDataFrameReceived(_ pixelBuffer: CVPixelBuffer) {
    // Process video frame
    // Note: Performance-intensive on mobile
}
```

**Limitations:**
- Higher battery consumption
- May impact app performance
- Not recommended for long recordings

### Android

```kotlin
// Video raw data via ZoomVideoSDKVideoCanvas
val canvas = ZoomVideoSDKVideoCanvas(context)
canvas.setDelegate(object : ZoomVideoSDKRawDataPipeDelegate {
    override fun onRawDataFrameReceived(rawData: ZoomVideoSDKVideoRawData) {
        // Process YUV frame
        // Note: Performance-intensive on mobile
    }
})
```

**Limitations:**
- Same as iOS - battery and performance concerns
- Consider cloud recording instead for mobile apps

## Web Platform

There is no native SDK support for raw recording on Web. For browser-based recording:

1. Use 3rd party browser recording solutions
2. **Important**: Call the recording API to trigger the "This meeting is being recorded" notification for compliance

## Common Use Cases

- Meeting bots for transcription
- Custom recording pipelines
- AI/ML processing (sentiment analysis, summarization)
- Media archival solutions

## Detailed Platform Guides

- **[Video SDK Linux Guide](../../video-sdk/linux/linux.md)** - Complete C++ implementation for headless bots
- **[Meeting SDK Linux Guide](../../meeting-sdk/linux/linux.md)** - Meeting SDK raw data capture

## Resources

- **Meeting SDK docs**: https://developers.zoom.us/docs/meeting-sdk/
- **Video SDK docs**: https://developers.zoom.us/docs/video-sdk/
