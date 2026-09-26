# cubecli ssh-key

Manage SSH keys

## `cubecli ssh-key create`

Create a new SSH key

Usage: `cubecli ssh-key create [flags]`

- `-f, --public-key-from-file string`: Path to public key file
- `-k, --public-key string`: Public key string
- `-n, --name string`: Name of the SSH key (required)

## `cubecli ssh-key delete`

Delete an SSH key

Usage: `cubecli ssh-key delete <key_id> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli ssh-key list`

List SSH keys

Usage: `cubecli ssh-key list`
