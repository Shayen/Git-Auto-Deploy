# editWidget.py
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

class tool_widget(QWidget):

	tool_command = str()
	location 	 = str()

	saveSetting = Signal(str)

	def __init__(self,  parent = None, modulename = '', command = '', location = ''):
		super(tool_widget, self).__init__(parent)
		# QWidget.__init__(parent)

		self.parent = parent
		self.tool_command = command
		self.modulename = modulename

		self.setupUi()
		self.initConnection()

	def setupUi(self):

		# ===================== MAIN WIDGET =====================
		self.horizontalLayout = QHBoxLayout( self )
		self.groupbox = QGroupBox(self)
		self.layout = QVBoxLayout(self.groupbox)

		self.H_layout = QHBoxLayout( self)
		self.label 	= QLabel(self)
		self.openLocation = QPushButton(self.groupbox)
		self.openLocation.setText("Open folder")

		self.groupbox.setLayout(self.layout)
		self.luanch_button = QPushButton(self)
		self.luanch_button.setText("Luanch")
		self.setting_button= QPushButton(self)
		self.setting_button.setIcon(QIcon(modulePath + '/icon/gear.png'))
		
		self.H_layout.addWidget(self.label)
		self.H_layout.addWidget(self.openLocation)
		self.H_layout.addWidget(self.setting_button)
		self.layout.addLayout(self.H_layout)
		self.layout.addWidget(self.luanch_button)
		self.horizontalLayout.addWidget(self.groupbox)

		self.H_layout.setStretchFactor(self.label, 1)

		# Setup stylesheet
		luanch_button_styleSheet = \
		'''
		QPushButton:disabled {background-color:#3f3f3f;
		color: #757575;}
		QPushButton{color : black ;background-color: #b8ff2b;
		font-style : bold;border: none;
		}
		'''
		self.luanch_button.setStyleSheet(luanch_button_styleSheet)
		self.luanch_button.setMinimumHeight(30)

		self.groupbox.setStyleSheet('''QGroupBox {font: bold;}''')

		# ===================== SETTING WIDGET =====================
		self.setting_widget = QWidget()
		self.setting_widget.resize(450, 400)
		setting_V_layout = QVBoxLayout( self.setting_widget )
		setting_locationLabel = QLabel(self.setting_widget)
		setting_locationLabel.setText("Location :")
		self.setting_location = QLineEdit(self.setting_widget)
		setting_label = QLabel(self.setting_widget)
		setting_label.setText("command :")
		self.setting_commandEditor = QTextEdit(self.setting_widget)
		self.setting_commandEditor.setWordWrapMode(QTextOption.NoWrap)
		self.setting_commandEditor.setPlainText(self.tool_command)
		self.setting_saveSetting = QPushButton(self.setting_widget)
		self.setting_saveSetting.setText("save setting")

		setting_V_layout.addWidget(setting_locationLabel)
		setting_V_layout.addWidget(self.setting_location)
		setting_V_layout.addWidget(setting_label)
		setting_V_layout.addWidget(self.setting_commandEditor)
		setting_V_layout.addWidget(self.setting_saveSetting)

		highlight = syntax.PythonHighlighter(self.setting_commandEditor.document())

		if self.tool_command == '':
			self.luanch_button.setEnabled(False)

	def initConnection(self):
		''' Initial connection in Widget '''

		# Main widget
		self.luanch_button.clicked.connect(self.__runCommand  )
		self.openLocation.clicked.connect( self.__openExplorer)
		self.setting_button.clicked.connect(self.call_settingWindow)

		# setting widget
		self.setting_saveSetting.clicked.connect(self.__updateCommand)

	def __updateCommand(self):
		''' update command to '''
		raw_data = self.parent.tool_data

		command  = self.setting_commandEditor.toPlainText()
		location = self.setting_location.text()

		# Update
		raw_data['tools'][self.modulename]['runcmd'] = command
		raw_data['tools'][self.modulename]['location'] = location

		save_config(config_filePath, raw_data)

	def call_settingWindow(self):
		''' open setting window '''
		self.setting_widget.show()

	def setTitle(self, title):
		self.groupbox.setTitle(title)
		self.modulename = title

	def setLinkStatus(self, is_link = False):

		if is_link and self.tool_command != '':
			status = "Status : Linked"
			pixmap = QPixmap( modulePath + '/icon/linked.png')
			self.label.setPixmap(pixmap)
		else :
			status = "Status : Not linked"
			pixmap = QPixmap( modulePath + '/icon/unlinked.png')
			self.label.setPixmap(pixmap)

		# self.label.setText(status)

	def setCommand(self, command):
		self.tool_command = command

	def setLocation(self,location):
		self.location = location
		self.setting_location.setText(location)

	def __openExplorer(self):
		"""Open File explorer after finish."""
		pathTofolder = self.location.replace('/', '\\')
		subprocess.Popen('explorer \/select,\"%s\"' % pathTofolder)

	def __runCommand(self):
		''' Run given command '''
		if self.tool_command == '':
			print ("Please set up command")
			return

		try:
			print(self.tool_command)
			exec(self.tool_command)
		except Exception as e:
			print('\n============ ERROR ============\n')
			traceback.print_exc()
			print(str(e) + "\nPlease check your tool's setting.")