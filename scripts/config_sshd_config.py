import os
import sys


'''
What, why

python3 
'''

'''
To be developed.
'''

sshd_config_file = '/etc/ssh/sshd_config'
sshd_config_lines = open(sshd_config_file).readlines()

checked_items = []
checked_lines = []
for line in sshd_config_lines:

	# Key

	item = 'PubkeyAuthentication'
	if item in line and not item in checked_items:
		line = 'PubkeyAuthentication yes' + '\n'
		checked_lines.append(line)
		checked_items.append(line)

	# Root

	item = 'PermitRootLogin'
	if item in line and not item in checked_items:
		line = 'PermitRootLogin no' + '\n'
		checked_lines.append(line)
		checked_items.append(line)

	# Passwords

	item = 'PasswordAuthentication'
	if item in line and not item in checked_items:
		line = 'PasswordAuthentication no' + '\n'
		checked_lines.append(line)
		checked_items.append(line)

	# Check

	#item = 'PermitEmptyPasswords'
	#if item in line and not item in checked_items:
	#	line = 'PermitEmptyPasswords no'
	#	checked_lines.append(line)
	#	checked_items.append(line)

with open(sshd_config_file, 'w+') as f:
	f.writelines(checked_lines)

with open(sshd_config_file+'_backup', 'w+') as f:
	f.writelines([l + '\n' for l in sshd_config_lines])



# Na potem do rozważenia:

# Pomysł Mist'a:

# PermitRootLogin no
# LoginGraceTime 20
# PasswordAuthentication no
# PermitEmptyPasswords no
# ChallengeResponseAuthentication no
# KerberosAuthentication no
# GSSAPIAuthentication no
# X11Forwarding no
# ClientAliveInterval  360
# ClientAliveCountMax 10

# Inne:

# PermitTunnel
 
