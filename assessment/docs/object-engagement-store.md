# Future object engagement store boundary

`EngagementStore` remains the only persistence contract used by assessment
services. A future `ObjectEngagementStore` may map validated relative POSIX
keys directly to object keys below one engagement prefix.

The future implementation must:

- use an immutable object generation/version token for optimistic concurrency;
- upload content-addressed objects before publishing a canonical manifest;
- promote one manifest object atomically (or with a compare-and-swap precondition)
  so readers observe either the prior snapshot or the complete new snapshot;
- preserve the same canonical JSON, checksum, version, evidence-admission, and
  archive-hygiene rules as `LocalEngagementStore`;
- never place credentials, local absolute paths, bucket names, or provider
  metadata in portable engagement state.

No S3 SDK, upload, bucket, credential, cloud resource, or Terraform behavior is
implemented in Phase 2. The skipped contract placeholder in the portability
suite records this boundary and its reason.
