import os
import sys
import platform
import time
from paramiko import SSHConfig, SSHClient
from datetime import datetime
import subprocess
import socket



'''
Backups.

First usecases:
1. linux to linux with connection by a key for all servers.
2. linux to linux with connection by a key for one server.
3. linux to linux with connection by a ip, login for one server.

For now for windows use in powershell:
 scp -i <your-key> <login>@<ip>:/home/{}/kopia_zapasowa/nowy* backup



Script will be developed.

ZPXD, Łukasz Pintal.
'''


class GetBackups():

	download_what = '/home/{}/kopia_zapasowa/nowy*'
	download_where = '/home/{}/kopie_zapasowe/{}/'

	# Paths.
	backup_folder_name = 'kopie_zapasowe'
	backup_folder_path = '/home/{}/kopie_zapasowe'
	home_folder = '/home/{}'

	# SSH
	ssh_config = '/home/{}/.ssh/config'
	ssh_key = '/home/{}/.ssh/{}'

	# Path & command templates.
	download_folder_command = '''scp -i {} {}@{}:{} {}'''
	carry_folder_command = '''scp -i {} {}@{}:{} {}'''
	

	def __init__(self):
		self.computer_user = os.getlogin()

	def create_folders(self):
		if not self.backup_folder_name in os.listdir(self.home_folder):
			os.mkdir(self.backup_folder_path)

	def create_paths(self):
		self.ssh_config = self.ssh_config.format(self.computer_user)
		self.home_folder = self.home_folder.format(self.computer_user)
		self.backup_folder_path = self.backup_folder_path.format(self.computer_user)
		self.download_what = self.download_what.format(self.computer_user)

	def date(self):
		date_obj = datetime.today()
		date_text = date_obj.strftime('%Y-%m-%d')
		return date_text
		
	def reconquista_linux_to_linux(self):
		pass

	def read_config(self, other_config):
		self.config = SSHConfig()
		if other_config:
			self.config.parse(open(other_config))
		else:
			config_file = self.ssh_config.format(self.computer_user)
			self.config.parse(open(config_file))

	def data_from_config(self, host):
		try:
			server_ssh_auth = self.config.lookup(host)
			server_ip = server_ssh_auth['hostname']
			server_user = server_ssh_auth['user']
			server_key = self.ssh_key.format(self.computer_user, server_ssh_auth['identityfile'][0])
			return server_key, server_user, server_ip
		except:
			return None, None, None

	def backup_folder(self, server_key, server_user, server_ip, folder, download_where):
		download_folder_command = self.download_folder_command.format(
			server_key,
			server_user,
			server_ip,
			folder,
			download_where,
		)
		try:
			try:
				os.mkdir(download_where)
			except:
				pass
			os.system(download_folder_command)
		except Exception as e:
			print('something wrong:', e)

	def backup_linux_to_linux(self, download_what=None, download_where=None, server_key=None, server_ip=None, server_user=None, other_config=None, hostname=None):
		'''
		'''
		self.create_paths()
		self.create_folders()
		self.read_config(other_config)

		if not download_what:
			download_what = self.download_what
		
		# 1. Back up 1 server by a HOST name.

		if hostname:

			# Get ssh connection informations.
			server_key, server_user, server_ip = self.data_from_config(hostname)
			if server_key and server_user and server_ip:

				if not download_where:
					server_ip_str = server_ip.replace('.', '_')
					download_where = self.download_where.format(self.computer_user, server_ip_str)
					if not server_ip in os.listdir(self.backup_folder_path):
						os.mkdir(download_where)
					
				# Prepare and run download commands.

				print('Starting download for: {}\n'.format(server_ip))
				self.backup_folder(server_key, server_user, server_ip, download_what, download_where)
		

		# 2. Back up 1 server by Login & IP and server key.

		elif server_key and server_user and server_ip:
			if not '/' in server_key:
				server_key = self.ssh_key.format(self.computer_user, server_key)
			if not download_where:
				server_ip_str = server_ip.replace('.', '_')
				download_where = self.download_where.format(self.computer_user, server_ip_str)
			
			# Prepare and run download commands.
			print('\n\n\nStarting download for: {}\n'.format(server_ip))
			self.backup_folder(server_key, server_user, server_ip, download_what, download_where)


		# 3. Back up ALL servers in given Config without stating anything.

		else:

			# Get ssh connection informations.
			self.read_config(other_config)

			hostnames = self.config.get_hostnames()
			for host in hostnames:
				print('\n\n--{}'.format(host))

				# Get ssh connection informations.
				server_key, server_user, server_ip = self.data_from_config(host)
				if server_key and server_user and server_ip:
					
					# Prepare and run download commands.
					print('\n\n\nStarting download for: {}\n'.format(server_ip))
					if not download_where:
						server_ip_str = server_ip.replace('.', '_')
						download_where = self.download_where.format(self.computer_user, server_ip_str)
					self.backup_folder(server_key, server_user, server_ip, download_what, download_where)


if __name__ == '__main__':
	Up = GetBackups()
	Up.backup_linux_to_linux(server_key='key_lukasz2', server_user='lukasz', server_ip='46.41.148.153')
