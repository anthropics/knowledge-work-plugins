# SDK Wrappers and GUI Integration

Building custom language wrappers and GUI applications with Zoom Meeting/Video SDKs.

## Overview

The native Zoom SDKs are written in C++. To use them from other languages or with GUI frameworks, you need wrappers or direct integration.

| Platform | Wrapper/Integration | Use Case |
|----------|---------------------|----------|
| Windows | C++/CLI → C# | WPF, WinForms, .NET apps |
| Linux | Native C++ | Qt, GTK desktop apps |
| Linux | Direct C++ | Headless bots, server-side |

## Windows: C++/CLI Wrapper for C#/.NET

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  C# Application Layer (WPF / WinForms / .NET)              │
│  - UI controls, business logic                              │
│  - Uses managed ZOOM_SDK_DOTNET_WRAP namespace             │
└─────────────────────────────────────────────────────────────┘
                          ↕ Managed/Unmanaged Boundary
┌─────────────────────────────────────────────────────────────┐
│  C++/CLI Wrapper Layer (zoom_sdk_dotnet_wrap.dll)          │
│  - Managed ref classes with ^ handles                       │
│  - Native C++ classes calling SDK                           │
│  - Event bridging: std::bind → C# delegates                │
└─────────────────────────────────────────────────────────────┘
                          ↕ Native C++ Interface
┌─────────────────────────────────────────────────────────────┐
│  Native Zoom SDK (videosdk.dll / sdk.dll)                  │
│  - Loaded dynamically via sdk_dll_path                      │
└─────────────────────────────────────────────────────────────┘
```

### Why C++/CLI (Not P/Invoke)?

| Aspect | P/Invoke | C++/CLI |
|--------|----------|---------|
| Complex C++ objects | ❌ Difficult | ✅ Native support |
| Callbacks/delegates | ❌ Manual marshaling | ✅ Automatic bridging |
| Object lifetime | ❌ Manual GC pinning | ✅ Automatic handling |
| std::function patterns | ❌ Not supported | ✅ Works with std::bind |

### Project Structure

```
videosdk-windows-dotnet-quickstart/
├── ZoomVideoSDK.CSharp.sln          # Visual Studio solution
├── config.json                       # Runtime configuration
├── sdk/                              # Zoom SDK files
│   └── x64/
│       ├── h/                        # C++ headers
│       ├── lib/                      # Static libraries (.lib)
│       └── bin/                      # Runtime DLLs (.dll)
├── ZoomVideoSDK.Wrapper/             # C++/CLI wrapper project
│   ├── ZoomVideoSDK.Wrapper.vcxproj  # CLRSupport=true
│   ├── ZoomSDKManager.h              # Managed wrapper class
│   └── ZoomSDKManager.cpp
├── ZoomVideoSDK.WinForms/            # C# WinForms app
│   ├── MainForm.cs
│   └── ZoomSDKInterop.cs
└── ZoomVideoSDK.WPF/                 # C# WPF app
    ├── MainWindow.xaml
    └── MainWindow.xaml.cs
```

### C++/CLI Wrapper Implementation

**Project Configuration (.vcxproj)**:
```xml
<PropertyGroup>
  <ConfigurationType>DynamicLibrary</ConfigurationType>
  <CLRSupport>true</CLRSupport>  <!-- Enable C++/CLI -->
  <CharacterSet>Unicode</CharacterSet>
</PropertyGroup>
```

**Wrapper Class (C++/CLI)**:
```cpp
// ZoomSDKManager.h
#pragma once

using namespace System;

namespace ZoomVideoSDK {
    namespace Wrapper {
        
        // Managed delegate (callable from C#)
        public delegate void SessionStatusChangedHandler(String^ status, String^ message);
        
        // Managed wrapper class
        public ref class ZoomSDKManager sealed {
        public:
            static property ZoomSDKManager^ Instance {
                ZoomSDKManager^ get() { return m_Instance; }
            }
            
            bool Initialize(String^ sdkDllPath);
            bool JoinSession(String^ sessionName, String^ token, String^ userName);
            void LeaveSession();
            
            // Events exposed to C#
            event SessionStatusChangedHandler^ SessionStatusChanged;
            
        private:
            static ZoomSDKManager^ m_Instance = gcnew ZoomSDKManager;
            
            // Bridge to invoke C# events from native callbacks
            void OnSessionStatusChanged(String^ status, String^ message) {
                SessionStatusChanged(status, message);
            }
        };
    }
}
```

**Callback Bridging Pattern**:
```cpp
// Native C++ handler class (unmanaged)
class NativeEventHandler {
public:
    static NativeEventHandler& GetInst() {
        static NativeEventHandler inst;
        return inst;
    }
    
