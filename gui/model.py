# model.py
import os
import sys
import json
import shutil

# Load PySide
try:
	from PySide2.QtWidgets import QPushButton

except ImportError:
	from PySide.QtGui import QPushButton

'''
NOTE:
Repository configurations are comprised of the following elements:

 - url 		: The URL to the repository.
 - match-url: An alternative URL used when matching incoming webhook requests (see https://github.com/olipo186/Git-Auto-Deploy/pull/148) 
 - branch 	: The branch which will be checked out.
 - remote 	: The name of the remote to use.
 - path 	: Path to clone the repository to. If omitted, the repository won't be cloned, only the deploy scripts will be executed.
 - deploy 	: A command to be executed. If `path` is set, the command is executed after a successfull `pull`.
 - payload-filter: A list of inclusive filters/rules that is applied to the request body of incoming web hook requests and determines whether the deploy command should be executed or not. See section *Filters* for more details.
 - header-filter: A set of inclusive filters/rules that is applied to the request header of incoming web hook requests and determines whether the deploy command should be executed or not. See section *Filters* for more details.
 - secret-token : The secret token set for your webhook (currently only implemented for [GitHub](https://developer.github.com/webhooks/securing/) and GitLab)
 - prepull 		: A command to execute immediately before the `git pull`.  This command could do something required for the ``git pull`` to succeed such as changing file permissions. 
 - postpull 	: A command to execute immediately after the `git pull`.  After the **prepull** command is executed, **postpull** can clean up any changes made.
'''

class Repository (object):

	repo_name		= str()
	url				= str()
	local_path		= str()
	current_branch	= str()
	last_commit		= str()
	filters			= None
	match_url		= str()
	deploy_cmd		= str()
	filters_button  = None

	def __init__(self, repodata = None, parent = None):

		if not repodata :
			repodata = {}

		if repodata.has_key( 'url' ) :
			self.url 		= repodata['url']

		if repodata.has_key( 'match-url' ) :
			self.match_url 	= repodata['match-url']

		if repodata.has_key( 'branch' ) :
			self.branch 	= repodata['branch']

		if repodata.has_key( 'remote' ) :
			self.remote 	= repodata['remote']

		if repodata.has_key( 'path' ) :
			self.local_path = repodata['path']
			self.repo_name  = os.path.basename(repodata['path'])

		if repodata.has_key( 'deploy' ) :
			self.deploy_cmd = repodata['deploy']

		if repodata.has_key( 'payload-filter' ) :
			self.payload_filter = repodata['payload-filter']

		if repodata.has_key( 'header-filter' ) :
			self.header_filter = repodata['header-filter']

		if repodata.has_key( 'secret-token' ) :
			self.token 		= repodata['secret-token']

		if repodata.has_key( 'prepull' ) :
			self.prepull_cmd = repodata['prepull']

		if repodata.has_key( 'postpull' ) :
			self.postpull_cmd = repodata['postpull']

		if repodata.has_key('filters'):
			self.filters = repodata['filters']

		self.filters_button = QPushButton("Edit filters", parent)
		self.filters_button.setEnabled(False)

		self.last_commit 	= self.__get_Lastcommit_in_local(local_path = self.local_path)
		self.current_branch = self.__get_current_branch_in_local(local_path = self.local_path)
		self.filters_button	= self.__create_filter_button_from_repodata(button = self.filters_button, parent = parent) 

	def __get_Lastcommit_in_local(self, local_path):
		
		if not os.path.exists(local_path):
			return 'null'

	def __get_current_branch_in_local(self, local_path):

		if not os.path.exists(local_path):
			return 'null'\

	def edit_filters_PushButton_onClick(self):

		print ('Edit Filters Clicked : ' + self.repo_name)

	def __create_filter_button_from_repodata(self, button, parent):
		'''
		arg :
			filters : (json)
		return :
			button  : button object (QtGui.QPushButton)
		'''

		button.setEnabled(True)

		return button