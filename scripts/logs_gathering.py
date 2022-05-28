import os
import json
import time
import string
import subprocess
import pandas as pd
from dateutil import parser

'''
Gathers all logs into one place.

To be developed:
- unifying log history into one log
- unifying multiple logs
- more logs, places
- meta
- time intervals
- dedicated parsers for each log
- scripts for log content change vulnerability

ZPXD, Łukasz Pintal.
'''


logs_gathering = {

	'file_logs' : {
		
		# 'apt_history' : {'path' : '/var/log/apt/history.log', },
		# 'apt_term' : 	{'path' : '/var/log/apt/term.log',},
		# 'apt_eipp' : 	{'path' : '/var/log/apt/eipp.log',},
		# 'auth' : 		{'path' : '/var/log/auth.log',},
		# 'btmt' : 		{'path' : '/var/log/btmt',},
		# 'dmesgs' :	 	{'path' : '/var/log/dmesgs',},
		# 'lastlog' : 	{'path' : '/var/log/lastlog',},
		#'syslog' : 		{'path' : '/var/log/syslog',},
		'check' : 		{'path' : '/home/lukasz/logs_test/level2',},
		# 'dmesg' : 		{'path' : '/var/log/dmesg',},
		# 'nginx_access': {'path' : '/var/log/nginx/access.log',},
		# 'apt_history' : {'path' : '/var/log/apt/history.log', },
		# 'apt_term' : 	  {'path' : '/var/log/apt/term.log',},
		# 'apt_eipp' : 	  {'path' : '/var/log/apt/eipp.log',},
		# 'auth' : 		  {'path' : '/var/log/auth.log',},
		# 'btmt' : 		  {'path' : '/var/log/btmt',},
		# 'dmesgs' :	  {'path' : '/var/log/dmesgs',},
		# 'lastlog' : 	  {'path' : '/var/log/lastlog',},
		'syslog' : 	  {'path' : '/var/log/syslog',},
		# 'check' : 	  {'path' : '/home/lukasz/logs_test/level2'},
		# 'dmesg' : 		{'path' : '/var/log/dmesg',},
		'nginx_access': {'path' : '/var/log/nginx/access.log',},
		# 'nginx_error' : {'path' : '/var/log/nginx/error.log',},
		# 'exim4' : 		{'path' : '/var/log/exim4/mainlog',},
		# TBD ...
	},

	'command_logs' : {

		'history' : 	 {'command' : 'history', },
		'top' : 		 {'command' : 'top -b -n 1', },
		'who' : 		 {'command' : 'who', },
		'last_wtmp' : 	 {'command' : 'last -f /var/log/wtmp', },
		'last' : 		 {'command' : 'last', },
		'lastb' : 		 {'command' : 'lastb', },
		'utmp' : 		 {'command' : 'utmpdump /var/run/utmp', },
		# TBD ...
	},
	
	'log_places' : [
		'/var/log',
		'/var/run',
	],

	'files_to_watch' : {
		#'item' : 		{'path' : '/path/to'},s
		
	},

	'folders_to_watch' : {
		#'item' : 		{'path' : '/path/to'},
	},

	'files_in_folders_to_watch' : {
		#'item' : 		{'path' : '/path/to'},
	},

	'folders_to_watch' : {
		#'item' : 		{'path' : '/path/to'},
	},

	'files_in_folders_to_watch' : {
		#'item' : 		{'path' : '/path/to'},
	},

	'meta' : {
		'',
		'',
		'',
	},
}

# Watcher blueprint.
file_watcher = '''
import sys
import os
import threading
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from logs_gathering import LogsGathering

def i_see_my_files(file_path, name):
	LOG = LogsGathering()
	yeah_echo = 0
	if os.path.exists(file_path):
		yeah = os.stat(file_path).st_mtime
		if yeah_echo != yeah:
			yeah_echo = yeah
			LOG.do(name, file_path)
		else:
			os.system('rm {}/{}_guardian.py'.format(LOG.guardians_folder_path, name))
			try:
				pid = str(open(file_path).readlines()[-1][1:])
				os.system('rm {}/{}_guardian.py'.format(LOG.guardians_folder_path, name))
				os.system('kill -9 {}'.format(pid))
			except:
				pass

'''

