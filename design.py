import keyboard
from PyQt5 import QtCore, QtGui
import PyQt5.QtWidgets as QtWidgets
import config
import os
import sys
import UC
import speech
import data_exchange
from logger import log
from execute_command import ntn


class Ui_Form(object):
    def setupUi(self, Form):
        self.ListenThreadHotWords = ListenThreadHotWords()
        self.ListenThreadHotWords.start()   # Запуск отдельного потока для прослушивания горячих слов
        self.TabListen = WaitTabListen(self)
        self.TabListen.start()
        # self.NoteBook = NoteBookThread()
        # self.NoteBook.start()

        self.Form = Form
        self.threadSay = None

        Form.setObjectName("Form")
        Form.resize(700, 700)
        Form.setMinimumSize(QtCore.QSize(700, 700))
        Form.setMaximumSize(QtCore.QSize(700, 700))

        id_font = QtGui.QFontDatabase.addApplicationFont('ofont.ru_Sunday.ttf')
        if id_font == -1:
            print('Шрифт SUNDAY не установлен')
        
        font = QtGui.QFont()
        font.setFamily("Sunday")
        font.setPointSize(20)

        # Главная страница
        self.VerticalLayoutMainWidget = QtWidgets.QWidget(Form)
        self.VerticalLayoutMainWidget.setGeometry(QtCore.QRect(50, 0, 600, 500))
        self.VerticalLayoutMainWidget.setStyleSheet(".QPushButton {background-color: transparent; color: white; border-radius: 10px; border: 1px solid white; padding-bottom: 3px;} \
            .QPushButton:hover {border-color: #858EE2}")
        self.VerticalLayoutMain = QtWidgets.QVBoxLayout(self.VerticalLayoutMainWidget)
        self.VerticalLayoutMain.setContentsMargins(0, 0, 0, 0)

        self.LabelMain = QtWidgets.QLabel(self.VerticalLayoutMainWidget)
        self.LabelMain.setText("Голосовой асисстент - Джек")
        self.LabelMain.setTextFormat(QtCore.Qt.AutoText)
        self.LabelMain.setAlignment(QtCore.Qt.AlignCenter)
        self.LabelMain.setStyleSheet(".QLabel {color: white;}")
        self.LabelMain.setFont(font)
        self.VerticalLayoutMain.addWidget(self.LabelMain)

        self.VerticalLayoutMain.addSpacing(250)

        self.SettingsButton = QtWidgets.QPushButton(self.VerticalLayoutMainWidget)
        self.SettingsButton.clicked.connect(lambda: self.settings_open_close())
        font.setPointSize(14)
        self.SettingsButton.setFont(font)
        self.SettingsButton.setText("Настройки")
        self.VerticalLayoutMain.addWidget(self.SettingsButton)

        self.VerticalLayoutMain.addSpacing(50)

        self.AllCommandsButton = QtWidgets.QPushButton(self.VerticalLayoutMainWidget)
        self.AllCommandsButton.clicked.connect(lambda: self.all_commands_open_close())
        self.AllCommandsButton.setFont(font)
        self.AllCommandsButton.setText("Все команды")
        self.VerticalLayoutMain.addWidget(self.AllCommandsButton)

        self.VerticalLayoutMain.addStretch(3)

        # Настройки
        self.VerticalLayoutSettingsWidget = QtWidgets.QWidget(Form)
        self.VerticalLayoutSettingsWidget.setGeometry(QtCore.QRect(125, 0, 450, 550))
        self.VerticalLayoutSettings = QtWidgets.QVBoxLayout(self.VerticalLayoutSettingsWidget)
        self.VerticalLayoutSettings.setContentsMargins(0, 0, 0, 0)
        self.VerticalLayoutSettingsWidget.setStyleSheet("\
        .QLabel {color: white;} \
        .QPushButton {border-radius: 10px; background-color: transparent; color: white; padding-bottom: 3px; \
            padding-left: 5px; padding-right: 5px; border: 1px solid white;} \
        .QPushButton:hover {border-width: 2px;} \
        .QComboBox {background-color: transparent; color: white; border: 1px solid white; border-radius: 10px;} \
        .QComboBox QAbstractItemView {background-color: #5c66cc; selection-background-color: #5c66cc; \
            border: 1px solid white; color: white;} \
        .QLineEdit {border-radius: 10px; background-color: transparent; color: white; padding-bottom: 3px; \
            padding-left: 5px; padding-right: 5px; border: 1px solid white;} \
        .QGroupBox {border: none;}")

        font.setPointSize(20)

        self.LabelSettings = QtWidgets.QLabel(self.VerticalLayoutSettingsWidget)
        self.LabelSettings.setText("Настройки")
        self.LabelSettings.setTextFormat(QtCore.Qt.AutoText)
        self.LabelSettings.setAlignment(QtCore.Qt.AlignCenter)
        self.LabelSettings.setFont(font)
        self.VerticalLayoutSettings.addWidget(self.LabelSettings)

        self.VerticalLayoutSettings.addStretch(4)
        

        # Язык интерфейса, пока бесплоезно, поэтому не делаю
        font.setPointSize(16)

        self.LabelLanguageInterface = QtWidgets.QLabel(self.VerticalLayoutSettingsWidget)
        self.LabelLanguageInterface.setText("Язык интерефейса")
        self.LabelLanguageInterface.setTextFormat(QtCore.Qt.AutoText)
        self.LabelLanguageInterface.setFont(font)
        self.LabelLanguageInterface.setHidden(not self.LabelLanguageInterface.isHidden()) # Если захочу сделать - закоментировать
        self.VerticalLayoutSettings.addWidget(self.LabelLanguageInterface)
        
        font.setPointSize(14)

        self.InputLanguageInterface = QtWidgets.QComboBox(self.VerticalLayoutSettingsWidget)
        self.InputLanguageInterface.addItems(['Русский', 'English'])
        self.InputLanguageInterface.setFont(font)
        self.InputLanguageInterface.setHidden(not self.InputLanguageInterface.isHidden()) # Если захочу сделать - закоментировать
        self.VerticalLayoutSettings.addWidget(self.InputLanguageInterface)

        self.VerticalLayoutSettings.addStretch(1)

        font.setPointSize(16)

        self.LabelMethodRecognation = QtWidgets.QLabel(self.VerticalLayoutSettingsWidget)
        self.LabelMethodRecognation.setText("Способ распознавания")
        self.LabelMethodRecognation.setTextFormat(QtCore.Qt.AutoText)
        self.LabelMethodRecognation.setFont(font)
        self.VerticalLayoutSettings.addWidget(self.LabelMethodRecognation)

        font.setPointSize(14)

        self.InputMethodRecognation = QtWidgets.QComboBox(self.VerticalLayoutSettingsWidget)
        self.InputMethodRecognation.addItems(['Онлайн', 'Оффлайн'])
        self.InputMethodRecognation.setFont(font)
        self.VerticalLayoutSettings.addWidget(self.InputMethodRecognation)

        self.VerticalLayoutSettings.addStretch(1)

        font.setPointSize(16)

        self.LabelBrowserDefault = QtWidgets.QLabel(self.VerticalLayoutSettingsWidget)
        self.LabelBrowserDefault.setText("Браузер")
        self.LabelBrowserDefault.setTextFormat(QtCore.Qt.AutoText)
        self.LabelBrowserDefault.setFont(font)
        self.VerticalLayoutSettings.addWidget(self.LabelBrowserDefault)

        font.setPointSize(14)

        self.HorizontalLayoutBrowserWidget = QtWidgets.QGroupBox(self.VerticalLayoutSettingsWidget)
        self.HorizontalLayoutBrowser = QtWidgets.QHBoxLayout(self.HorizontalLayoutBrowserWidget)

        self.LineEditPathSettings = QtWidgets.QLineEdit(self.HorizontalLayoutBrowserWidget)
        self.LineEditPathSettings.setFont(font)
        self.HorizontalLayoutBrowser.addWidget(self.LineEditPathSettings)


        self.ButtonBrowseSettings = QtWidgets.QPushButton(self.HorizontalLayoutBrowserWidget)
        self.ButtonBrowseSettings.clicked.connect(lambda: self.settings_browse_path())
        self.ButtonBrowseSettings.setText("Обзор")
        self.ButtonBrowseSettings.setStyleSheet(".QPushButton {padding-left: 5px; padding-right: 5px;}")
        self.ButtonBrowseSettings.setFont(font)
        self.HorizontalLayoutBrowser.addWidget(self.ButtonBrowseSettings)

        self.HorizontalLayoutBrowserWidget.setLayout(self.HorizontalLayoutBrowser)
        self.VerticalLayoutSettings.addWidget(self.HorizontalLayoutBrowserWidget)

        font.setPointSize(16)

        self.LabelScreenshotsPath = QtWidgets.QLabel(self.VerticalLayoutSettingsWidget)
        self.LabelScreenshotsPath.setText("Скриншоты")
        self.LabelScreenshotsPath.setTextFormat(QtCore.Qt.AutoText)
        self.LabelScreenshotsPath.setFont(font)
        self.VerticalLayoutSettings.addWidget(self.LabelScreenshotsPath)

        font.setPointSize(14)

        self.HorizontalLayoutScreenshotsWidget = QtWidgets.QGroupBox(self.VerticalLayoutSettingsWidget)
        self.HorizontalLayoutScreenshots = QtWidgets.QHBoxLayout(self.HorizontalLayoutScreenshotsWidget)

        self.LineEditScreenshotsSettings = QtWidgets.QLineEdit(self.HorizontalLayoutScreenshotsWidget)
        self.LineEditScreenshotsSettings.setFont(font)
        self.HorizontalLayoutScreenshots.addWidget(self.LineEditScreenshotsSettings)


        self.ButtonBrowseScreenshotsSettings = QtWidgets.QPushButton(self.HorizontalLayoutScreenshotsWidget)
        self.ButtonBrowseScreenshotsSettings.clicked.connect(lambda: self.settings_browse_screenshots())
        self.ButtonBrowseScreenshotsSettings.setText("Обзор")
        self.ButtonBrowseScreenshotsSettings.setStyleSheet(".QPushButton {padding-left: 5px; padding-right: 5px;}")
        self.ButtonBrowseScreenshotsSettings.setFont(font)
        self.HorizontalLayoutScreenshots.addWidget(self.ButtonBrowseScreenshotsSettings)

        self.HorizontalLayoutScreenshotsWidget.setLayout(self.HorizontalLayoutBrowser)
        self.VerticalLayoutSettings.addWidget(self.HorizontalLayoutScreenshotsWidget)

        self.VerticalLayoutSettings.addStretch(2)

        font.setPointSize(16)

        self.LayoutButtonsSettingsWidget = QtWidgets.QGroupBox(self.VerticalLayoutSettingsWidget)
        self.LayoutButtonsSettings = QtWidgets.QHBoxLayout(self.LayoutButtonsSettingsWidget)

        self.ButtonSaveSettings = QtWidgets.QPushButton(self.LayoutButtonsSettingsWidget)
        self.ButtonSaveSettings.clicked.connect(lambda: self.settings_close_save())
        self.ButtonSaveSettings.setText("Сохранить")
        self.ButtonSaveSettings.setStyleSheet(".QPushButton {color: #8EF13C; border-color: #8EF13C;}")
        self.ButtonSaveSettings.setFont(font)
        self.LayoutButtonsSettings.addWidget(self.ButtonSaveSettings)

        self.ButtonCancelSettings = QtWidgets.QPushButton(self.LayoutButtonsSettingsWidget)
        self.ButtonCancelSettings.clicked.connect(lambda: self.settings_close_cancel())
        self.ButtonCancelSettings.setText("Отмена")
        self.ButtonCancelSettings.setStyleSheet(".QPushButton {color: #F13C73; border-color: #F13C73;}")
        self.ButtonCancelSettings.setFont(font)
        self.LayoutButtonsSettings.addWidget(self.ButtonCancelSettings)

        self.LayoutButtonsSettingsWidget.setLayout(self.LayoutButtonsSettings)
        self.VerticalLayoutSettings.addWidget(self.LayoutButtonsSettingsWidget)

        # Все команды

        self.VerticalLayoutAllCommandsWidget = QtWidgets.QWidget(Form)
        self.VerticalLayoutAllCommandsWidget.setGeometry(QtCore.QRect(125, 0, 450, 550))
        self.VerticalLayoutAllCommandsWidget.setStyleSheet("\
        .QPushButton {background-color: transparent; color: white; border-radius: 10px; border: 1px solid white; \
            padding-bottom: 3px;} \
        .QPushButton:hover {border-width: 2px;} \
        .QGroupBox {background-color: transparent; border: none;} \
        .QLabel {background-color: transparent; border-radius: 10px; border: 1px solid #858EE2; color: white; \
            padding-bottom: 3px;}")
        self.VerticalLayoutAllCommands = QtWidgets.QVBoxLayout(self.VerticalLayoutAllCommandsWidget)
        self.VerticalLayoutAllCommands.setContentsMargins(0, 0, 0, 0)

        font.setPointSize(20)

        self.LabelAllCommands = QtWidgets.QLabel(self.VerticalLayoutAllCommandsWidget)
        self.LabelAllCommands.setText("Все команды")
        self.LabelAllCommands.setTextFormat(QtCore.Qt.AutoText)
        self.LabelAllCommands.setAlignment(QtCore.Qt.AlignCenter)
        self.LabelAllCommands.setStyleSheet(".QLabel {color: white; border: none;}")
        self.LabelAllCommands.setFont(font)
        self.VerticalLayoutAllCommands.addWidget(self.LabelAllCommands)
        
        self.VerticalLayoutAllCommands.addSpacing(10)

        font.setPointSize(14)

        self.GroupBoxAllCommands = QtWidgets.QGroupBox(self.VerticalLayoutAllCommandsWidget)
        self.GroupBoxAllCommands.setStyleSheet("\
        .QLabel {font-style: bold;}")
        self.FormLayoutAllCommands = QtWidgets.QFormLayout(self.GroupBoxAllCommands)
        self.GroupBoxAllCommands.setLayout(self.FormLayoutAllCommands)

        self.HintTextAllCommands = QtWidgets.QLineEdit(self.GroupBoxAllCommands)
        self.HintTextAllCommands.setReadOnly(True)
        self.HintTextAllCommands.setAlignment(QtCore.Qt.AlignCenter)
        self.HintTextAllCommands.setText("Команда")
        self.HintTextAllCommands.setFont(font)

        self.HintPathAllCommands = QtWidgets.QLineEdit(self.GroupBoxAllCommands)
        self.HintPathAllCommands.setReadOnly(True)
        self.HintPathAllCommands.setAlignment(QtCore.Qt.AlignCenter)
        self.HintPathAllCommands.setText("Путь")
        self.HintPathAllCommands.setFont(font)

        self.ScrollAllCommands = QtWidgets.QScrollArea()
        self.ScrollAllCommands.setStyleSheet("\
            .QScrollArea {background: transparent; border-radius: 10px; border: 1px solid white;} \
            .QScrollBar {background: rgba(38, 38, 38, 0.5); width: 10px; border-radius: 5px;} \
            .QScrollBar::handle {background-color:  rgba(140, 140, 140, 0.3); border-radius: 5px; border: 1px solid black;} \
            .QScrollBar::handle:hover {background-color:  rgba(120, 140, 140, 0.5); border-radius: 5px; border: 1px solid black;} \
            .QScrollBar::add-line {background: transparent;}    \
            .QScrollBar::sub-line {background: transparent;} \
            .QScrollBar::up-arrow, .QScrollBar::down-arrow {background: none;} \
            .QScrollBar::add-page, .QScrollBar::sub-page {background: none;}    \
            .QLineEdit {background: transparent; border-radius: 10px; border: 1px solid #858EE2; color: white; padding-left: 5px; \
            padding-right: 5px; padding-bottom: 3px;}")
        self.ScrollAllCommands.setWidget(self.GroupBoxAllCommands)
        self.ScrollAllCommands.setWidgetResizable(True)

        self.VerticalLayoutAllCommands.addWidget(self.ScrollAllCommands)
        self.FormLayoutAllCommands.addRow(self.HintTextAllCommands, self.HintPathAllCommands)

        font.setPointSize(16)
        
        self.GroupBoxButtonsAllCommands = QtWidgets.QGroupBox(self.VerticalLayoutAllCommandsWidget)
        self.GroupBoxButtonsAllCommands.setStyleSheet("\
        .QLabel {border-color: #858EE2; color: gray;}")

        BoxLayoutButtonsV = QtWidgets.QVBoxLayout(self.GroupBoxButtonsAllCommands)
        self.GroupBoxButtonsAllCommands.setLayout(BoxLayoutButtonsV)
        
        BoxLayoutButtonsH = QtWidgets.QHBoxLayout(self.GroupBoxButtonsAllCommands)
        self.VerticalLayoutAllCommands.addWidget(self.GroupBoxButtonsAllCommands)

        self.AddNewCommands = QtWidgets.QPushButton(self.VerticalLayoutAllCommandsWidget)
        self.AddNewCommands.clicked.connect(lambda: self.add_command_open_close())
        self.AddNewCommands.setText("Добавить новую команду")
        self.AddNewCommands.setFont(font)
        self.AddNewCommands.setStyleSheet(".QPushButton {border-color: RGBA(7, 87, 170, 0.5)}")

        self.SaveAndExitAllCommands = QtWidgets.QPushButton(self.GroupBoxButtonsAllCommands)
        self.SaveAndExitAllCommands.clicked.connect(lambda: self.all_commands_close_save())
        self.SaveAndExitAllCommands.setText("Сохранить")
        self.SaveAndExitAllCommands.setFont(font)
        self.SaveAndExitAllCommands.setStyleSheet(".QPushButton {border-color: #8EF13C; color: #8EF13C;}")

        self.ExitAllCommands = QtWidgets.QPushButton(self.GroupBoxButtonsAllCommands)
        self.ExitAllCommands.clicked.connect(lambda: self.all_commands_close_cancel())
        self.ExitAllCommands.setText("Отмена")
        self.ExitAllCommands.setFont(font)
        self.ExitAllCommands.setStyleSheet(".QPushButton {border-color: #F13C73; color: #F13C73}")

        BoxLayoutButtonsH.addWidget(self.SaveAndExitAllCommands)
        BoxLayoutButtonsH.addWidget(self.ExitAllCommands)
        
        BoxLayoutButtonsV.addWidget(self.AddNewCommands)
        
        BoxLayoutButtonsV.addLayout(BoxLayoutButtonsH)

        # Добавить команду
        self.VerticalLayoutAddCommandWidget = QtWidgets.QWidget(Form)
        self.VerticalLayoutAddCommandWidget.setGeometry(QtCore.QRect(125, 0, 450, 550))
        self.VerticalLayoutAddCommandWidget.setStyleSheet("\
        .QPushButton {background-color: transparent; color: white; border-radius: 10px; border: 1px solid white; \
            padding-bottom: 3px;} \
        .QPushButton:hover {border-width: 2px;} \
        .QLineEdit {color: white; padding-bottom: 3px; border-radius: 10px; border: 1px solid white; \
            padding-left: 5px; padding-right: 5px; background: transparent;}")
        self.VerticalLayoutAddCommand = QtWidgets.QVBoxLayout(self.VerticalLayoutAddCommandWidget)
        self.VerticalLayoutAddCommand.setContentsMargins(0, 0, 0, 0)

        font.setPointSize(20)

        self.LabelAddCommand = QtWidgets.QLabel(self.VerticalLayoutAllCommandsWidget)
        self.LabelAddCommand.setText("Добавить команду")
        self.LabelAddCommand.setTextFormat(QtCore.Qt.AutoText)
        self.LabelAddCommand.setAlignment(QtCore.Qt.AlignCenter)
        self.LabelAddCommand.setStyleSheet(".QLabel {color: white;}")
        self.LabelAddCommand.setFont(font)
        self.VerticalLayoutAddCommand.addWidget(self.LabelAddCommand)

        self.VerticalLayoutAddCommand.addStretch(2)

        font.setPointSize(16)

        self.HintTextAddCommand = QtWidgets.QLabel(self.VerticalLayoutAddCommandWidget)
        self.HintTextAddCommand.setText("Команда:")
        self.HintTextAddCommand.setTextFormat(QtCore.Qt.AutoText)
        self.HintTextAddCommand.setStyleSheet(".QLabel {color: white;}")
        self.HintTextAddCommand.setFont(font)
        self.VerticalLayoutAddCommand.addWidget(self.HintTextAddCommand)

        font.setPointSize(14)

        self.LineEditTextAddCommand = QtWidgets.QLineEdit(self.VerticalLayoutAddCommandWidget)
        self.LineEditTextAddCommand.setFont(font)
        self.VerticalLayoutAddCommand.addWidget(self.LineEditTextAddCommand)

        font.setPointSize(16)

        self.ButtonRecordAddCommand = QtWidgets.QPushButton(self.VerticalLayoutAddCommandWidget)
        self.ButtonRecordAddCommand.clicked.connect(lambda: self.add_command_listen())
        self.ButtonRecordAddCommand.setText("Запись")
        self.ButtonRecordAddCommand.setStyleSheet(".QPushButton {min-width: 300px;}")
        self.ButtonRecordAddCommand.setFont(font)
        self.VerticalLayoutAddCommand.addWidget(self.ButtonRecordAddCommand, alignment=QtCore.Qt.AlignCenter)

        self.VerticalLayoutAddCommand.addStretch(1)

        font.setPointSize(16)

        self.HintTextAddCommand = QtWidgets.QLabel(self.VerticalLayoutAddCommandWidget)
        self.HintTextAddCommand.setText("Путь:")
        self.HintTextAddCommand.setTextFormat(QtCore.Qt.AutoText)
        self.HintTextAddCommand.setStyleSheet(".QLabel {color: white;}")
        self.HintTextAddCommand.setFont(font)
        self.VerticalLayoutAddCommand.addWidget(self.HintTextAddCommand)

        font.setPointSize(14)

        GroupBoxAddCommand = QtWidgets.QGroupBox(self.VerticalLayoutAddCommandWidget)
        GroupBoxAddCommand.setStyleSheet(".QGroupBox {background: transparent; border: none;}")
        self.VerticalLayoutAddCommand.addWidget(GroupBoxAddCommand)
        FormLayoutAddCommand = QtWidgets.QFormLayout(GroupBoxAddCommand)
        GroupBoxAddCommand.setLayout(FormLayoutAddCommand)

        
        self.LineEditPathAddCommand = QtWidgets.QLineEdit(GroupBoxAddCommand)
        self.LineEditPathAddCommand.setFont(font)

        font.setPointSize(16)

        self.ButtonBrowseAddCommand = QtWidgets.QPushButton(GroupBoxAddCommand)
        self.ButtonBrowseAddCommand.clicked.connect(lambda: self.add_command_browse_path())
        self.ButtonBrowseAddCommand.setText("Обзор")
        self.ButtonBrowseAddCommand.setFont(font)
        FormLayoutAddCommand.addRow(self.LineEditPathAddCommand, self.ButtonBrowseAddCommand)

        self.VerticalLayoutAddCommand.addStretch(1)

        GroupBoxAddCommand = QtWidgets.QGroupBox(self.VerticalLayoutAddCommandWidget)
        GroupBoxAddCommand.setStyleSheet(".QGroupBox {background: transparent; border: none;}")
        self.VerticalLayoutAddCommand.addWidget(GroupBoxAddCommand)
        FormLayoutAddCommand = QtWidgets.QHBoxLayout(GroupBoxAddCommand)
        GroupBoxAddCommand.setLayout(FormLayoutAddCommand)

        self.ButtonAddAddCommand = QtWidgets.QPushButton(GroupBoxAddCommand)
        self.ButtonAddAddCommand.clicked.connect(lambda: self.add_command_close_add())
        self.ButtonAddAddCommand.setText("Добавить")
        self.ButtonAddAddCommand.setStyleSheet(".QPushButton {border-color: #8EF13C; color: #8EF13C;}")
        self.ButtonAddAddCommand.setFont(font)

        self.ButtonCancelAddCommand = QtWidgets.QPushButton(GroupBoxAddCommand)
        self.ButtonCancelAddCommand.clicked.connect(lambda: self.add_command_open_close())
        self.ButtonCancelAddCommand.setText("Отмена")
        self.ButtonCancelAddCommand.setStyleSheet(".QPushButton {border-color: #F13C73; color: #F13C73}")
        self.ButtonCancelAddCommand.setFont(font)

        FormLayoutAddCommand.addWidget(self.ButtonAddAddCommand)
        FormLayoutAddCommand.addWidget(self.ButtonCancelAddCommand)

        # Ошибка добавление команды

        self.VerticalLayoutWarningAddCommandWidget = QtWidgets.QWidget(Form)
        self.VerticalLayoutWarningAddCommandWidget.setGeometry(QtCore.QRect(125, 0, 450, 550))
        self.VerticalLayoutWarningAddCommandWidget.setStyleSheet("\
        .QPushButton {background-color: transparent; color: white; border-radius: 10px; border: 1px solid white; \
            padding-bottom: 3px;} \
        .QPushButton:hover {border-width: 2px;}")
        self.VerticalLayoutWarningAddCommand = QtWidgets.QVBoxLayout(self.VerticalLayoutWarningAddCommandWidget)
        self.VerticalLayoutWarningAddCommand.setContentsMargins(0, 0, 0, 0)

        font.setPointSize(20)

        self.LabelWarningAddCommand = QtWidgets.QLabel(self.VerticalLayoutWarningAddCommandWidget)
        self.LabelWarningAddCommand.setTextFormat(QtCore.Qt.AutoText)
        self.LabelWarningAddCommand.setAlignment(QtCore.Qt.AlignCenter)
        self.LabelWarningAddCommand.setStyleSheet(".QLabel {color: red;}")
        self.LabelWarningAddCommand.setFont(font)
        self.VerticalLayoutWarningAddCommand.addWidget(self.LabelWarningAddCommand)

        self.VerticalLayoutWarningAddCommand.addStretch(2)

        font.setPointSize(14)
        self.LabelTextWarningAddCommand = QtWidgets.QLabel(self.VerticalLayoutWarningAddCommandWidget)
        self.LabelTextWarningAddCommand.setTextFormat(QtCore.Qt.AutoText)
        self.LabelTextWarningAddCommand.setAlignment(QtCore.Qt.AlignCenter)
        self.LabelTextWarningAddCommand.setStyleSheet(".QLabel {color: white;}")
        self.LabelTextWarningAddCommand.setFont(font)
        self.VerticalLayoutWarningAddCommand.addWidget(self.LabelTextWarningAddCommand)

        self.VerticalLayoutWarningAddCommand.addStretch(1)

        font.setPointSize(16)
        GroupBoxWarning = QtWidgets.QGroupBox(self.VerticalLayoutWarningAddCommandWidget)
        GroupBoxWarning.setStyleSheet(".QGroupBox {border: none}")
        self.VerticalLayoutWarningAddCommand.addWidget(GroupBoxWarning)
        HLayoutButtonsWarning = QtWidgets.QHBoxLayout(GroupBoxWarning)
        GroupBoxWarning.setLayout(HLayoutButtonsWarning)

        self.ButtonWarningYes = QtWidgets.QPushButton(GroupBoxWarning)
        self.ButtonWarningYes.clicked.connect(lambda: self.warning_yes())
        self.ButtonWarningYes.setStyleSheet(".QPushButton {border-color: #F13C73; color: #F13C73;}")
        self.ButtonWarningYes.setText("Да")
        self.ButtonWarningYes.setFont(font)
        self.ButtonWarningYes.setHidden(not self.ButtonWarningYes.isHidden())
        HLayoutButtonsWarning.addWidget(self.ButtonWarningYes)

        self.ButtonWarningNo = QtWidgets.QPushButton(GroupBoxWarning)
        self.ButtonWarningNo.clicked.connect(lambda: self.warning_no())
        self.ButtonWarningNo.setStyleSheet(".QPushButton {border-color: #8EF13C; color: #8EF13C;}")
        self.ButtonWarningNo.setText("Нет")
        self.ButtonWarningNo.setFont(font)
        self.ButtonWarningNo.setHidden(not self.ButtonWarningNo.isHidden())
        HLayoutButtonsWarning.addWidget(self.ButtonWarningNo)

        self.ButtonWarningOk = QtWidgets.QPushButton(GroupBoxWarning)
        self.ButtonWarningOk.clicked.connect(lambda: self.warning_ok())
        self.ButtonWarningOk.setStyleSheet(".QPushButton {border-color: #8EF13C; color: #8EF13C;}")
        self.ButtonWarningOk.setText("Ок")
        self.ButtonWarningOk.setFont(font)
        self.ButtonWarningOk.setHidden(not self.ButtonWarningOk.isHidden())
        HLayoutButtonsWarning.addWidget(self.ButtonWarningOk)

        # self.VerticalLayoutMainWidget.setHidden(not self.VerticalLayoutMainWidget.isHidden()) # Убрать
        self.VerticalLayoutWarningAddCommandWidget.setHidden(not self.VerticalLayoutWarningAddCommandWidget.isHidden())
        self.VerticalLayoutAddCommandWidget.setHidden(not self.VerticalLayoutAddCommandWidget.isHidden())
        self.VerticalLayoutAllCommandsWidget.setHidden(not self.VerticalLayoutAllCommandsWidget.isHidden())
        self.VerticalLayoutSettingsWidget.setHidden(not self.VerticalLayoutSettingsWidget.isHidden())
        # self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.start_load(font)
        Form.setWindowTitle("Jack")

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        if config.language_interface == "English":
            Form.setWindowTitle(_translate("Form", "Jack"))
            self.label.setText(_translate("Form", "Voice assistant - Jack"))
            self.settingsButton.setText(_translate("Form", "Settings"))

            self.all_commands.setText(_translate("Form", "All commands"))
            self.addCommandButton.setText(_translate("Form", "  Add new command  "))
            self.addTextLabelHint.setText(_translate("Form", "Command text:"))

            self.onVoiceListenButton.setText(_translate("Form", "Record"))
            self.addPathLabelHint.setText(_translate("Form", "Path:"))
            self.submitAddCommandButton.setText(_translate("Form", "Add"))
            self.cancelAddCommandButton.setText(_translate("Form", "Cancel"))
            self.browseFileSystem.setText(_translate("Form", "Browse"))

            self.returnOnMainAllCommands.setText(_translate("Form", "   Back on main    "))
            self.returnOnMainSettings.setText(_translate("Form", "   Back on main    "))

            self.addCommandErrorLabel.setText(_translate("Form", "Error"))
            self.addCommandErrorText.setText(_translate("Form", "The command already exists"))
            self.addCommandErrorButton.setText(_translate("Form", "    OK    "))

            self.settingsHintLanguage.setText(_translate("Form", "Interface language: "))
            self.settingsHintRecognation.setText(_translate("Form", "Recognition method: "))
            self.settingsHintBrowserDefault.setText(_translate("Form", "Default browser"))
            self.settingsBrowserButton.setText(_translate("Form", "Browse"))
            self.settingsSave.setText(_translate("Form", "    Save    "))
        elif config.language_interface == "Russian":
            Form.setWindowTitle(_translate("Form", "Джек"))
            self.label.setText(_translate("Form", "Голосовой ассистент - Джек"))
            self.settingsButton.setText(_translate("Form", "Настройки"))

            self.all_commands.setText(_translate("Form", "Все команды"))
            self.addCommandButton.setText(_translate("Form", "  Добавить новую команду  "))
            self.addTextLabelHint.setText(_translate("Form", "Текст команды:"))

            self.onVoiceListenButton.setText(_translate("Form", "Запись"))
            self.addPathLabelHint.setText(_translate("Form", "Путь:"))
            self.submitAddCommandButton.setText(_translate("Form", "Добавить"))
            self.cancelAddCommandButton.setText(_translate("Form", "Отмена"))
            self.browseFileSystem.setText(_translate("Form", "Обзор"))

            self.returnOnMainAllCommands.setText(_translate("Form", "   Вернуться на главную    "))
            self.returnOnMainSettings.setText(_translate("Form", "   Вернуться на главную    "))

            self.addCommandErrorLabel.setText(_translate("Form", "Ошибка"))
            self.addCommandErrorText.setText(_translate("Form", "Команда уже существует"))
            self.addCommandErrorButton.setText(_translate("Form", "    OK    "))

            self.settingsHintLanguage.setText(_translate("Form", "Язык интерфейса: "))
            self.settingsHintRecognation.setText(_translate("Form", "Метод распознования: "))
            self.settingsHintBrowserDefault.setText(_translate("Form", "Браузер по умолчанию"))
            self.settingsBrowserButton.setText(_translate("Form", "Обзор"))
            self.settingsSave.setText(_translate("Form", "    Сохранить    "))
    
    def start_load(self, font):
        # загрузка настроек
        self.InputLanguageInterface.setCurrentText(config.language_interface)
        self.InputMethodRecognation.setCurrentIndex(config.method_recognition)
        self.LineEditPathSettings.setText(config.browser_path)
        self.LineEditScreenshotsSettings.setText(config.path_to_screenshots)

        # загрузка команд
        font.setPointSize(14)
        for command, path in UC.commands.items(): 
            text_command = QtWidgets.QLineEdit()
            text_command.setText(command)
            text_command.setFont(font)

            text_path = QtWidgets.QLineEdit()
            text_path.setText(path)
            text_path.setFont(font)

            self.FormLayoutAllCommands.addRow(text_command, text_path)

    def settings_open_close(self):
        self.VerticalLayoutSettingsWidget.setHidden(not self.VerticalLayoutSettingsWidget.isHidden())
        self.VerticalLayoutMainWidget.setHidden(not self.VerticalLayoutMainWidget.isHidden())

    def settings_close_cancel(self):
        self.settings_open_close()

        self.InputLanguageInterface.setCurrentText(config.language_interface)
        self.InputMethodRecognation.setCurrentIndex(config.method_recognition)
        self.LineEditPathSettings.setText(config.browser_path)
        self.LineEditScreenshotsSettings.setText(config.path_to_screenshots)

    def settings_close_save(self):
        self.settings_open_close()

        # сохранение при закрытии
        config.language_interface = self.InputLanguageInterface.currentText()   # язык интерфейса
        config.method_recognition = self.InputMethodRecognation.currentIndex()  # способ распознования: 0 - онлайн, 1 - оффлайн
        config.browser_path = self.LineEditPathSettings.text()                  # браузер
        config.path_to_screenshots = self.LineEditScreenshotsSettings.text()    # Скриншоты

    def settings_browse_path(self):
        path_window = QtWidgets.QFileDialog.getOpenFileName()[0]
        self.LineEditPathSettings.setText(path_window)

    def settings_browse_screenshots(self):
        path_window = QtWidgets.QFileDialog.getExistingDirectory()
        print(path_window)
        self.LineEditScreenshotsSettings.setText(path_window)

    def all_commands_open_close(self):
        self.VerticalLayoutAllCommandsWidget.setHidden(not self.VerticalLayoutAllCommandsWidget.isHidden())
        self.VerticalLayoutMainWidget.setHidden(not self.VerticalLayoutMainWidget.isHidden())

    def all_commands_close_cancel(self):
        self.all_commands_open_close()

        d = list(UC.commands.items())

        for i in range(1, self.FormLayoutAllCommands.rowCount()):
            text = self.FormLayoutAllCommands.itemAt(i, 0).widget()
            path = self.FormLayoutAllCommands.itemAt(i, 1).widget()
            if text.text() != d[i-1][0]:
                text.setText(d[i-1][0])
            
            if path.text() != d[i-1][1]:
                path.setText(d[i-1][1])

    def all_commands_close_save(self):
        self.all_commands_open_close()

        # сохранение
        UC.commands.clear()
        t = self.FormLayoutAllCommands.rowCount()
        x = 0
        for i in range(1, t):
            try:
                command = self.FormLayoutAllCommands.itemAt(i-x, 0).widget().text()
                path = self.FormLayoutAllCommands.itemAt(i-x, 1).widget().text()

                if command.strip(" ") == "" or path.strip(" ") == "":
                    self.FormLayoutAllCommands.removeRow(i - x)
                    x += 1
                    continue

                if command not in UC.commands:
                    UC.commands[command] = path
                else:
                    z = 0
                    while command + f"_{z}" not in UC.commands:
                        z += 1
                    
                    UC.commands[command + f"_{z}"] = path
            except:
                continue

        d = list(UC.commands.items())
        if len(d) != 0:
            for i in range(1, self.FormLayoutAllCommands.rowCount()):
                try:
                    text = self.FormLayoutAllCommands.itemAt(i, 0).widget()
                    path = self.FormLayoutAllCommands.itemAt(i, 1).widget()

                    if text.text() != d[i-1][0]:
                        text.setText(d[i-1][0])
                    
                    if path.text() != d[i-1][1]:
                        path.setText(d[i-1][1])
                except:
                    continue
        

        print(UC.commands)

    def add_command_open_close(self):
        self.LineEditTextAddCommand.setText("")
        self.LineEditPathAddCommand.setText("")
        self.ButtonRecordAddCommand.setText("Запись")

        if self.threadSay:
            self.threadSay.terminate()

        self.VerticalLayoutAddCommandWidget.setHidden(not self.VerticalLayoutAddCommandWidget.isHidden())
        self.VerticalLayoutAllCommandsWidget.setHidden(not self.VerticalLayoutAllCommandsWidget.isHidden())

    def add_command_close_add(self):
        font = QtGui.QFont()
        font.setFamily("Sunday")
        font.setPointSize(14)

        command = self.LineEditTextAddCommand.text().strip(" ")
        path = self.LineEditPathAddCommand.text().strip(" ")

        if command == "" or path == "":
            self.LabelWarningAddCommand.setText("Ошибка")
            self.LabelTextWarningAddCommand.setText(""" "Путь" и "команда" не могут быть пустыми """)
            self.ButtonWarningOk.setHidden(not self.ButtonWarningOk.isHidden())

            self.VerticalLayoutAddCommandWidget.setHidden(not self.VerticalLayoutAddCommandWidget.isHidden())
            self.VerticalLayoutWarningAddCommandWidget.setHidden(not self.VerticalLayoutWarningAddCommandWidget.isHidden())

        elif command not in UC.commands:
            UC.commands[command] = path

            text_command = QtWidgets.QLineEdit()
            text_command.setText(command)
            text_command.setFont(font)

            text_path = QtWidgets.QLineEdit()
            text_path.setText(path)
            text_path.setFont(font)

            self.FormLayoutAllCommands.addRow(text_command, text_path)

            self.VerticalLayoutAddCommandWidget.setHidden(not self.VerticalLayoutAddCommandWidget.isHidden())
            self.VerticalLayoutAllCommandsWidget.setHidden(not self.VerticalLayoutAllCommandsWidget.isHidden())
        
        else:
            self.LabelWarningAddCommand.setText("Предупреждение")
            self.LabelTextWarningAddCommand.setText("Такая команда уже существует, \n заменить её?")
            self.ButtonWarningYes.setHidden(not self.ButtonWarningYes.isHidden())
            self.ButtonWarningNo.setHidden(not self.ButtonWarningNo.isHidden())

            self.VerticalLayoutAddCommandWidget.setHidden(not self.VerticalLayoutAddCommandWidget.isHidden())
            self.VerticalLayoutWarningAddCommandWidget.setHidden(not self.VerticalLayoutWarningAddCommandWidget.isHidden())

    def add_command_browse_path(self):
        path_window = QtWidgets.QFileDialog.getOpenFileName()[0]
        self.LineEditPathAddCommand.setText(path_window)

    def add_command_listen(self):
        if self.ButtonRecordAddCommand.text() == "Запись":
            self.ButtonRecordAddCommand.setText("Остановить")
            self.threadSay = ListenThread()
            self.threadSay.finished.connect(lambda: self.add_command_finish_record()) # Когда поток завершиться - вызов функции (она закончится в любом случае)
            self.ListenThreadHotWords.terminate() # Остановка потока с просдушивание горячих слов
            self.threadSay.start() # Запуск потока с просдушиванием ввода
        else:
            self.threadSay.terminate() # Остановка прослушивания ввода
            self.add_command_finish_record()

    def add_command_finish_record(self):
        self.threadSay = None
        self.ButtonRecordAddCommand.setText("Запись")
        self.LineEditTextAddCommand.setText(data_exchange.say_command_text)
        self.ListenThreadHotWords.start()
        
    def warning_yes(self):
        self.ButtonWarningYes.setHidden(not self.ButtonWarningYes.isHidden())
        self.ButtonWarningNo.setHidden(not self.ButtonWarningNo.isHidden())

        command = self.LineEditTextAddCommand.text().strip(" ")
        print(command)
        path = self.LineEditPathAddCommand.text()

        UC.commands[command] = path

        for i in range(1, self.FormLayoutAllCommands.rowCount()):
            commands = self.FormLayoutAllCommands.itemAt(i, 0).widget().text()
            if commands == command:
                self.FormLayoutAllCommands.itemAt(i, 1).widget().setText(path)

        self.VerticalLayoutWarningAddCommandWidget.setHidden(not self.VerticalLayoutWarningAddCommandWidget.isHidden())
        self.VerticalLayoutAllCommandsWidget.setHidden(not self.VerticalLayoutAllCommandsWidget.isHidden())

    def warning_no(self):
        self.ButtonWarningYes.setHidden(not self.ButtonWarningYes.isHidden())
        self.ButtonWarningNo.setHidden(not self.ButtonWarningNo.isHidden())

        self.VerticalLayoutAddCommandWidget.setHidden(not self.VerticalLayoutAddCommandWidget.isHidden())
        self.VerticalLayoutWarningAddCommandWidget.setHidden(not self.VerticalLayoutWarningAddCommandWidget.isHidden())

    def warning_ok(self):
        self.ButtonWarningOk.setHidden(not self.ButtonWarningOk.isHidden())

        self.VerticalLayoutAddCommandWidget.setHidden(not self.VerticalLayoutAddCommandWidget.isHidden())
        self.VerticalLayoutWarningAddCommandWidget.setHidden(not self.VerticalLayoutWarningAddCommandWidget.isHidden())

    def tab_listen(self, n):
        self.ListenThreadHotWords.terminate()
        speech.command()
        self.ListenThreadHotWords.start()
        

