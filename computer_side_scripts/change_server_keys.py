import os
import sys
import platform
import time
from paramiko import SSHConfig


'''
Create / change your RSA key pair and blocks loging in by a password.

PS: On Windows just open powershell and see this shining commands:
ssh-keygen -t rsa -b 4096 -N "" -f <key-name>
ssh-copy-id <name>@<ip> -f
Will create key for you to use it. Update config file with a key as shown in lines 25-33


Create keys requirements:
1. Server with user with password
2. Server allows password login


Change keys requirements:
1. If you want to change keys fill ~/.ssh/config file correctly fg.

Host linuxhot_r
	HostName 1.1.1.1
	User root

Host linuxhot
	HostName 1.1.1.1
	User luke
	IdentityFile ~/.ssh/linuxhot_key

2. Allow password login on server for user you want to change keys for.


ZPXD, Łukasz Pintal.
'''



class KeyMaker():
	
	# Path & command templates.
	ssh_keygen = '''ssh-keygen -t rsa -b 4096 -N "" -f {}'''
	ssh_copy_id = 'ssh-copy-id -i {} {}@{} -f'

	def __init__(self, ssh_config):
		self.ssh_config = ssh_config
		self.key = '/'.join(ssh_config.split('/')[:-1]) +  '/key_{}'

	def create_server_keys_frominput(self):
		'''
		Creates RSA key pair by input data.
		'''

		# Informations.
		ip_adress = input('Enter IP (1.1.1.1):')
		server_user = input('Enter your username on server:')
		self.create_server_keys(server_user=server_user, ip_adress=ip_adress)

	def create_server_keys(self, server_user=None, ip_adress=None):
		'''
		Creates RSA key pair.
		'''
		try:
			# Prepare commands.
			key = self.key.format(server_user) + "__" + ip_adress.replace('.', "_")

			ssh_keygen = self.ssh_keygen.format(key)
			ssh_copy_id = self.ssh_copy_id.format(key, server_user, ip_adress)

			# Create key and make it avaliable for server.
			os.popen(ssh_keygen)
			time.sleep(2)
			os.system(ssh_copy_id)

			# Block loging in by a password.
			os.system('bash allow_password_login_to_server_by_user_ip.sh 0 {} {}'.format(server_user, ip_adress))

			print('Done. Protect your ssh folder. Protect your private key. Connect by ssh key now.')

		except Exception as e:
			print(e)
			print('Could not finish creating the key for {}.'.format(ip_adress))
			print('Read script requirements.')

	def change_server_keys(self, other_config=None):
		'''
		Changes RSA keys for all servers specified in ~/.ssh/config or other_config file.

		other_config: path to file written in ssh_config style.
		'''

		# Open ssh config file and load it's values to config.
		config = SSHConfig()
		if other_config:
			config.parse(open(other_config))
		else:
			config.parse(open(self.ssh_config))

		# For every config hostnames.
		hostnames = config.get_hostnames()
		for host in hostnames:
			try:
				# Get ssh connection informations.
				server_ssh_auth = config.lookup(host)
				ip_adress = server_ssh_auth['hostname']
				user = server_ssh_auth['user']
				key = server_ssh_auth['identityfile'][0]
					
				# Prepare commands.
				key = self.key.format(user)
				ssh_keygen = self.ssh_keygen.format(key)
				ssh_copy_id = self.ssh_copy_id.format(key, user, ip_adress)

				# Create key and make it avaliable for server.
				os.popen(ssh_keygen)
				time.sleep(2)
				os.system(ssh_copy_id)

			except:
				print('Could not finish creating the key for host {}.'.format(host))
				print('Read script requirements.')
			continue

		print('Done. Protect your ssh folder. Protect your private key. Connect by ssh key now.')

def intro():

	print('Program creates SSH RSA key pair or changes it for one or multiple servers stated by input or automatically imported from config file.')
	print('')
	print('For using script automatically you need to have config file in order.')
	print('')
	print('Check your ~/.ssh/config file for: [read online where to find config if you are lost, its easy].')
	print('')
	print('1. correct Host - no spaces or wierd names in Host field')
	print('2. correct IP')
	print('3. correct server username')
	print('4. correct key path for your key in IdentityFile path fg. "~/.ssh/linuxhot_key". ')
	print('5. rather correct file format and some order in the file.')
	print('')
	print('Host linuxhot_r        # <---- this is how you name your host.')
	print('    HostName 1.1.1.1   # <---- this is your server ip')
	print('    User root          # <---- this is your user: root')
	print('')
	print('Host linuxhot          # <---- name')
	print('    HostName 1.1.1.1   # <---- ip')
	print('    User luke          # <---- user but not root')	
	print('    IdentityFile ~/.ssh/linuxhot_key # <---- !!! path to key')
	print('')
	print('Usage 1: create new key:')
	print('python3 change_server_keys.py')
	print('')
	print('Usage 2: change keys')
	print('python3 change_server_keys.py nowe_kluczyki_xDDD')
	print('')
	print('Usage 3:')
	print('use this script in other script.')
	print('')

def outro():
	print('now you can connect to server by: ssh <Host> where host is how you named your Host in config file.')



if __name__ == "__main__":

	# Platform.

	# 1. Windows.
	if platform.system() == 'Windows':
		print('You use this script on Windows. Windows usage undergoes testing yet. Check repo in few days for update.')

	# 2. Woah.
	elif platform.system() == 'Darwin':
		print('You use this script on MAC. Windows usage undergoes testing yet. Check repo in few days for update.')

	# 3. Linux.
	else:

		# Change keys / create new keys for all servers stated correctly in ~/.ssh/config file.
		if len(sys.argv) == 2:
			computer_user = os.getlogin()
			ssh_config = '/home/{}/.ssh/config'.format(computer_user)
			if '/' in sys.argv[1]:
				ssh_config = sys.argv[1]
			KM = KeyMaker(ssh_config)
			KM.change_server_keys()
		
		# Create 1 new key pair:
		elif len(sys.argv) == 3:
			server_user = sys.argv[1]
			ip_adress = sys.argv[2]
			computer_user = os.getlogin()
			ssh_config = '/home/{}/.ssh/config'.format(computer_user)
			KM = KeyMaker(ssh_config)
			KM.create_server_keys(server_user=server_user, ip_adress=ip_adress)
		else:
			intro()
			computer_user = os.getlogin()
			ssh_config = '/home/{}/.ssh/config'.format(computer_user)
			KM = KeyMaker(ssh_config)
			KM.create_server_keys_frominput()
			outro()


