#!/usr/bin/env python3

import os
import subprocess
import yaml

# Clone the repository
subprocess.run(
    ['git', 'clone', 'https://github.com/brulejr/ansible-homelab.git'])
os.chdir('ansible-homelab')

# Set up static defaults
server_name = "localhost"
username = "sysadm"
puid = "1000"
pgid = "1000"
private_key_path = "/home/sysadm/.ssh/rsa"

# load configuration file defaults
with open('../config.yml', 'r') as stream:
    config = yaml.safe_load(stream)
server_name = config.get('server_name', server_name)
username = config.get('username', username)
puid = config.get('puid', puid)
pgid = config.get('pgid', pgid)
private_key_path = config.get('private_key_path', private_key_path)
cloudflare_email = config.get('cloudflare_email')
cloudflare_dns_token = config.get('cloudflare_dns_token')
traefik_user_hash = config.get('traefik_user_hash')

# Read user input
domain_name = input("Enter the domain name: ")
server_name = input(f"Enter server name [{server_name}]: ").strip() or server_name
username = input(f"Enter username [{username}]: ").strip() or username
puid = input(f"Enter puid for the user [{puid}]: ").strip() or puid
pgid = input(f"Enter pgid for the user [{pgid}]: ").strip() or pgid
cloudflare_email = input(f"Enter the Cloudflare email [{cloudflare_email}]: ") or cloudflare_email
cloudflare_dns_token = input(f"Enter the Cloudflare DNS Token [{cloudflare_dns_token}]: ") or cloudflare_dns_token
traefik_user_hash = input(f"Enter Traefik dashboard user hash [{traefik_user_hash}]: ") or traefik_user_hash
 
# Replace values in vars.yml file
with open('group_vars/all/vars.yml', 'r') as f:
    content = f.read()
content = content.replace('<server_name>', server_name)
content = content.replace('<username>', username)
content = content.replace('<puid>', puid)
content = content.replace('<pgid>', pgid)
content = content.replace('<domain_name>', domain_name)
content = content.replace('<cloudflare_email>', cloudflare_email)
content = content.replace('<cloudflare_dns_token>', cloudflare_dns_token)
content = content.replace('<traefik_basic_auth_hash>', traefik_user_hash)
with open('group_vars/all/vars.yml', 'w') as f:
    f.write(content)

# Replace values in inventory file
with open('inventory', 'r') as f:
    content = f.read()
content = content.replace('<server_name>', server_name)
content = content.replace('<username>', username)
private_key_path = input(f"Enter path to private key [{private_key_path}]: ").strip() or private_key_path
content = content.replace('<path/to/private/key>', private_key_path)
with open('inventory', 'w') as f:
    f.write(content)

# Run the playbook
subprocess.run(['ansible-playbook', 'main.yml'])