file_watcher_reviver = '''
import sys
import os
import threading
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from logs_gathering import LogsGathering

def guardians():
	while True:
		from logs_gathering import LogsGathering
		LOG = LogsGathering()
		LOG.things_to_watch_list()
		for name, file_path in LOG.things_to_watch.items():
			file_path = file_path['path']
			guardian_path = LOG.guardians_folder_path + '/' + name + '_guardian.py' 
			if os.path.exists(file_path) and not os.path.exists(guardian_path):
				LOG.create_guardian(name, file_path)

centurion = threading.Thread(target=guardians)
centurion.start()
'''

# Guardian blueprint.
template = '''
guardian = threading.Thread(target=i_see_my_files, args=['{}', '{}'])
guardian.start()
'''

class LogsGathering():

	place_for_logs_folder = '/home/{}'
	logs_gathering_file = 'logs_gathering.json'
	logs_folder = 'logs_gathering'

	guardians_folder = 'guardians'
	i_see_my_files = 'i_see_my_files.py'
	guardians_revive = 'guardians_revive.py'
	
	def __init__(self, logs_gathering=None):
		self.place_for_logs_folder = self.place_for_logs_folder.format(os.getlogin())
		self.logs_folder_path = self.place_for_logs_folder + '/' + self.logs_folder
		self.guardians_folder_path = self.logs_folder_path + '/' + self.guardians_folder
		self.logs_gathering_file_path = self.logs_folder_path + '/' + self.logs_gathering_file
		self.logs_gathering = logs_gathering
		self.things_to_watch = None

	
	# Preperation.

	def install_prequisites(self):
		'''
		Install prequisites & prepare files.
		'''
		pass

	def prepare_files_and_commands(self):
		'''
		Prepares logs to be scrapped.
		
		To potem.
		'''
		#os.system('sudo unxz /var/log/apt/eipp.log.xz') # Unpacks eipp log into readable format.
		#os.system('export HISTTIMEFORMAT="%F %T" ""') # Adds datestamp to 'history' command.

	def prepare_places(self):
		'''
		Prepare place for logs (folders).
		'''
		if not self.logs_folder in os.listdir(self.place_for_logs_folder):
			os.mkdir(self.logs_folder_path)
		log_folders = os.listdir(self.logs_folder_path)
		if not 'guardians' in log_folders:
			os.mkdir(self.guardians_folder_path)
		for k, v in self.logs_gathering['file_logs'].items():
			if not k in log_folders:
				save_path = os.path.join(self.logs_folder_path, k)
				os.mkdir(save_path)
				save_path = os.path.join(self.logs_folder_path, k, 'history')
				os.mkdir(save_path)
		for k, v in self.logs_gathering['command_logs'].items():
			if not k in log_folders:
				save_path = os.path.join(self.logs_folder_path, k)
				os.mkdir(save_path)
				save_path = os.path.join(self.logs_folder_path, k, 'history')
				os.mkdir(save_path)
				
	def things_to_watch_list(self):
		self.things_to_watch =  dict(logs_gathering['file_logs'], **logs_gathering['files_to_watch'], **logs_gathering['folders_to_watch'], **logs_gathering['files_in_folders_to_watch'])
		

	def things_to_watch_list(self):
		self.things_to_watch = {}
		for k, v in logs_gathering['file_logs'].items():
			self.things_to_watch[k] = v
		for k, v in logs_gathering['files_to_watch'].items():
			self.things_to_watch[k] = v
		for k, v in logs_gathering['folders_to_watch'].items():
			self.things_to_watch[k] = v
		for k, v in logs_gathering['files_in_folders_to_watch'].items():
			folder_path = v['path']
			folder_files = self.get_all_folder_files(folder_path)
			for f in folder_files:
				file_name = f.split('/')[-1].split('.')[0]
				if os.path.exists(f):
					self.things_to_watch[file_name] = {'path': f}
				else:
					pid = str(open(f).readlines()[-1][1:])
					os.system('rm {}/{}_guardian.py'.format(LOG.guardians_folder_path, file_name))
					os.system('kill -9 {}'.format(pid))

	# Config.

	# 1. Load.
	# 2. Save.
	# 3. Research: look for logs.

	def load_logs_gathering_config_from_file(self, config_path=None):
		'''
		Load from JSON, if not exists load from here.
		'''
		if not config_path:
			config_path = self.logs_gathering_file_path
		with open(config_path, 'r') as fp:
			self.logs_gathering = json.loads(fp.read())

	def save_logs_gathering_config_with_new_results(self):
		'''
		Save logs_gathering to JSON file..
		'''
		with open(self.logs_gathering_file_path, 'w') as fp:
			json.dump(self.logs_gathering, fp)

	def search_add_new_logs(self, ask=True):
		'''
		Searches for log files.

		Adds them to logs_gathering config file if you decide so.

		ask: bool: default True, asks before adding log to config.
		'''
		new_logs = []
		existing_log_paths = []
		for k, v in self.logs_gathering['file_logs'].items():
			existing_log_paths.append((v['path']))
		for place in self.logs_gathering['log_places']:
			logs_paths = self.get_all_folder_files(place, 'log')
			for log_path in logs_paths: # :)
				if log_path not in existing_log_paths:
					if not log_path.endswith('gz') and not log_path[-1].isdigit():
						name = log_path.split('.')[0]
						new_logs.append((name, log_path))

		print('Found {} new log files:'.format(len(new_logs)))
		for name, log_path in new_logs:
			print(name, "-", log_path)
			if ask:
				decide = input('Press y to add log.').lower()
				if decide == 'y':
					logs_gathering['file_logs'][name] = {'path' : log_path}
			else:
				logs_gathering['file_logs'][name] = {'path' : log_path}

	# Helpers.
	# 1. Date.
	# 2. Get all folder files with log in name.
	# 3. Make a command and get output.

	def date(self):
		'''
		Create date as a str.
		'''
		date_obj = datetime.today()
		date_text = date_obj.strftime('%Y-%m-%d-%H-%M-%S')
		return date_text

	def get_all_folder_files(self, folder_path, condition=None):
		'''
		Returns list of all file paths from given folder that fulfill the condition.

		folder_path: str: path of a folder you want to search.
		condition: ['str', 'str', 'str'] or 'str': what you look for in a file name.
		'''
		new_folders = [folder_path]
		new_files = []
		for folder_path in new_folders:
			for folder, folders_in, files_in in os.walk(folder_path, topdown=True):
				for folder_in in folders_in:
					full_folder_path = folder_path + '/' + folder_in
					if full_folder_path not in new_folders:
						new_folders.append(full_folder_path)

				for file in files_in:
					if condition:
						if isinstance(condition, list):
							for c in condition:
								if c in file:
									file_path = folder + '/' + file
									if not file_path in new_files:
										new_files.append(file_path)
						else:
							if condition in file:
								file_path = folder + '/' + file
								if not file_path in new_files:
									new_files.append(file_path)
					else:
						file_path = folder + '/' + file
						if not file_path in new_files:
							new_files.append(file_path)
		return new_files

	def command_with_output(self, command):
	    command = command.split()
	    ok = subprocess.sPopen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	    output = ok.communicate()[0]
	    return output

	# Gathering logs:
	# 1. Gather 1
	# 2. Gather ALL
	# 3. Vulnerability

	def quick_log_gatherer(self, name, full_path):
		'''
		Save 1 log - quick unaccurate method saves log to log history folder.
		'''
		file_name = date()
		if not name in os.listdir(self.logs_folder_path):
			mkdir(os.path.join(self.logs_folder_path, name))
		save_as = os.path.join(self.logs_folder_path, name, 'history', file_name)
		command = 'cat {} > {}'.format(log['path'], save_as)
		os.system(command)

	def quick_logs_gatherer(self):
		'''
		Save ALL logs - quick unaccurate method to gather all logs to history folders.
		'''
		for name, log in self.logs_gathering['command_logs'].items():
			file_name = self.date()
			save_as = os.path.join(self.logs_folder_path, 'history', file_name)
			command = '{} > {}'.format(log['command'], save_as)
			os.system(command)

		for name, log in self.logs_gathering['file_logs'].items():
			file_name = self.date()
			save_as = os.path.join(self.logs_folder_path, name, 'history', file_name)
			command = 'cat {} > {}'.format(log['path'], save_as)
			os.system(command)

	def do(self, file_name, path):
		'''
		.
		'''
		check_name = 'checkcheckcheck.txt'
		check = self.logs_folder_path + '/' + check_name
		if check in os.listdir():
			with open(check, 'w+') as f:
				f.write(self.date())
		else:
			with open(check, 'a+') as f:
				f.write(self.date())

	def syslog(self):
		'''
		.
		'''
		df_path = '/home/lukasz/logs_gathering/syslog/syslog.csv'
		columns = ['date', 'program', 'runner', 'info']
		if not os.path.exists(df_path):
			log = open('/var/log/syslog').readlines()
			data = []
			for line in log:
				elements = line.split()
				date_string = ' '.join(elements[:3])
				date = parser.parse(date_string)
				data_row = {
					'date' : date,
					'program' : elements[3],
					'runner' : elements[4],
					'info' : ' '.join(elements[5:]),
				}
				data.append(data_row)
			df = pd.DataFrame(data, columns=columns)
			df = df.loc[:len(df)-2, :]
			df.to_csv(df_path, index=False)
		else:
			df = pd.read_csv(df_path)
			last_date = df.loc[len(df)-1, 'date']
			last_date = parser.parse(date_string)
			log = open('/var/log/syslog').readlines()
			data = []
			for line in log[::-1]:
				elements = line.split()
				date_string = ' '.join(elements[:3])
				date = syslog_date_to_timestamp(date_string)
				if date > last_date:
					data_row = {
						'date' : date,
						'program' : elements[3],
						'runner' : elements[4],
						'info' : ''.join(elements[5:]),
					}
					data.append(data_row)
			df2 = pd.DataFrame(data, columns=columns)
			df = pd.concat([df, df2], axis=0, ignore_index=True)
			df.to_csv(df_path, index=False)

	def do(self, log_name, path):
		'''
		.
		'''
		if log_name == 'syslog':
			self.syslog()



		# TEMP CHECKER.
		check_name = 'checkcheckcheck.txt'
		check = self.logs_folder_path + '/' + check_name
		string = '{:20} - {}\n'.format(log_name, self.date())
		if check in os.listdir():
			with open(check, 'w+') as f:
				f.write(string)
		else:
			with open(check, 'a+') as f:
				f.write(string)

	def create_guardians(self):
		for name, info in logs_gathering['file_logs'].items():
			self.create_guardian(name, info['path'])

	def create_guardian(self, name, file_path):
		if os.path.exists(file_path):
			script = file_watcher + template.format(file_path, name)
			file_path = self.guardians_folder_path + '/' + name + '_guardian.py'
			with open(file_path, 'w') as f:
				f.write(script)
			time.sleep(0.1)
			os.system('python3 {}'.format(file_path))
			time.sleep(0.1)
			command = 'python3 {}'.format(file_path)
			p = subprocess.Popen(command.split())
			pid = p.pid
			time.sleep(0.1)
			with open(file_path, 'a+') as f:
				f.write('#{}'.format(pid))

	def create_reviver(self):
		'''
		Create watcher file, starts it 
		and removes last one (active) after 1 second.
		'''
		reviver_path = self.guardians_folder_path + '/' + self.guardians_revive
		with open(reviver_path, 'w') as f:
			f.write(file_watcher_reviver)
		time.sleep(0.1)
		os.system('python3 {}'.format(reviver_path))
		time.sleep(0.1)
		command = 'python3 {}'.format(reviver_path)
		p = subprocess.Popen(command.split())
		pid = p.pid


	def run_script_on_background(self, script_path, arg_str=''):
		'''
		.
		'''
		command = 'sudo python3 {} {} &'
		command = command.format(script_path, arg_str)
		os.system(command)
		return command

	def ongoing_bash(self, script_path, every_n_seconds=1, arg_str=''):
		'''
		.
		'''
		command = 'sudo watch -n {} sudo python3 {} {}'
		command = command.format(every_n_seconds, script_path, arg_str)
		os.system(command)
		return command

	def make_autostart(self):
		'''
		.
		'''
		pass
		
	def make_autostart(self, name, command, info):
		'''
		Create autostart for command.
		'''
		file_name = '{}.service'.format(name)
		folder = '/etc/systemd/system/'
		path = folder + file_name
		template = '''
		[Unit]
		Description={}

		[Service]
		ExecStart={}

		RemainAfterExit=yes

		[Install]
		WantedBy=multi-user.target
		'''
		if not file_name in os.listdir(folder):
			contents = template.format(info, command)
			with open(path, 'w') as autostart:
				autostart.write(contents)
			os.system('sudo systemctl daemon-reload')
			os.system('sudo systemctl enable {}'.format(file_name))

# To do.
# - history/history
# - dla guardianow - sprawdzanie procesow po usunieciu pliku jeszcze


if __name__ == "__main__":
	LOG = LogsGathering(logs_gathering)

	LOG.install_prequisites()
	LOG.prepare_files_and_commands()
	LOG.prepare_places()

	# Żyjący program robimy, bez default configa
	#LOG.load_logs_gathering_config_from_file()
	#LOG.search_add_new_logs(ask=True) # ...
	#LOG.quick_logs_gatherer()

	# Guardians:
	LOG.things_to_watch_list()
	LOG.create_guardians()
	LOG.create_reviver()
	print(LOG.things_to_watch)
