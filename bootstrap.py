#!/usr/bin/env python3

import os
import subprocess

# Clone the repository
subprocess.run(
    ['git', 'clone', 'https://github.com/brulejr/ansible-homelab.git'])
os.chdir('ansible-homelab')

# Read user input
server_ip = input("Enter server IP address: ")
timezone = input("Enter timezone: ")
username = input("Enter username: ")
puid = input("Enter puid of the user: ")
pgid = input("Enter pgid of the user: ")

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