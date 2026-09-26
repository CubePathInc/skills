# cubecli auth

Log in, log out and inspect credentials

## `cubecli auth login`

Log in to CubePath in the browser and store the session in a profile

Log in to CubePath through your browser and store the session in a profile.

Each profile holds the session of one organization, chosen on the consent
screen. Log in once per organization and switch with 'cubecli profile use'
or '--profile'.

Without a profile name, the active profile is used ('default' if none).

For CI and other non-interactive use, store an API token instead with
'--token', or set CUBE_API_TOKEN.

Usage: `cubecli auth login [profile] [flags]`

- `--api-url string`: API URL for this profile (kept from the existing profile if omitted)
- `--no-browser`: Print the login URL instead of opening a browser
- `--skip-mcp`: Do not offer to add the CubePath MCP server to AI agents
- `--skip-skills`: Do not offer to install the CubePath skills for AI agents
- `--token`: Store an API token instead of logging in with the browser
- `--use`: Make this the active profile

Examples:

```
  cubecli login
  cubecli login work
  cubecli login staging --api-url https://api.staging.cubepath.com
  cubecli login --no-browser      # over SSH, no local browser
  cubecli login ci --token        # store an API token
```

## `cubecli auth logout`

Revoke the session of a profile and remove its credentials

Revoke the browser session of a profile on CubePath and remove its stored
credentials. The profile itself (name, API URL) is kept, so 'cubecli login
<profile>' logs it back in. Use 'cubecli profile delete' to remove it entirely.

API tokens are only removed locally: revoke them in the dashboard.

Usage: `cubecli auth logout [profile] [flags]`

- `--all`: Log out every profile

## `cubecli auth status`

Show how each profile is authenticated

Usage: `cubecli auth status`