    void onSessionJoin() {
        // Forward to managed wrapper using QMetaObject pattern
        ZoomSDKManager::Instance->OnSessionStatusChanged("Joined", "Session joined successfully");
    }
};

// Binding native callbacks to handler
void ZoomSDKManager::BindEvents() {
    // Use std::bind to connect native callbacks
    ZOOM_SDK::GetSessionService().m_cbonSessionJoin = 
        std::bind(&NativeEventHandler::onSessionJoin, &NativeEventHandler::GetInst());
}
```

### C# Application Usage

**WPF Example**:
```csharp
using ZoomVideoSDK.Wrapper;

public partial class MainWindow : Window
{
    private ZoomSDKManager _sdk;
    
    public MainWindow()
    {
        InitializeComponent();
        
        _sdk = ZoomSDKManager.Instance;
        _sdk.SessionStatusChanged += OnSessionStatusChanged;
    }
    
    private void JoinButton_Click(object sender, RoutedEventArgs e)
    {
        bool initialized = _sdk.Initialize(@".\sdk\x64\bin");
        if (initialized)
        {
            _sdk.JoinSession(
                sessionName: SessionNameTextBox.Text,
                token: JwtTokenTextBox.Text,
                userName: UserNameTextBox.Text
            );
        }
    }
    
    private void OnSessionStatusChanged(string status, string message)
    {
        // Must invoke on UI thread
        Dispatcher.Invoke(() => {
            StatusLabel.Content = $"{status}: {message}";
        });
    }
}
```

**WinForms Example**:
```csharp
public partial class MainForm : Form
{
    private ZoomSDKManager _sdk;
    
    private void OnSessionStatusChanged(string status, string message)
    {
        // Must invoke on UI thread
        this.Invoke((MethodInvoker)delegate {
            statusLabel.Text = $"{status}: {message}";
        });
    }
}
```

### Build Configuration

**DLL Dependencies**:
```
C# App (managed)
    ↓ references
ZoomVideoSDK.Wrapper.dll (C++/CLI mixed-mode)
    ↓ loads dynamically at runtime
videosdk.dll + dependencies (native)
```

**Post-Build Events**:
```batch
REM Copy SDK DLLs to output directory
xcopy /Y "$(SolutionDir)sdk\x64\bin\*.dll" "$(OutDir)"
```

---

## Linux: Qt GUI Integration

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Qt Application (C++)                                       │
│  - Qt Widgets / QML                                         │
│  - Signals/Slots for event handling                         │
└─────────────────────────────────────────────────────────────┘
                          ↕ Direct C++ calls
┌─────────────────────────────────────────────────────────────┐
│  Native Zoom SDK (libvideosdk.so)                          │
│  - Video/Audio processing                                   │
│  - Network communication                                    │
└─────────────────────────────────────────────────────────────┘
```

### Project Structure

```
videosdk-linux-qt-quickstart/
├── README.md
├── run_qt_demo.sh                    # Run script
├── src/
│   ├── CMakeLists.txt                # Qt6/Qt5 build config
│   ├── config.json                   # Session config
│   ├── bin/                          # Build output
│   │   └── VideoSDKQtDemo
│   ├── include/                      # SDK headers
│   ├── lib/                          # SDK libraries
│   └── Source Files:
│       ├── zoom_v-sdk_linux_bot_qt.cpp   # Main entry
│       ├── QtMainWindow.h/cpp            # Main window
│       ├── QtVideoWidget.h/cpp           # Video display
│       ├── QtVideoRenderer.h/cpp         # YUV→RGB rendering
│       ├── QtPreviewVideoHandler.h/cpp   # Self video
│       └── QtRemoteVideoHandler.h/cpp    # Remote video
```

### Qt Video Rendering

```cpp
// QtVideoWidget.h
class QtVideoWidget : public QWidget {
    Q_OBJECT
    
public:
    explicit QtVideoWidget(QWidget* parent = nullptr);
    void updateFrame(const QImage& frame);
    
protected:
    void paintEvent(QPaintEvent* event) override;
    
private:
    QImage m_currentFrame;
    QMutex m_mutex;
};

// QtVideoWidget.cpp
void QtVideoWidget::updateFrame(const QImage& frame) {
    QMutexLocker lock(&m_mutex);
    m_currentFrame = frame;
    update();  // Trigger repaint
}

void QtVideoWidget::paintEvent(QPaintEvent* event) {
    QPainter painter(this);
    QMutexLocker lock(&m_mutex);
    
    if (!m_currentFrame.isNull()) {
        // Scale to fit with aspect ratio
        QImage scaled = m_currentFrame.scaled(
            size(), Qt::KeepAspectRatio, Qt::SmoothTransformation);
        
        // Center the image
        int x = (width() - scaled.width()) / 2;
        int y = (height() - scaled.height()) / 2;
        painter.drawImage(x, y, scaled);
    }
}
```

