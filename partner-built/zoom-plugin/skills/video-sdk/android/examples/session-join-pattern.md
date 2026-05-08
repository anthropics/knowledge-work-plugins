# Android Session Join Pattern

```kotlin
suspend fun joinVideoSession(sessionName: String, userName: String) {
  val token = tokenApi.getVideoSdkToken(sessionName, userName)

  val initResult = videoSdk.initialize(initParams)
  check(initResult.isSuccess) { "SDK init failed" }

  videoSdk.addListener(sessionListener)

  val joinResult = videoSdk.joinSession(
    sessionName = sessionName,
    userName = userName,
    token = token
  )
  check(joinResult.isSuccess) { "Join failed" }

  videoHelper.startVideo()
  audioHelper.startAudio()
}
```

## Notes

- Start local media after join success.
- Keep camera/mic permissions and denial handling explicit.
