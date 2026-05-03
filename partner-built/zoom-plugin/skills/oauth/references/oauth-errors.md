# OAuth Error Messages

> Source: https://developers.zoom.us/docs/integrations/oauth/

This table lists OAuth error messages, possible causes, and recommended mitigations.

| Error Code | Error Message | Description | Guidance |
|------------|---------------|-------------|----------|
| 4700 | *(empty)* | The cause can vary depending on the API. | Use the tracking ID to find additional information in the logs and contact Zoom for further assistance. |
| 4700 | Token cannot be empty. | The token is missing. | Verify that the token is present in the header and that its value is correct. |
| 4700 | Exception message | This is a catch all for unexpected errors. | Report the error code to Zoom for further assistance. |
| 4702, 4704 | Invalid client. / Invalid client secret. | Client ID does not match authenticated client. The client ID or client secret isn't entered correctly, or the related app doesn't exist. | Verify that the client ID and client secret are entered in the header correctly. If they are correct then contact Zoom for further assistance. |
| 4705 | Grant type is not supported from token endpoint. | The grant type is not supported by the token endpoint. | Use a valid grant type against `https://zoom.us/oauth/token` (for example `authorization_code`, `refresh_token`, `account_credentials`, `client_credentials`, `urn:ietf:params:oauth:grant-type:device_code`). |
| 4706 | Client ID or client secret is missing. | The client ID and client secret are missing either in the header or in the request parameter. | Verify that the client ID and client secret are entered correctly in the header or request parameter. |
| 4706 | Missing grant type. | OAuth requires the grant type, and it is missing in the header. | Verify that the grant type is entered in the header. |
| 4709 | Redirect URI mismatch. | The redirect_uri is missing or the value is null or is incorrect. | Verify that the redirect_uri is entered correctly. |
| 4711 | Refresh token invalid. | The token scopes do not match with the client scopes. | Verify that there isn't a mismatch between the token's scopes and the client's scopes. |
| 4717 | The app has been disabled | The app has been disabled. | Contact Zoom support to enable the app. |
| 4724 | Exception error message. | An invalid JWT token is passed in the header. | Verify that the JWT token is correctly signed and that the token passed in the header is valid. |
| 4732 | Creating authorization code error. | The lookup service may be down. ELK logs usually throw a `/lookup/v1/indexes POST 5005` Internal Server error. | Contact your DNS lookup service provider to verify the server status, or contact Zoom for further support. |
| 4733 | Code is expired | Authorization codes have an expiration time of 5 minutes. | Regenerate the authorization code. |
| 4734 | Invalid authorization code. | The authorization code is invalid. | Regenerate the authorization code. |
| 4735 | The owner of the token does not exist. | The user ID of the token doesn't exist. This might happen if the refresh token was issued for a user who has since been removed from an account. The user ID is stored in the `uid` field of a token. | Verify the `uid` for the token is valid and entered correctly. |
| 4737 | Can not find the authentication for the access token. | The refresh token isn't found in the DynamoDB table. | Contact Zoom and request to reauthorize the app. |
| 4738 | The token is disabled by admin. | An admin turned off pre-approval for the related app for users under an account. | Contact Zoom for further support. |
| 4740 | The token ID is out of the token tolerance range. | The maximum number of times a refresh token is allowed to be used has been surpassed. Tolerance errors happen with version 7 tokens. Version 8 and later tokens do not use the tolerance mechanism. | Contact Zoom for assistance with reconfiguring the tolerance range. |
| 4741 | The token has been revoked. | This happens when you perform multiple authorizations. With multiple authorizations, the last token issued is considered valid, and the previous ones are invalidated. | Make sure you are using the latest and valid authorization token. |

## Common Issues Quick Reference

| Symptom | Check |
|---------|-------|
| Empty error (4700) | Check tracking ID in logs |
| Invalid client (4702/4704) | Verify Client ID and Client Secret |
| Grant type error (4705) | Use: `refresh_token`, `authorization_code`, `device_auth`, `account_credentials` |
| Missing credentials (4706) | Ensure Client ID/Secret in header or request params |
| Redirect mismatch (4709) | Verify redirect_uri matches app configuration |
| Token scope mismatch (4711) | Compare token scopes vs client scopes |
| Code expired (4733) | Authorization codes expire in 5 minutes |
| Invalid code (4734) | Regenerate authorization code |
| Token revoked (4741) | Use the most recent token from latest authorization |
