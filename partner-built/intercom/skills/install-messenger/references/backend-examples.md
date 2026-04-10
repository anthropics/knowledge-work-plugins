# Backend JWT Endpoint Examples

All examples implement the same pattern: read the Identity Verification Secret from an environment variable, sign a JWT with HS256 containing the required claims, and return `{ "token": "<jwt>" }`. The endpoint must be authentication-protected.

See the main SKILL.md for the required JWT claims table and the canonical Node.js/Express example.

## Python / Flask

```python
import jwt
import time
import os

INTERCOM_SECRET = os.environ['INTERCOM_IDENTITY_SECRET']

@app.route('/api/intercom-jwt')
@login_required
def intercom_jwt():
    token = jwt.encode(
        {
            'user_id': str(current_user.id),
            'email': current_user.email,
            'name': current_user.name,
            'exp': int(time.time()) + 7200,  # 2 hours
        },
        INTERCOM_SECRET,
        algorithm='HS256',
    )
    return {'token': token}
```

## Python / Django

```python
# views.py
import jwt
import time
import os
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

INTERCOM_SECRET = os.environ['INTERCOM_IDENTITY_SECRET']

@login_required
def intercom_jwt(request):
    token = jwt.encode(
        {
            'user_id': str(request.user.id),
            'email': request.user.email,
            'name': request.user.get_full_name(),
            'exp': int(time.time()) + 7200,  # 2 hours
        },
        INTERCOM_SECRET,
        algorithm='HS256',
    )
    return JsonResponse({'token': token})
```

Add the URL pattern: `path('api/intercom-jwt', views.intercom_jwt)` in `urls.py`.

## PHP

Requires the `firebase/php-jwt` package: `composer require firebase/php-jwt`

```php
<?php
// api/intercom-jwt.php
require_once 'vendor/autoload.php';
use Firebase\JWT\JWT;

$secret = getenv('INTERCOM_IDENTITY_SECRET');
$user = get_authenticated_user(); // Your auth logic

$token = JWT::encode([
    'user_id' => (string) $user->id,
    'email' => $user->email,
    'name' => $user->name,
    'exp' => time() + 7200, // 2 hours
], $secret, 'HS256');

header('Content-Type: application/json');
echo json_encode(['token' => $token]);
```

## Ruby / Rails

```ruby
# app/controllers/api/intercom_controller.rb
class Api::IntercomController < ApplicationController
  before_action :authenticate_user!

  def jwt
    token = JWT.encode(
      {
        user_id: current_user.id.to_s,
        email: current_user.email,
        name: current_user.name,
        exp: 2.hours.from_now.to_i,
      },
      ENV['INTERCOM_IDENTITY_SECRET'],
      'HS256'
    )

    render json: { token: token }
  end
end
```

**Alternative: `intercom-rails` gem** — For simpler setups, install with `gem "intercom-rails"`, run `rails generate intercom:config YOUR_WORKSPACE_ID`, and configure the secret in the generated initializer. See the [Intercom install page](https://app.intercom.com/a/apps/_/settings/channels/messenger/install) for details.
