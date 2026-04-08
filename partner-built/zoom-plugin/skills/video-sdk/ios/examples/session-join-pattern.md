# iOS Session Join Pattern

```swift
func joinSession(sessionName: String, userName: String) async throws {
  let token = try await tokenClient.fetchVideoToken(sessionName: sessionName, userName: userName)

  try videoSDK.initialize(with: initParams)
  videoSDK.delegate = self

  try videoSDK.joinSession(
    sessionName: sessionName,
    userName: userName,
    token: token
  )

  try videoSDK.audioHelper.startAudio()
  try videoSDK.videoHelper.startVideo()
}
```

## Notes

- Trigger media start after successful join callback when possible.
- Keep token expiry handling (refresh/rejoin) explicit.