class ListenThread(QtCore.QThread):
    def __init__(self):
        super(ListenThread, self).__init__()

    def run(self):
        speech.listening = 1
        speech.say("Начинайте говорить после звукового сигнала", False)
        speech.listen_speech_new_command()


class ListenThreadHotWords(QtCore.QThread):
    def __init__(self):
        super(ListenThreadHotWords, self).__init__()

    def run(self):
        speech.wait_hotwords()


class NoteBookThread(QtCore.QThread):
    def __init__(self):
        super(NoteBookThread, self).__init__()

    def run(self):
        keyboard.add_hotkey("num 1", lambda: ntn.start())
        try:
            keyboard.wait()
        except:
            pass


class WaitTabListen(QtCore.QThread):
    def __init__(self, st):
        super(WaitTabListen, self).__init__()
        self.st = st

    def run(self):
        keyboard.add_hotkey("num 0", lambda: self.st.tab_listen(self.st))
        try:
            keyboard.wait()
        except:
            pass


class FormCreate(QtWidgets.QWidget):
    def __init__(self):
        super(FormCreate, self).__init__()

    def paintEvent(self, a0: QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)
        pixmap = QtGui.QPixmap("./station.png")
        painter.drawPixmap(self.rect(), pixmap)
    
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.hide()
        # config.configfile.save()
        UC.command_file.save()
        # log.close()

        try:
            speech.spotify.browser.close()
            speech.spotify.browser.quit()
        except:
            print(end="")

        return super().closeEvent(a0)


def start():
    UC.command_file = UC.CommandFile()
    # print(UC.commands)
    app = QtWidgets.QApplication(sys.argv)
    Form = FormCreate()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())