# BYOS (Bring Your Own Storage)

Video SDK feature that saves cloud recordings **directly** to your Amazon S3 bucket. No downloading required.

> **Official docs:** https://developers.zoom.us/docs/build/storage/

## How BYOS Works

```
┌─────────────────┐                    ┌─────────────────┐
│   Video SDK     │                    │    Your AWS     │
│    Session      │   Direct Upload    │    S3 Bucket    │
│                 │ ──────────────────►│                 │
│  Recording...   │   (via IAM role    │  .mp4 .m4a .txt │
│                 │    or access key)  │                 │
└─────────────────┘                    └─────────────────┘
```

## BYOS vs Recording Download Pipeline

| Aspect | BYOS (Video SDK) | Recording Download Pipeline |
|--------|------------------|----------------------------|
| How it works | Zoom writes directly to your S3 | You download from Zoom, upload to S3 |
| Products | Video SDK only | Zoom Meetings |
| Latency | During recording | After recording completes |
| Your infrastructure | Just S3 bucket + credentials | Webhook server + download code |
| Bandwidth cost | None (direct to S3) | You pay for download |

## Prerequisites

- Video SDK account with **Cloud Recording add-on plan** (Universal Credit plans include this)
- AWS account with administrator access
- Amazon S3 bucket

## S3 File Path Structure

BYOS recordings are stored at:

```
Buckets/{bucketName}/cmr/byos/{YYYY}/{MM}/{DD}/{GUID}/cmr_byos/
```

## Setup

### Step 1: Create S3 Bucket

Create a private S3 bucket with "Block all public access" enabled.

### Step 2: Enable BYOS in Zoom Portal

1. Go to **Developer account web portal**
2. Navigate to **Account Settings** → **General** → **Communications Content Storage Location**
3. Toggle **Bring Your Own Storage** on
4. Click **Manage Storage** → **Add Storage**

### Step 3: Choose Authentication Method

#### Option A: AWS Access Key (Simpler)

1. Enter your **Access Key ID** and **Access Secret Key**
2. Zoom encrypts these values
3. Click **Save**

#### Option B: Cross Account Access (More Secure)

1. **Enter Your ARN** in format:
   ```
   arn:aws:iam::YOUR_AWS_ACCOUNT_ID:role/ZoomArchivingRole
   ```

2. **Get Zoom Account ID** from the help text below the ARN field, or via [Get Account Settings API](https://developers.zoom.us/docs/api/accounts/#tag/accounts/get/accounts/{accountId}/settings)

3. **Create IAM Policy** with these permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "S3BucketList",
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket",
        "s3:GetBucketLocation"
      ],
      "Resource": "arn:aws:s3:::your_bucket_name"
    },
    {
      "Sid": "S3ObjectAccess",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::your_bucket_name/*"
    }
  ]
}
```

4. **Create Trust Relationship** for the IAM role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "Zoom_ARN"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "YOUR_ZOOM_ACCOUNT_ID"
        }
      }
    }
  ]
}
```

### Step 4: Verify Configuration

Zoom performs HTTP PUT, GET, and LIST operations against your bucket to validate credentials.

### Step 5: Test

Record a Video SDK session and verify recordings appear in your S3 bucket.

## Managing Storage Locations

- **Multiple locations:** You can add multiple storage locations, but only one is the default
- **Switch default:** Use the ellipsis menu to change the default location
- **Delete:** Cannot delete the only storage location; add another first

### Via API

Use the [Video SDK BYOS Storage APIs](https://developers.zoom.us/docs/api/video-sdk/#tag/byos-storage):

| Endpoint | Description |
|----------|-------------|
| `GET /v2/videosdk/byos/storage` | List storage locations |
| `POST /v2/videosdk/byos/storage` | Add storage location |
| `DELETE /v2/videosdk/byos/storage/{storageId}` | Delete storage location |
| `PATCH /v2/videosdk/byos/storage/{storageId}` | Update storage location |

## Managing Recordings

Use the [Cloud Recording APIs](https://developers.zoom.us/docs/api/video-sdk/#tag/cloud-recording) to manage, play, and download BYOS recordings.

**Important:** Cloud recordings have two components:

| Component | Location | Managed by |
|-----------|----------|------------|
| Metadata | Zoom (portal) | Zoom APIs / Web Portal |
| Recording files | Your S3 bucket | You / AWS |

## Web Portal Limitations

The Zoom web portal only manages **metadata**, not S3 files:

- **Delete in portal** → Only removes metadata, S3 files remain
- **Trash recovery** → Restore metadata within 30 days to re-enable playback
- **After 30 days** → Metadata permanently deleted, no portal playback (files still in S3)

**Recommendation:** Use APIs for full control over BYOS recordings.

## Effects of Disabling BYOS

| Action | Metadata | S3 Files |
|--------|----------|----------|
| Toggle BYOS off | Deleted from Recordings page | Unaffected |
| Delete storage location | Deleted from Recordings page | Unaffected |

**Warning:** Both actions permanently remove metadata. Re-adding the same storage location won't restore playback in the portal.

## Troubleshooting

### Verify Storage Location

1. Click **Manage Storage**
2. Click **ellipsis** → **Verify**

This tests region, bucket, and credentials.

### Check AWS CloudTrail

Look for `AssumeRole` or `PutObject` errors:

```bash
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=AssumeRole
```

### Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Upload fails | Invalid credentials | Verify access key or IAM role |
| Permission denied | Missing S3 permissions | Check IAM policy has all required actions |
| Bucket not found | Wrong region/name | Verify bucket name and region match exactly |

## Security Best Practices

1. **Use Cross Account Access** over access keys when possible
2. **Set External ID** to your Zoom account ID (prevents confused deputy)
3. **Enable S3 encryption** (SSE-S3 or SSE-KMS)
4. **Enable bucket versioning** for recovery
5. **Audit IAM roles** regularly for least privilege
6. **Delete during off-peak hours** to avoid incomplete uploads

## Resources

- **BYOS Overview:** https://developers.zoom.us/docs/build/storage/
- **Get Started:** https://developers.zoom.us/docs/build/storage-get-started/
- **Manage Storage:** https://developers.zoom.us/docs/build/storage-manage/
- **BYOS Storage APIs:** https://developers.zoom.us/docs/api/video-sdk/#tag/byos-storage
- **Cloud Recording APIs:** https://developers.zoom.us/docs/api/video-sdk/#tag/cloud-recording
