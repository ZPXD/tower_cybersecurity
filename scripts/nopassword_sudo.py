import os
import sys

'''
Allow user to use sudo without password (Good luck!).

If you are still alive, see some most important commands and matetials on linux: http://linuxhot16challenge.info/


ZPXD, Łukasz Pintal.
'''

sudoers_location = '/etc/sudoers'


def update_sudoers(username, action):
	'''
	Adds one line to Linux Ubuntu /etc/sudoers file - or removes it.
	Line allows user to use sudo without password
	(if he or she is in the sudo group)
	or deny it.
	'''

	no_passwd_line = "{} ALL=(ALL) NOPASSWD:ALL".format(username)

	# Allow no password sudo.

	if int(action) != 0: # Allow.		
		os.system('echo "{no_passwd_line}" >> {sudoers_location}'.format(no_passwd_line, sudoers_location))
		print()
		print('Now user {} can use sudo without a password if he or she is in the sudo group.'.format(username))

	# Deny no password sudo.

	else:
		sudoers_lines = open(sudoers_location).readlines()
		sudoers = [l for l in sudoers_lines if not l == user_line]
		with open(sshd_config_file, 'w+') as f:
			f.writelines(sudoers_lines)
		print()
		print('Now user {} cant use sudo without a password if he or she is in the sudo group.'.format(username))

if __name__ == '__main__':
	if len(sys.argv) == 3:
		username = sys.argv[1]
		action = sys.argv[2]
		set_sudoers(username, action)
	else:
		print('No username or no action picked.')
		print('Add two arguments: <username> <int>')
		print()
		print('1. Deny no password sudo (0):')
		print('python3 prepare_sudoers.py 0')
		print()
		print('2. Allow no password sudo (1):')
		print('python3 prepare_sudoers.py 1')
