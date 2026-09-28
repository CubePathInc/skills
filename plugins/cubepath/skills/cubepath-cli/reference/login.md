# cubecli login

Log in to CubePath and store the credentials in a profile

## `cubecli login`

Log in to CubePath and store the credentials in a profile

Log in to CubePath and store the credentials in a profile.

cubecli login signs you in through the browser when the CubePath API supports
it; otherwise it asks for an API token, which you create at
https://my.cubepath.com/organization/tokens.

Each profile holds the credentials of one organization. Log in once per
organization and switch with 'cubecli profile use' or '--profile'.

Without a profile name, the active profile is used ('default' if none).

For CI and other non-interactive use, pass '--token' or set CUBE_API_TOKEN.

Usage: `cubecli login [profile] [flags]`

- `--api-url string`: API URL for this profile (kept from the existing profile if omitted)
- `--no-browser`: For browser sign-in, print the URL instead of opening a browser
- `--skip-mcp`: Do not offer to add the CubePath MCP server to AI agents
- `--skip-skills`: Do not offer to install the CubePath skills for AI agents
- `--token`: Use an API token instead of the browser sign-in
- `--use`: Make this the active profile

Examples:

```
  cubecli login
  cubecli login work
  cubecli login staging --api-url https://api.staging.cubepath.com
  cubecli login ci --token        # always use an API token
```
