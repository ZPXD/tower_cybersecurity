import os
from datetime import datetime
import sys


'''
Backups.


Each time you run the script it creates backup ZIP folder in 
/home/<user>/<backup_folder_name> folder

with content of:
- all folders in backup_folders
- all files defined in backup_files
- all settings defined in backup_settings [TBD]
- all packages defined by backup_packages [TBD]

Use second part of this script to download files to copmuter or make reconquista.

In development:
- encryption
- comparing versions in case of code injection
- anti-malware file analysis by pychecker & others
- more


ZPXD, Łukasz Pintal.
'''



class Backup():

	# Backup folder.
	backup_folder_name = 'kopia_zapasowa'
	backup_base = '/home/{}/{}' # /home/<user>/<backup_folder_name>

	# Commands.
	backup_folder_command = 'cp -r {} {}'
	backup_file_command = 'cp {} {}'

	# Resources.
	backup_folders = [
		'/var/www',
		'/home/{}',
		'/etc/systemd/system',
		'/etc/nginx/',
		'/root',
		'/etc/sudoers',
		'/etc/ssh/sshd_config',
	]

	backup_files = [
	]

	backup_settings = [
	]

	backup_packages = [
	]


	def __init__(self):
		self.server_user = os.getlogin()

	def install_prequisites(self):
		# if exists, dont install
		os.system('sudo apt install zip')

	def prepare_content_to_be_saved(self):
		temp_folders = []
		for folder in self.backup_folders:
			if '/home/{}' in folder:
				folder.format(self.server_user)
			temp_folders.append(folder)
		self.backup_folders = temp_folders
		temp_files = []
		for file in self.backup_files:
			if '/home/{}' in file:
				folder.format(self.server_user)
			temp_files.append(folder)
		self.backup_files = temp_files

	def date(self):
		'''

		'''
		date_obj = datetime.today()
		date_text = date_obj.strftime('%Y-%m-%d-%H-%M-%S')
		return date_text

	def get_paths(self):
		'''
		'''

		# MAIN FOLDERS.
		self.home_folder = '/home/{}'.format(self.server_user)
		self.backup_base = self.backup_base.format(self.server_user, self.backup_folder_name)
		self.backup_history = self.backup_base + '/' + 'historia'
		
		# THIS BACKUP - TO BECOME.
		self.this_backup = self.backup_base + '/' + 'nowy' + '_' + self.date()
		self.this_backup_name = self.this_backup.split('/')[-1]

		self.create_backup_folders()

		# LAST BACKUPS.
		newest_backup = [f for f in os.listdir(self.backup_base) if f.startswith('nowy')]
		if newest_backup:
			self.newest_backup = self.backup_base + '/' + newest_backup[0]
			self.newest_backup_name = newest_backup[0]
		else:
			self.newest_backup = ''
			self.newest_backup_name = ''

		next_backup = [f for f in os.listdir(self.backup_base) if f.startswith('kolejny')]
		if next_backup:
			self.next_backup = self.backup_base + '/' + next_backup[0]
			self.next_backup_name = next_backup[0]
		else:
			self.next_backup = ''
			self.next_backup_name = ''


	def create_backup_folders(self):
		'''
		'''
		if not self.backup_folder_name in os.listdir(self.home_folder):
			os.mkdir(self.backup_base)
		if not 'historia' in os.listdir(self.backup_base):
			os.mkdir(self.backup_history)

	def make_backups(self):
		'''
		'''
		os.mkdir(self.this_backup)
		for folder in self.backup_folders:
			if 'home/{}' in folder:
				folder = folder.format(self.server_user)
			try:
				base = self.this_backup + '/' + folder.split('/')[-1]
				backup_command = self.backup_folder_command.format(folder, base)
				print(backup_command)
				os.system(backup_command)
			except Exception as e:
				print(e)
		for file in self.backup_files:
			if 'home/{}' in folder:
				folder = folder.format(self.server_user)
			try:
				base = self.this_backup + '/' + file.split('/')[-1]
				backup_command = self.backup_file_command.format(file, base)
				os.system(backup_command)
			except Exception as e:
				print(e)

	def move(self):
		'''
		'''
		# Save last backup to history.
		if self.next_backup_name in os.listdir(self.backup_base):
			archive_name = self.next_backup.replace('kolejny_', '')
			rename_command = 'mv {} {}'.format(self.next_backup, archive_name)
			os.system(rename_command)
			move_command = 'mv {} {}'.format(archive_name, self.backup_history)
			os.system(move_command)

		# Save newest backup file as a next backup file.
		if self.newest_backup_name in os.listdir(self.backup_base):
			save_path = self.newest_backup.replace('nowy', 'kolejny')
			move_command = 'mv {} {}'.format(self.newest_backup, save_path)
			os.system(move_command)

	def compare_backups(self):
		'''
		'''

	def zip_folder(self, folder=None, zip_as=None):
		'''
		'''
		if folder and zip_as:
			zip_command = 'zip {} {}'.format(zip_as, folder)
		else:
			zip_command = 'zip {} {}'.format(self.this_backup+'.zip', self.this_backup)
		os.system(zip_command)

		rm_command = 'rm -r {}'.format(self.this_backup)
		os.system(rm_command)

	def send(self, login=None, ip=None, key_contents=None, port=None):
		pass
		
	def now(self):
		'''
		'''
		self.get_paths()
		self.prepare_content_to_be_saved()
		self.move()
		self.make_backups()
		self.install_prequisites()
		self.zip_folder()


if __name__ == '__main__':

	if len(sys.argv) > 1:
		if '-l' in sys.argv:
			i = sys.argv.index('-l')
			login = sys.argv[i+1]
		if '-ip' in sys.argv:
			i = sys.argv.index('-ip')
			ip = sys.argv[i+1]
		if '-key' in sys.argv:
			i = sys.argv.index('-key')
			key = sys.argv[i+1]
			key_contents = open(key).read()
		if '-p' in sys.argv:
			i = sys.argv.index('-p')
			port = sys.argv[i+1] 

		#print(login, ip, key_contents, port)
		backup = Backup()
		backup.send(login, ip, key_contents, port)
	else:
		backup = Backup()
		backup.now()