### YUV to RGB Conversion

```cpp
// QtVideoRenderer.cpp
QImage convertYUV420ToRGB(const unsigned char* yuvData, int width, int height) {
    QImage image(width, height, QImage::Format_RGB888);
    
    const unsigned char* yPlane = yuvData;
    const unsigned char* uPlane = yuvData + width * height;
    const unsigned char* vPlane = uPlane + (width * height / 4);
    
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            int yIndex = y * width + x;
            int uvIndex = (y / 2) * (width / 2) + (x / 2);
            
            int Y = yPlane[yIndex];
            int U = uPlane[uvIndex] - 128;
            int V = vPlane[uvIndex] - 128;
            
            // ITU-R BT.601 conversion
            int R = qBound(0, (int)(Y + 1.402 * V), 255);
            int G = qBound(0, (int)(Y - 0.344 * U - 0.714 * V), 255);
            int B = qBound(0, (int)(Y + 1.772 * U), 255);
            
            image.setPixel(x, y, qRgb(R, G, B));
        }
    }
    
    return image;
}
```

### Qt Event Threading

```cpp
// Invoke SDK callbacks on Qt main thread
class VideoCallback : public IZoomVideoSDKRawDataPipeDelegate {
public:
    void onRawDataFrameReceived(YUVRawDataI420* data) override {
        QImage frame = convertYUV420ToRGB(data->getBuffer(), 
                                           data->getWidth(), 
                                           data->getHeight());
        
        // Thread-safe UI update using Qt's event system
        QMetaObject::invokeMethod(m_videoWidget, [this, frame]() {
            m_videoWidget->updateFrame(frame);
        }, Qt::QueuedConnection);
    }
    
private:
    QtVideoWidget* m_videoWidget;
};
```

### Build with CMake

```cmake
cmake_minimum_required(VERSION 3.14)
project(VideoSDKQtDemo)

set(CMAKE_CXX_STANDARD 17)

# Find Qt
find_package(Qt6 COMPONENTS Core Widgets REQUIRED)
# Or: find_package(Qt5 COMPONENTS Core Widgets REQUIRED)

# Find ALSA for audio
find_package(ALSA REQUIRED)

# Source files
set(SOURCES
    zoom_v-sdk_linux_bot_qt.cpp
    QtMainWindow.cpp
    QtVideoWidget.cpp
    QtVideoRenderer.cpp
)

add_executable(VideoSDKQtDemo ${SOURCES})

target_link_libraries(VideoSDKQtDemo
    Qt6::Core Qt6::Widgets
    ${ALSA_LIBRARIES}
    ${CMAKE_SOURCE_DIR}/lib/libvideosdk.so
)
```

---

## Linux: GTK GUI Integration

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  GTKmm Application (C++)                                    │
│  - GTK Widgets (Gtk::Window, Gtk::Box, etc.)               │
│  - Glib signals for event handling                          │
│  - SDL2 for video rendering                                 │
└─────────────────────────────────────────────────────────────┘
                          ↕ Direct C++ calls
┌─────────────────────────────────────────────────────────────┐
│  Native Zoom SDK (libvideosdk.so)                          │
└─────────────────────────────────────────────────────────────┘
```

### Project Structure

```
videosdk-linux-gtk-quickstart/
├── README.md
├── src/
│   ├── CMakeLists.txt
│   ├── config.json
│   ├── bin/
│   │   └── SkeletonDemo
│   └── Source Files:
│       ├── zoom_v-sdk_linux_bot.cpp     # Main entry + GTK UI
│       ├── VideoRenderer.h/cpp          # SDL2 video rendering
│       ├── VideoDisplayBridge.h/cpp     # SDK→Renderer bridge
│       ├── PreviewVideoHandler.h/cpp    # Self video
│       └── RemoteVideoRawDataHandler.h/cpp  # Remote video
```

### GTK Video Rendering (SDL2)

```cpp
// VideoRenderer.h
class VideoRenderer {
public:
    VideoRenderer(Gtk::Widget* container);
    ~VideoRenderer();
    
    void renderFrame(const unsigned char* yuvData, int width, int height);
    
private:
    SDL_Window* m_window;
    SDL_Renderer* m_renderer;
    SDL_Texture* m_texture;
};

