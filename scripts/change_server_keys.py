import os
import sys
import platform
from paramiko import SSHConfig

'''
Create / change your RSA key pair.

for all servers stated in ~/.ssh/config file correctly fg.

Host linuxhot_r
	HostName 1.1.1.1
	User root

Host linuxhot
	HostName 1.1.1.1
	User luke
	IdentityFile ~/.ssh/linuxhot_key

In example above script would make second host renew RSA keys.

ZPXD, Łukasz Pintal.
'''



class KeyMaker():
	
	# Path & command templates.
	key = '~/.ssh/{}_key'
	ssh_keygen = 'ssh-keygen -t rsa -b 4096 -N '' -f {} <<< y'
	ssh_copy_id = 'ssh-copy-id -i {} {}@{} -f'

	def __init__(self, ssh_config):
		self.ssh_config = ssh_config

	def create_server_keys_frominput(self):
		'''
		Creates RSA key pair by input data.
		'''

		# Informations.
		ip_adress = input('Enter IP (1.1.1.1):')
		server_user = input('Enter your username on server:')
		self.reate_server_keys(server_user=server_user, ip_adress=ip_adress)

	def create_server_keys(self, server_user=None, ip_adress=None):
		'''
		Creates RSA key pair.
		'''
		try:
			# Prepare commands.
			key = self.key.format(user)
			ssh_keygen = self.ssh_keygen.format(key)
			ssh_copy_id = self.ssh_copy_id.format(key, server_user, ip_adress)

			# Create key and make it avaliable for server.
			os.system(ssh_keygen)
			os.system(ssh_copy_id)
			print('Done. Protect your ssh folder. Protect your private key. Use public key to access servers.')

		except:
			print('Could not finish creating the key.')
			continue

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
				ssh_copy_id = self.ssh_copy_id.format(key, user, host)

				# Create key and make it avaliable for server.
				os.system(ssh_keygen)
				os.system(ssh_copy_id)
				print(ssh_keygen)
				print(ssh_config)

			except:
				continue

def intro():

	print('Program creates SSH RSA key pair or changes it for one or multiple servers stated by input or automatically imported from config file.')
	print('')
	print('For using script automatically you need to have config file in order.')
	print('Check your ~/.ssh/config file for: [read online where to find config if you are lost, its easy].')
	print('')
	print('1. correct Host - no spaces or wierd names in Host field')
	print('2. correct IP')
	print('3. correct server username')
	print('4. correct key path for your key in IdentityFile path fg. "~/.ssh/linuxhot_key". ')
	print('5. rather correct file format and some order in the file.')
	print('')
	print('')
	example = '''
	Host linuxhot_r
		HostName 1.1.1.1
		User root

	Host linuxhot
		HostName 1.1.1.1
		User luke
		IdentityFile ~/.ssh/linuxhot_key
	'''
	print(example)
	print('')
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


if __name__ == "__main__":

	# Intro.
	intro()

	# Platform.

	# 1. Windows.
	if platform.system() == 'Windows':
		print('You use this script on Windows. Windows usage undergoes testing yet. Check repo in few days for update.')

	# 2. Woah.
	elif sys.platform == 'woah':
		pass

	# 3. Linux.
	else:

		# Change keys / create new keys for all servers stated correctly in ~/.ssh/config file.
		if len(sys.argv) == 2:
			ssh_config = '~/.ssh/config'
			if '/' in sys.argv[2]:
				ssh_config = sys.argv[2]
			KM = KeyMaker(ssh_config)
			KM.change_server_keys()
		
		# Create 1 new key pair:
		if len(sys.argv) == 3:
			ip_adress = sys.argv[1]
			server_user = sys.argv[2]
			ssh_config = '~/.ssh/config'
			KM = KeyMaker(ssh_config)
			KM.create_server_keys(server_user=server_user, ip_adress=ip_adress)
		else:
			ssh_config = '~/.ssh/config'
			KM = KeyMaker(ssh_config)
			KM.create_server_keys_frominput(self)



