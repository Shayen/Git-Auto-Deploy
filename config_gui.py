# main GUI file
import os
import sys
import json
import shutil

# Load PySide
try:
	from PySide2.QtCore import *
	from PySide2.QtGui import *
	from PySide2.QtWidgets import *
	from PySide2.QtUiTools import *
	from PySide2 import __version__

except ImportError:
	from PySide.QtCore import *
	from PySide.QtGui import *
	from PySide.QtUiTools import *
	from PySide import __version__

__app_version__ = '0.1.0 Alpha'
# v0.1.0 alpha : init tool

'''
TODO : 
[X] Load UI from file
[X] Read config.json
[X] Link config.json to main GUI
[ ] Create/Update config.json via GUI
[ ] Run as service/stop service via GUI
[ ] Check running service (require to run via window service)
'''

class GAD_PreferenceUI( QMainWindow ):
	
	CONFIG_PATH = 'config.json'
	CONFIG = {}

	def __init__(self, parent=None):
		""" Description """
		QMainWindow.__init__(self, parent)

		_uiFilename_ = 'gitautodeploy_ui.ui'
		_uiFilePath_ = 'gui/' + _uiFilename_		

		# Check is ui file exists?
		if not os.path.isfile( _uiFilePath_ ):
			print("UI file not exists : " + _uiFilePath_ )
			return

		# ---- LoadUI -----
		loader = QUiLoader()
		currentDir = os.path.dirname(__file__)
		file = QFile( _uiFilePath_ )
		file.open(QFile.ReadOnly)
		self.ui = loader.load(file, parentWidget=self)
		file.close()
		# -----------------

		self.ui.setWindowTitle('Git-auto-deploy preference v.' + str(__app_version__))

		# Load config
		self.CONFIG = self.loadConfig("config.json")

		self._initUI()
		self._initConnect()

		self.ui.show()

	def _initUI(self):

		# Http
		self.ui.lineEdit_http_host.setText(self.CONFIG['http-host'])
		self.ui.lineEdit_http_port.setText(str(self.CONFIG['http-port']))
		self.ui.checkBox_http_enable.setCheckState(Qt.Checked if self.CONFIG['http-enabled']else Qt.Unchecked)

		# Https
		self.ui.lineEdit_https_host.setText(self.CONFIG['https-host'])
		self.ui.lineEdit_https_port.setText(str(self.CONFIG['https-port']))
		self.ui.checkBox_https_enable.setCheckState(Qt.Checked if self.CONFIG['https-enabled']else Qt.Unchecked)

		# common
		self.ui.lineEdit_pid_filepath.setText(self.CONFIG['pid-file'])
		self.ui.checkBox_daemon_mode_active.setCheckState(Qt.Checked if self.CONFIG['daemon-mode']else Qt.Unchecked)
		self.ui.lineEdit_log_filepath.setText(self.CONFIG['log-file'])
		level_indx = self.ui.comboBox_log_level.findText(self.CONFIG['log-level'], Qt.MatchExactly )
		self.ui.comboBox_log_level.setCurrentIndex(level_indx)

		# Pre-post deployscript
		# self.ui.lineEdit_predeploy_script.setText(self.CONFIG[''])
		# self.ui.lineEdit_postdeploy_script.setText(self.CONFIG[''])

		# Webui
		self.ui.checkBox_enable_webui.setCheckState(Qt.Checked if self.CONFIG['web-ui-enabled']else Qt.Unchecked)
		self.ui.checkBox_enable_webui_auth.setCheckState(Qt.Checked if self.CONFIG['web-ui-auth-enabled']else Qt.Unchecked)
		self.ui.checkBox_enable_webui_https.setCheckState(Qt.Checked if self.CONFIG['web-ui-require-https']else Qt.Unchecked)
		# Web-ui white list
		self.ui.listWidget_webui_whitelist.addItems(self.CONFIG['web-ui-whitelist'])
		# Web-UI Auth
		self.ui.lineEdit_webui_auth_username.setText(self.CONFIG['web-ui-username'])
		self.ui.lineEdit_webui_auth_password.setText(self.CONFIG['web-ui-password'])
		# SSL cert
		self.ui.lineEdit_sll_key_path.setText(str(self.CONFIG['ssl-key']))
		self.ui.lineEdit_sll_cert_path.setText(self.CONFIG['ssl-cert'])

	def _initConnect(self):
		pass

	def init_config(self, config):
		"""Initialize config by filling out missing values etc."""

		import os

		# Translate any ~ in the path into /home/<user>
		if 'pid-file' in config and config['pid-file']:
			config['pid-file'] = os.path.expanduser(config['pid-file']).replace('\\', '/')

		if 'log-file' in config and config['log-file']:
			config['log-file'] = os.path.expanduser(config['log-file']).replace('\\', '/')

		if 'ssl-cert' in config and config['ssl-cert']:
			config['ssl-cert'] = os.path.expanduser(config['ssl-cert']).replace('\\', '/')

		if 'ssl-key' in config and config['ssl-key']:
			config['ssl-key'] = os.path.expanduser(config['ssl-key']).replace('\\', '/')

		if 'repositories' not in config:
			config['repositories'] = []

		return config

	def loadConfig(self, config_file_path):
		'''
		Input : 
			filepath : Full path to json file
		Output :
			return : dictionary of config
		'''

		from gitautodeploy.cli.config import get_config_defaults, get_config_from_environment, get_config_from_file, rename_legacy_attribute_names
		from gitautodeploy.cli.config import ConfigFileNotFoundException, ConfigFileInvalidException

		# Get default config values
		config = get_config_defaults()

		# Config file path provided or found?
		if os.path.exists(config_file_path):

			try:
				file_config = get_config_from_file(config_file_path)
			except ConfigFileNotFoundException as e:
				print("No config file not found at '%s'" % e)
				return
			except ConfigFileInvalidException as e:
				print("Unable to read config file due to invalid JSON format in '%s'" % e)
				return

			# Merge config values from config file (overrides environment variables)
			config.update(file_config)

		# Rename legacy config option names
		config = rename_legacy_attribute_names(config)

		# Initialize config by expanding with missing values
		config = self.init_config(config)

		return config

def main():
	app  = QApplication(sys.argv) 
	form = GAD_PreferenceUI()
	print (json.dumps(form.CONFIG, indent = 2))
	app.exec_()

if __name__ == '__main__':
	main()