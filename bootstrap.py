#!/usr/bin/env python3

import os
import subprocess

# Clone the repository
subprocess.run(
    ['git', 'clone', 'https://github.com/brulejr/ansible-homelab.git'])
os.chdir('ansible-homelab')

# Set up defaults
server_ip = "localhost"
timezone = "America/New_York"
username = "sysadm"
puid = "1000"
pgid = "1000"

# Read user input
server_ip = input(f"Enter server IP address [{server_ip}]: ").strip() or server_ip
timezone = input(f"Enter timezone [{timezone}]: ").strip() or timezone
username = input(f"Enter username [{username}]: ").strip() or username
puid = input(f"Enter puid for the user [{puid}]: ").strip() or puid
pgid = input(f"Enter pgid for the user [{pgid}]: ").strip() or pgid

# Replace values in vars.yml file
with open('group_vars/all/vars.yml', 'r') as f:
    content = f.read()
content = content.replace('<server_ip>', server_ip)
content = content.replace('<timezone>', timezone)
content = content.replace('<username>', username)
content = content.replace('<puid>', puid)
content = content.replace('<pgid>', pgid)
with open('group_vars/all/vars.yml', 'w') as f:
    f.write(content)

# Replace values in inventory file
with open('inventory', 'r') as f:
    content = f.read()
content = content.replace('<server_ip>', server_ip)
content = content.replace('<username>', username)
private_key_path = input("Enter path to private key: ")
content = content.replace('<path/to/private/key>', private_key_path)
with open('inventory', 'w') as f:
    f.write(content)

# Run the playbook
subprocess.run(['ansible-playbook', 'main.yml'])