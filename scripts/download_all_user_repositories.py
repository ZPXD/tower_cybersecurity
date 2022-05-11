import os
import requests
import sys



'''
Backup Your GitHub.


Script downloads all public repositories from github to folder you specify.

Do not hesitate to follow up with:
- check code against any destructive/toxic methods
- check code against any data/content manipulation
- copy code to other devices like protected, properly scanned pendrive
- multiple layers of distributed encryption/decryption with generators

<3 stay strong


ZPXD, Łukasz Pintal.
'''



def download_all_github_repositories(github_user=None, backup_folder_name='backup'):
	
	# Enter GitHub user name. 
	if github_user == None:
		github_user = input("Enter the github username:")
	
	# Download user GitHub repositories info as a json.
	request = requests.get('https://api.github.com/users/'+github_user+'/repos')
	json = request.json()

	# Download user GitHub repositories contents.
	for i in range(0,len(json)):
		repo_url = json[i]['svn_url'] + '.git'
		repo_name = json[i]['name']
		os.system('git clone {} {}/{}'.format(repo_url, backup_folder_name, repo_name))

	# Info.
	print('{} repositories downloaded into: {}'.format(i, )



if __name__ == '__main__':
	download_all_github_repositories(*sys.argv[1:])