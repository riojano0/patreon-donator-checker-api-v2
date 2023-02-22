#[WIP] Patreon donator checker api V2

Create api take simple information from patreon to know status of your patreons

Demo: https://patreon-donator-checker-api-v2.onrender.com/docs

# What is set?

Currently, have a configuration that show in the response the following cases configure for the campaign 1874794

- User Active -> More than 300cents and not decline and not pause
- User Inactive -> Less than 300cents and not decline and not pause
- User Inactive -> Decline or pause


## Example:

```json
[
  {
    "id": "1234568",
    "patreon_uid": "989b9376-2e4b-4c31-8fbd-cb6fb1743999",
    "username": "dummy1",
    "mail": "dummy1@test.com",
    "status": "INACTIVE",
    "tier": null
  },
    {
    "id": "1234568",
    "patreon_uid": "989b9376-2e4b-4c31-8fbd-cb6fb174399A",
    "username": "dummy1",
    "mail": "dummy1@test.com",
    "status": "ACTIVE",
    "tier": "Tier 2"
  }
  
]
```

# What environment variables I need?

- ACCESS_TOKEN: Access token provide by Patreon
- X-API-Key-Valid: Internal key used to validate request from know resources

### Pending
- Fetch specific users
- ~~Create cache/database to fetch on the same 1 minutes~~
  