# Unity Session Join Pattern

```csharp
public async Task JoinVideoSession(string sessionName, string userName)
{
    var token = await tokenClient.FetchVideoToken(sessionName, userName);

    zoomSdk.Initialize(initParams);
    zoomSdk.OnSessionJoin += HandleSessionJoin;

    zoomSdk.JoinSession(sessionName, userName, token);

    zoomSdk.GetAudioHelper().StartAudio();
    zoomSdk.GetVideoHelper().StartVideo();
}
```

## Notes

- Bind/unbind Unity event handlers during scene lifecycle.
- Guard against stale handlers when reloading scenes.
