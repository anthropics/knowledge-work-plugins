# Cryptography Reference

## Hashing

### Common Hash Functions

```vcl
declare local var.hash STRING;

// MD5 (not for security, only checksums)
set var.hash = digest.hash_md5("hello");

// SHA-1 (legacy, avoid for security)
set var.hash = digest.hash_sha1("hello");

// SHA-256 (recommended)
set var.hash = digest.hash_sha256("hello");

// SHA-512
set var.hash = digest.hash_sha512("hello");

// CRC32
set var.hash = digest.hash_crc32("hello");

// xxHash (fast, non-cryptographic)
set var.hash = digest.hash_xxh32("hello");
set var.hash = digest.hash_xxh64("hello");
```

### Base64 Encoded Hashes

```vcl
declare local var.hash STRING;

// SHA-256 with base64 output
set var.hash = digest.hash_sha256_base64("hello");

// SHA-512 with base64 output
set var.hash = digest.hash_sha512_base64("hello");
```

## HMAC (Keyed Hashing)

```vcl
declare local var.sig STRING;
declare local var.key STRING;

set var.key = "secret_key";

// HMAC-MD5
set var.sig = digest.hmac_md5(var.key, "message");

// HMAC-SHA1
set var.sig = digest.hmac_sha1(var.key, "message");

// HMAC-SHA256 (recommended)
set var.sig = digest.hmac_sha256(var.key, "message");

// HMAC-SHA512
set var.sig = digest.hmac_sha512(var.key, "message");

// Base64 encoded output
set var.sig = digest.hmac_sha256_base64(var.key, "message");
```

## Base64 Encoding

### Encode

```vcl
declare local var.encoded STRING;

// Standard Base64
set var.encoded = digest.base64("hello world");

// URL-safe Base64
set var.encoded = digest.base64url("hello world");

// No padding
set var.encoded = digest.base64url_nopad("hello world");
```

### Decode

```vcl
declare local var.decoded STRING;

// Standard Base64 decode
set var.decoded = digest.base64_decode("aGVsbG8gd29ybGQ=");

// URL-safe Base64 decode
set var.decoded = digest.base64url_decode("aGVsbG8gd29ybGQ");

// No padding decode
set var.decoded = digest.base64url_nopad_decode("aGVsbG8gd29ybGQ");
```

## Hex Encoding

```vcl
declare local var.hex STRING;
declare local var.bin STRING;

// Base64 to hex
set var.hex = bin.base64_to_hex("aGVsbG8=");  // "68656c6c6f"

// Hex to base64
set var.bin = bin.hex_to_base64("68656c6c6f");  // "aGVsbG8="
```

## Secure Comparison

Constant-time comparison to prevent timing attacks:

```vcl
declare local var.match BOOL;

set var.match = digest.secure_is_equal("secret1", "secret2");

if (digest.secure_is_equal(req.http.X-API-Key, table.lookup(api_keys, "valid_key"))) {
  // Authenticated
}
```

## Signature Verification

### RSA Signature Verification

```vcl
declare local var.valid BOOL;
declare local var.pubkey STRING;
declare local var.signature STRING;
declare local var.message STRING;

set var.pubkey = {"-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...
-----END PUBLIC KEY-----"};

set var.signature = req.http.X-Signature;
set var.message = req.http.X-Message;

// RSA-SHA256 verification
set var.valid = digest.rsa_verify(
  sha256,
  digest.base64_decode(var.signature),
  var.message,
  digest.base64_decode(var.pubkey)
);

if (!var.valid) {
  error 401 "Invalid signature";
}
```

### ECDSA Signature Verification

```vcl
declare local var.valid BOOL;

set var.valid = digest.ecdsa_verify(
  sha256,
  digest.base64_decode(req.http.X-Signature),
  "message to verify",
  digest.base64_decode(var.pubkey)
);
```

## AWS Signature v4

For signing requests to AWS services:

```vcl
declare local var.signature STRING;

set var.signature = digest.awsv4_hmac(
  var.secret_key,
  var.date,         // YYYYMMDD
  var.region,       // us-east-1
  var.service,      // s3
  var.string_to_sign
);
```

## Common Patterns

### API Key Validation

