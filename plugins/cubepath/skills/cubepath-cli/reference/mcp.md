# cubecli mcp

Connect the CubePath MCP server to your AI agents

## `cubecli mcp install`

Add the CubePath MCP server to your AI agents

Usage: `cubecli mcp install [flags]`

- `--agent stringSlice`: Agent to configure: claude, codex, gemini, cursor, vscode or all (repeatable; default: detected agents)

Examples:

```
  cubecli mcp install
  cubecli mcp install --agent claude --agent cursor
```

## `cubecli mcp status`

Show which AI agents have the CubePath MCP server

Usage: `cubecli mcp status`

## `cubecli mcp uninstall`

Remove the CubePath MCP server from your AI agents

Remove the CubePath MCP server from your AI agents' configuration.

This does not revoke the access they were granted. Disconnect them at
https://my.cubepath.com/account/connections.

Usage: `cubecli mcp uninstall [flags]`

- `--agent stringSlice`: Agent: claude, codex, gemini, cursor, vscode or all (default: every agent that has it)