// VideoRenderer.cpp
void VideoRenderer::renderFrame(const unsigned char* yuvData, int width, int height) {
    // Update YUV texture directly (SDL handles conversion)
    SDL_UpdateYUVTexture(m_texture, nullptr,
        yuvData,                           // Y plane
        width,                             // Y pitch
        yuvData + width * height,          // U plane
        width / 2,                         // U pitch
        yuvData + width * height * 5/4,    // V plane
        width / 2);                        // V pitch
    
    SDL_RenderClear(m_renderer);
    SDL_RenderCopy(m_renderer, m_texture, nullptr, nullptr);
    SDL_RenderPresent(m_renderer);
}
```

### GTK Main Window

```cpp
// zoom_v-sdk_linux_bot.cpp
class MainWindow : public Gtk::Window {
public:
    MainWindow() {
        set_title("Zoom Video SDK Demo");
        set_default_size(1200, 800);
        
        // Create layout
        auto mainBox = Gtk::make_managed<Gtk::Box>(Gtk::ORIENTATION_VERTICAL);
        
        // Device selection
        m_cameraCombo = Gtk::make_managed<Gtk::ComboBoxText>();
        m_micCombo = Gtk::make_managed<Gtk::ComboBoxText>();
        m_speakerCombo = Gtk::make_managed<Gtk::ComboBoxText>();
        
        // Control buttons
        m_joinButton = Gtk::make_managed<Gtk::Button>("Join Session");
        m_leaveButton = Gtk::make_managed<Gtk::Button>("Leave Session");
        
        // Video areas (SDL embedded)
        m_selfVideoArea = Gtk::make_managed<Gtk::DrawingArea>();
        m_remoteVideoArea = Gtk::make_managed<Gtk::DrawingArea>();
        
        // Connect signals
        m_joinButton->signal_clicked().connect(
            sigc::mem_fun(*this, &MainWindow::on_join_clicked));
        
        add(*mainBox);
        show_all_children();
    }
    
private:
    void on_join_clicked() {
        // Initialize SDK and join session
        ZoomVideoSDKInitParams params;
        params.domain = "https://zoom.us";
        m_sdk->initialize(params);
        
        ZoomVideoSDKSessionContext context;
        context.sessionName = m_sessionEntry->get_text().c_str();
        context.token = m_tokenEntry->get_text().c_str();
        m_sdk->joinSession(context);
    }
};
```

### Build Dependencies

```bash
# Ubuntu/Debian
sudo apt install build-essential cmake
sudo apt install libgtkmm-3.0-dev libsdl2-dev
sudo apt install libasound2-dev libcurl4-openssl-dev
```

```cmake
# CMakeLists.txt
find_package(PkgConfig REQUIRED)
pkg_check_modules(GTKMM REQUIRED gtkmm-3.0)
pkg_check_modules(SDL2 REQUIRED sdl2)
pkg_check_modules(ALSA REQUIRED alsa)

target_link_libraries(SkeletonDemo
    ${GTKMM_LIBRARIES}
    ${SDL2_LIBRARIES}
    ${ALSA_LIBRARIES}
    ${CMAKE_SOURCE_DIR}/lib/libvideosdk.so
)
```

---

## Comparison: Qt vs GTK

| Aspect | Qt | GTK |
|--------|----|----|
| Language | C++ (native) | C++ (GTKmm wrapper) |
| Video Rendering | QPainter / QImage | SDL2 / Cairo |
| Threading | Signals/Slots + QMetaObject | Glib main loop + idle callbacks |
| Build System | CMake / qmake | CMake |
| Look & Feel | Platform-native | GTK theme |
| Learning Curve | Moderate | Moderate |

## Resources

### Sample Repositories

- **Windows C#**: [videosdk-windows-dotnet-desktop-framework-quickstart](https://github.com/tanchunsiong/videosdk-windows-dotnet-desktop-framework-quickstart)
- **Linux Qt**: [videosdk-linux-qt-quickstart](https://github.com/tanchunsiong/videosdk-linux-qt-quickstart)
- **Linux GTK**: [videosdk-linux-gtk-quickstart](https://github.com/tanchunsiong/videosdk-linux-gtk-quickstart)

### Official Documentation

- [Windows Meeting SDK](https://developers.zoom.us/docs/meeting-sdk/windows/)
- [Windows Video SDK](https://developers.zoom.us/docs/video-sdk/windows/)
- [Linux Video SDK](https://developers.zoom.us/docs/video-sdk/linux/)
