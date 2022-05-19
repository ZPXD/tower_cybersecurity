import os
import sys



'''
Allow/Deny password login 
(and allow login by a key).

Be sure you got your SSH key on your computer before starting.
Script configure sshd_config file.


ZPXD, Łukasz Pintal.
'''


sshd_config_file = '/etc/ssh/sshd_config'
sshd_config_lines = open(sshd_config_file).readlines()


def allow_server_password_login(allow=-1):

	# Adjust file options: allow/deny password authentication.

	lines = ""
	for line in sshd_config_lines:
		if allow == 1:
			if 'PermitRootLogin' in line:
				lines += 'PermitRootLogin yes' + '\n'
			elif 'PasswordAuthentication' in line:
				lines += 'PasswordAuthentication yes' + '\n'
			elif 'PubkeyAuthentication' in line:
				lines += 'PubkeyAuthentication yes' + '\n'
			else:
				lines += line + '\n'
		elif allow == 0:
			if 'PermitRootLogin' in line:
				lines += 'PermitRootLogin no' + '\n'
			elif 'PasswordAuthentication' in line:
				lines += 'PasswordAuthentication no' + '\n'
			elif 'PubkeyAuthentication' in line:
				lines += 'PubkeyAuthentication yes' + '\n'
			else:
				lines += line + '\n'
		else:
			print('Use script with argument:\n')
			print('python3 allow_server_password_login.py 0')
			print('python3 allow_server_password_login.py 1')

	# Save sshd_config file with backup.

	os.system('rm {}'.format(sshd_config_file))
	with open(sshd_config_file, 'w+') as f:
		f.write(lines)

	with open(sshd_config_file + '_backup', 'w+') as f:
		f.write(sshd_config_lines)

	# Restart ssh services.

	os.system('systemctl restart ssh')
	os.system('systemctl restart sshd')


if __name__ == '__main__':
	allow = -1
	if len(sys.argv) == 2:
		allow = int(sys.argv[1])
	allow_server_password_login(allow)





# TBD In future:

# Mist ideas:

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
# PermitTunnel


