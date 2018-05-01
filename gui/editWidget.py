# editWidget.py
import json
import syntax

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
		self.setWindowTitle('Filter editor')
		self.tool_command = self.setCommand(command)
		self.modulename = modulename

		self.setupUi()
		self.initConnection()

	def setupUi(self):

		# ===================== SETTING WIDGET =====================
		# self = QWidget(self)
		self.resize(450, 400)
		setting_V_layout = QVBoxLayout( self )
		setting_label = QLabel(self)
		setting_label.setText("command :")
		self.setting_commandEditor = QTextEdit(self)
		self.setting_commandEditor.setWordWrapMode(QTextOption.NoWrap)
		self.setting_commandEditor.setPlainText(self.tool_command)
		self.setting_saveSetting = QPushButton(self)
		self.setting_saveSetting.setText("save setting")

		setting_V_layout.addWidget(setting_label)
		setting_V_layout.addWidget(self.setting_commandEditor)
		setting_V_layout.addWidget(self.setting_saveSetting)

		highlight = syntax.PythonHighlighter(self.setting_commandEditor.document())

	def initConnection(self):
		''' Initial connection in Widget '''

		# setting widget
		self.setting_saveSetting.clicked.connect(self.__updateCommand)

	def __updateCommand(self):
		''' update command to '''
		print ('Under construction.')
		return False
		raw_data = self.parent.tool_data

		command  = self.setting_commandEditor.toPlainText()
		location = self.setting_location.text()

		# Update
		raw_data['tools'][self.modulename]['runcmd'] = command
		raw_data['tools'][self.modulename]['location'] = location

		save_config(config_filePath, raw_data)

	def call_settingWindow(self):
		''' open setting window '''
		self.setWindowFlags(Qt.Window)
		self.show()

	def setTitle(self, title):
		self.modulename = title

	def setCommand(self, command):
		if not command :
			self.tool_command = 'Null'
			return 'Null'

		self.tool_command = json.dumps(command, indent = 2)
		return json.dumps(command, indent = 2)

if __name__ == '__main__':
	import sys
	form = QApplication(sys.argv)
	app = tool_widget ()
	app.show()
	form.exec_()