```vcl
table api_keys STRING {
  "abc123": "user1",
  "def456": "user2",
}

sub vcl_recv {
  #FASTLY recv

  declare local var.key STRING;
  declare local var.user STRING;

  set var.key = req.http.X-API-Key;
  set var.user = table.lookup(api_keys, var.key);

  if (!var.user) {
    error 401 "Invalid API key";
  }

  set req.http.X-User = var.user;
}
```

### JWT Validation (Simple)

```vcl
sub vcl_recv {
  #FASTLY recv

  declare local var.token STRING;
  declare local var.header STRING;
  declare local var.payload STRING;
  declare local var.signature STRING;
  declare local var.expected_sig STRING;
  declare local var.secret STRING;

  set var.secret = "your-256-bit-secret";

  // Extract token from Authorization header
  if (req.http.Authorization ~ "^Bearer (.+)$") {
    set var.token = re.group.1;
  } else {
    error 401 "Missing token";
  }

  // Split JWT parts (header.payload.signature)
  if (var.token ~ "^([^.]+)\.([^.]+)\.([^.]+)$") {
    set var.header = re.group.1;
    set var.payload = re.group.2;
    set var.signature = re.group.3;
  } else {
    error 401 "Invalid token format";
  }

  // Verify HMAC-SHA256 signature
  set var.expected_sig = digest.base64url_nopad(
    digest.hmac_sha256(var.secret, var.header + "." + var.payload)
  );

  if (!digest.secure_is_equal(var.signature, var.expected_sig)) {
    error 401 "Invalid signature";
  }

  // Decode payload and pass to backend
  set req.http.X-JWT-Payload = digest.base64url_decode(var.payload);
}
```

### Request Signing

```vcl
sub vcl_miss {
  #FASTLY miss

  declare local var.timestamp STRING;
  declare local var.signature STRING;
  declare local var.secret STRING;

  set var.secret = "shared_secret";
  set var.timestamp = strftime({"%Y%m%dT%H%M%SZ"}, now);

  // Create signature
  set var.signature = digest.hmac_sha256_base64(
    var.secret,
    bereq.method + bereq.url + var.timestamp
  );

  // Add to backend request
  set bereq.http.X-Timestamp = var.timestamp;
  set bereq.http.X-Signature = var.signature;
}
```

### Cache Key Hashing

```vcl
sub vcl_hash {
  #FASTLY hash

  // Create a hash of request properties for cache key
  declare local var.key STRING;
  set var.key = digest.hash_sha256(
    req.http.Host + req.url.path + req.http.Accept-Language
  );
  set req.hash = var.key;
}
```

### Basic Auth Verification

```vcl
sub vcl_recv {
  #FASTLY recv

  declare local var.expected STRING;
  declare local var.provided STRING;

  // Expected: "username:password" base64 encoded
  set var.expected = digest.base64("admin:secret123");

  // Extract provided credentials
  if (req.http.Authorization ~ "^Basic (.+)$") {
    set var.provided = re.group.1;
  } else {
    error 401 "Authorization required";
  }

  if (!digest.secure_is_equal(var.provided, var.expected)) {
    error 401 "Invalid credentials";
  }
}

sub vcl_error {
  #FASTLY error

  if (obj.status == 401) {
    set obj.http.WWW-Authenticate = {"Basic realm="Protected""};
    return (deliver);
  }
}
```

## Function Reference

| Function                                  | Description            |
| ----------------------------------------- | ---------------------- |
| `digest.hash_md5(s)`                      | MD5 hash (hex)         |
| `digest.hash_sha1(s)`                     | SHA-1 hash (hex)       |
| `digest.hash_sha256(s)`                   | SHA-256 hash (hex)     |
| `digest.hash_sha512(s)`                   | SHA-512 hash (hex)     |
| `digest.hash_sha256_base64(s)`            | SHA-256 hash (base64)  |
| `digest.hmac_sha256(key, msg)`            | HMAC-SHA256 (hex)      |
| `digest.hmac_sha256_base64(key, msg)`     | HMAC-SHA256 (base64)   |
| `digest.base64(s)`                        | Base64 encode          |
| `digest.base64_decode(s)`                 | Base64 decode          |
| `digest.base64url(s)`                     | URL-safe base64 encode |
| `digest.base64url_decode(s)`              | URL-safe base64 decode |
| `digest.secure_is_equal(a, b)`            | Constant-time compare  |
| `digest.rsa_verify(alg, sig, msg, key)`   | RSA signature verify   |
| `digest.ecdsa_verify(alg, sig, msg, key)` | ECDSA signature verify |
