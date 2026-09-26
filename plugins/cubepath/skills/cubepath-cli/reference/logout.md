# cubecli logout

Revoke the session of a profile and remove its credentials

## `cubecli logout`

Revoke the session of a profile and remove its credentials

Revoke the browser session of a profile on CubePath and remove its stored
credentials. The profile itself (name, API URL) is kept, so 'cubecli login
<profile>' logs it back in. Use 'cubecli profile delete' to remove it entirely.

API tokens are only removed locally: revoke them in the dashboard.

Usage: `cubecli logout [profile] [flags]`

- `--all`: Log out every profile
