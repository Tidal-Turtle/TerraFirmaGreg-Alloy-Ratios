import sys, os, logging, datetime

from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QDialog, QMessageBox, QLabel, QFrame, QSpacerItem, QMenu
from PyQt6.QtGui import QRegularExpressionValidator, QFont, QAction
from PyQt6.QtCore import QRegularExpression, pyqtSignal, Qt, QTimer
from mainWindow import Ui_MainWindow
from info_dialog import Ui_info_dialog
from settings_dialog import Ui_SettingsDialog
from oreInputWdgt import Ui_oreInputWdgt
from oreOutputWdgt import Ui_oreOutputWdgt

from getAlloyOreInfo import getAlloyOreInfo
from TFG_alloy_ratios import getAlloyRatio
from handleInfoErrors import handleInfo, handleError, errorOutputs
from saveToFile import saveAlloyInfo, getSettingsInfo, saveSettingsInfo

global date_Ymd
global date_YmdHMS
global dir_name
global alloy_types, alloy_dict, settings_dict
alloy_types = ''
alloy_dict = ''
settings_dict = {}

dir_name = 'app'

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.componentsSubcontainer = QtWidgets.QVBoxLayout()
        self.componentsContainer.setSpacing(0)
        self.componentsSubcontainer_wrapper.setLayout(self.componentsSubcontainer)
        
        self.alloy_list.itemPressed.connect(self.handleAlloySelection)
        self.summary_alloy_save.clicked.connect(self.saveAlloyInfo)
        self.summary_alloy_reset.clicked.connect(self.handleAlloySelection)
        self.summary_alloy_clear.clicked.connect(self.clearAlloySelection)
        self.summary_alloy_calculate.clicked.connect(self.sendCalculateSignal)
        self.recipe_mode_button.clicked.connect(self.showTab)
        self.alloy_add_button.clicked.connect(self.addAlloyToList)
        self.customMenubar_settings_button.clicked.connect(self.launchSettings)

    def launchSettings(self):
        settings_dialog = Settings()
        settings_dialog.exec()

    def addAlloyToList(self):
        self.clearAlloySelection()
        self.handleAlloySelection('New alloy')
        self.alloy_list.setCurrentItem(self.alloy_list.findItems('New alloy', Qt.MatchFlag.MatchExactly)[0])

    def showTab(self):
        self.frameRecipeMode.setHidden(not self.frameRecipeMode.isHidden())
        self.line.setHidden(not self.line.isHidden())
        if self.frameRecipeMode.isHidden() == True:
            self.setMinimumSize(250, 450)
            self.setMaximumSize(300, 650)
        else:
            self.setMinimumSize(1000, 600)
            self.setMaximumSize(1100, 800)

    def handleAlloySelection(self, alloy_selection):
        if alloy_selection == 'New alloy':
            self.alloy_list.addItem(alloy_selection)
            self.summary_alloy_type_input.setText(alloy_selection)
        else: 
            try:
                alloy_selection = self.alloy_list.currentItem().text()
                test_exception = alloy_selection + 'test'
                self.summary_alloy_type_input.setText(alloy_selection)
                if self.summary_results_ingots_output.text() == '':
                    self.summary_results_alloy_type_output.setText(alloy_selection)
                self.summary_ingots_input.setText(str(alloy_dict[alloy_selection].get('Ingots')))
                
                info_msg = 'You have chosen: ' + alloy_selection
                handleInfo(info_msg, dir_name)
            except:
                info_msg = 'Cannot reset the alloy selection, because nothing was selected.'
                handleInfo(info_msg, dir_name)
        if alloy_selection == 'New alloy':
            alloy_info_chosen = {}
            alloy_ore_mB_chosen = []
        else:
            alloy_info_chosen = alloy_dict[alloy_selection]
            alloy_ore_mB_chosen = list(alloy_info_chosen.get('mB/ore'))

        if oreInputWidget.instances != []:
            self.removeWidget('InputFields')
        summary_component_list = []
        if alloy_selection == 'New alloy':
            summary_component_list.append(oreInputWidget())
            new_alloy = summary_component_list[0]
            self.componentsSubcontainer.addWidget(new_alloy.layoutWidget)
            new_alloy.setParent(self.componentsSubcontainer_wrapper)
            i = len(oreInputWidget.instances)
            new_alloy.changeComponentInfo(i, alloy_info_chosen)
            new_alloy.adaptRatioSetup()
        else:
            for i in range(len(alloy_ore_mB_chosen)):
                summary_component_list.append(oreInputWidget())
                self.componentsSubcontainer.addWidget(summary_component_list[i].layoutWidget)
                summary_component_list[i].setParent(self.componentsSubcontainer_wrapper)
                summary_component_list[i].changeComponentInfo(i, alloy_info_chosen)
                summary_component_list[i].adaptRatioSetup()
        oreInputWidget.instances = summary_component_list
    
    def handleResults(self, alloy_type, alloy_results_dict, results_info_msg_buffer):
        self.summary_results_alloy_type_output.setText(alloy_type)
        self.summary_results_ingots_output.setText(alloy_results_dict[alloy_type].get('Final ingots'))
        alloy_results_mB_list = alloy_results_dict[alloy_type].get('mB/ore')
        if oreOutputWidget.instances != []:
            self.removeWidget('OutputFields')
        results_components_list = []
        for i in range(len(alloy_results_mB_list)):
            results_components_list.append(oreOutputWidget())
            results_components_list[i].changeComponentInfo(i, alloy_type, alloy_results_dict)
            self.resultsComponentsSubcontainer.addWidget(results_components_list[i].layoutWidget)
        oreOutputWidget.instances = results_components_list
        self.summary_results_description.setText("\n".join(results_info_msg_buffer))

    def removeWidget(self, *args):
        handleInfo('removeWidget() called', 'app')
        for arg in args:
            if type(arg) == str:
                source = arg
        if source != None and source == 'InputFields':
            if len(oreInputWidget.instances) > 0:
                for i in range(len(oreInputWidget.instances)):
                    oreInputWidget.validateInput(oreInputWidget.instances[i], ['ratioMin_input', 'ratioMax_input'], 'handleAlloySelection')
                    oreInputWidget.instances[i].layoutWidget.setParent(None)
                    self.componentsContainer.removeWidget(oreInputWidget.instances[i])
                    oreInputWidget.instances[i].layoutWidget.deleteLater()
                    oreInputWidget.instances[i].deleteLater()
                oreInputWidget.instances.clear()
            handleInfo('removeWidget() finished', 'app')
        elif source != None and source == 'OutputFields':
            for i in range(len(oreOutputWidget.instances)):
                instance = oreOutputWidget.instances[i]
                self.resultsComponentsContainer.removeWidget(instance.layoutWidget)
            oreOutputWidget.instances.clear()
            handleInfo('removeWidget() finished', 'app')
        
    def saveAlloyInfo(self):
        handleInfo('saveAlloyInfo() called', 'app')
        self.clearFocus
        if self.summary_alloy_type_input.text() == '' or self.summary_ingots_input.text() == '' or len(oreInputWidget.instances) == 0:
            handleInfo('saveAlloyInfo() stopped - invalid input', 'app')
            return
        else:
            for instance in oreInputWidget.instances:
                if instance.summary_ore_ratioMin_input.text() == '' or instance.summary_ore_ratioMax_input.text() == '' or instance.summary_ore_unit_input.text() == ('' or '0' or '00' or '000'):
                    handleInfo('saveAlloyInfo() stopped - invalid input', 'app')
                    msg_Box('saveAlloyInfo() stopped - invalid input', 'ERROR')
                    return
        current_alloy_type = self.summary_alloy_type_input.text()
        current_ingots = self.summary_ingots_input.text()
        current_mb_ore_list = []
        alloy_ratio_list = []
        current_alloy_dict = {}
        current_alloy_dict[current_alloy_type] = {}
        current_alloy_dict[current_alloy_type].update({'Ingots': current_ingots})
        for i, instance in enumerate(oreInputWidget.instances):
            current_mb_ore = instance.summary_ore_unit_input.text()
            current_mb_ore_list.append(current_mb_ore)
            current_ratioMin = instance.summary_ore_ratioMin_input.text()
            current_ratioMax = instance.summary_ore_ratioMax_input.text()
            alloy_ratio_list.append([current_ratioMin, current_ratioMax])
            print(alloy_ratio_list)
        current_alloy_dict[current_alloy_type].update({'mB/ore': current_mb_ore_list})
        current_alloy_dict[current_alloy_type].update({'ratio_ore': alloy_ratio_list})
        alloy_dict.update(current_alloy_dict)
        if current_alloy_dict == 'New alloy':
            del alloy_dict['New alloy']
            temp_removal = self.alloy_list.takeItem(self.alloy_list.row(self.alloy_list.findItems('New alloy', Qt.MatchFlag.MatchExactly)[0]))
            self.alloy_list.removeItemWidget(temp_removal)

        self.updateAlloyList(alloy_dict)
        saveAlloyInfo('AlloyOreInfo.txt', alloy_dict)
        handleInfo('saveAlloyInfo() finished', 'app')
        if current_alloy_type != 'New alloy':
            self.alloy_list.setCurrentRow(self.alloy_list.row(self.alloy_list.findItems(current_alloy_type, Qt.MatchFlag.MatchExactly)[0]))
        return 'saveAlloyInfo() finished'
    
    def updateAlloyList(self, alloy_dict):
        alloy_types_list = list(alloy_dict.keys())
        for i in range(len(alloy_types_list)):
            if self.alloy_list.findItems(alloy_types_list[i], Qt.MatchFlag.MatchExactly) == []:
                self.alloy_list.addItem(alloy_types_list[i])

    def clearAlloySelection(self):
        self.summary_alloy_type_input.setText('')
        if self.summary_results_ingots_output.text() == '':
            self.summary_results_alloy_type_output.setText('')
        self.summary_ingots_input.setText('')
        if oreInputWidget.instances != []:
            for i in range(len(oreInputWidget.instances)):
                instance = oreInputWidget.instances[i]
                self.componentsContainer.removeWidget(instance.layoutWidget)
        self.alloy_list.selectionModel().clear()
        self.removeWidget('InputFields')
    
    def sendCalculateSignal(self):
        if self.saveAlloyInfo() == None:
            return
        try:
            if (self.alloy_list.currentItem().text() != None or self.alloy_list.currentItem().text()) != '' and self.alloy_list.currentItem().text() == self.summary_alloy_type_input.text():
                alloy_type = self.alloy_list.currentItem().text()
                alloy_info_chosen = alloy_dict.get(alloy_type)
                alloy_results_dict = {}
                alloy_results_dict, results_info_msg_buffer = getAlloyRatio(alloy_type, alloy_info_chosen)
                self.handleResults(alloy_type, alloy_results_dict, results_info_msg_buffer)
            else:
                info_msg = 'It seems you changed something from the preset. Do you want to overwrite the current preset?'
                handleInfo(info_msg, dir_name)
                msg_Box(info_msg, 'SAVE')
        except:
            info_msg = 'Cannot calculate, because nothing was selected. Please, select an alloy from the left hand side.'
            handleInfo(info_msg, dir_name)
            msg_Box(info_msg, 'INFO')

class Settings(QDialog, Ui_SettingsDialog):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        settings_dict = getSettingsInfo('settings.txt')
        oreInputWidget.decimalDisplayChoice = settings_dict.get('decimal_delimiter')
        if oreInputWidget.decimalDisplayChoice == ',':
            self.radioButton1.setChecked(True)
        else:
            self.radioButton2.setChecked(True)

        apply_button = self.buttonBox.button(self.buttonBox.StandardButton.Apply)
        if apply_button:
            apply_button.clicked.connect(self.updateDecimals)
            apply_button.clicked.connect(self.accept)
        
        info_msg = 'Settings read from file: ' + str(settings_dict)
        handleInfo(info_msg, dir_name)
    
    def updateDecimals(self):
        if self.radioButton1.isChecked() == True:
            settings_dict['decimal_delimiter'] = ','
            for i, instance in enumerate(oreInputWidget.instances):
                instance.decimalDisplayChoice = settings_dict.get('decimal_delimiter')
                instance.regex = QRegularExpression(r"\d{3}|\d{1,2}\,\d{2}|\d{1,2}\,\d{1}|\d{1,2}\,|\d{1,2}|\d{0}")
                instance.validatorRatio = QRegularExpressionValidator(instance.regex)
                instance.adaptRatioSetup()
            saveSettingsInfo('settings.txt', settings_dict)
        else:
            settings_dict['decimal_delimiter'] = '.'
            for i, instance in enumerate(oreInputWidget.instances):
                instance.decimalDisplayChoice = settings_dict.get('decimal_delimiter')
                instance.regex = QRegularExpression(r"\d{3}|\d{1,2}\.\d{2}|\d{1,2}\.\d{1}|\d{1,2}\.|\d{1,2}|\d{0}")
                instance.validatorRatio = QRegularExpressionValidator(instance.regex)
                instance.adaptRatioSetup()
            saveSettingsInfo('settings.txt', settings_dict)
        if window.alloy_list.currentItem() != None:
            #alloy_selection = window.alloy_list.currentItem().text()   # TODO Maybe make it a choice, if changing the comma/dot also resets the input fields (the numbers)
            #alloy_info_chosen = alloy_dict[alloy_selection]            # Right now, it just keeps the value.
            for instance in oreInputWidget.instances:
                #instance.changeComponentInfo(ore_number, alloy_info_chosen)
                instance.adaptRatioSetup()

class MessageBox(QDialog, Ui_info_dialog):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

class oreInputWidget(QFrame, Ui_oreInputWdgt):
    instances = []
    remind_input_field = 1
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        settings_dict = getSettingsInfo('settings.txt')
        self.decimalDisplayChoice = settings_dict.get('decimal_delimiter')
        if self.decimalDisplayChoice == '.':
            self.regex = QRegularExpression(r"\d{3}|\d{1,2}\.\d{2}|\d{1,2}\.\d{1}|\d{1,2}\.|\d{1,2}|\d{0}")
        elif self.decimalDisplayChoice == ',':
            self.regex = QRegularExpression(r"\d{3}|\d{1,2}\,\d{2}|\d{1,2}\,\d{1}|\d{1,2}\,|\d{1,2}\d{0}")
        self.validatorRatio = QRegularExpressionValidator(self.regex)
        self.summary_ore_ratioMin_input.setValidator(self.validatorRatio)
        self.summary_ore_ratioMax_input.setValidator(self.validatorRatio)
        self.summary_ore_unit_input.setValidator(QRegularExpressionValidator(QRegularExpression(r"\d{1,3}")))

        self.summary_ore_ratioMin_input.editingFinished.connect(lambda field_type=['ratioMin_input'], source=['returnPressed']: self.validateInput(field_type, source))
        self.summary_ore_ratioMax_input.editingFinished.connect(lambda field_type=['ratioMax_input'], source=['returnPressed']: self.validateInput(field_type, source))
        self.summary_ore_ratioMin_input.textEdited.connect(lambda text, field_type=['ratioMin_input'], source=['textEdited']: self.validateInput(field_type, source))
        self.summary_ore_ratioMax_input.textEdited.connect(lambda text, field_type=['ratioMax_input'], source=['textEdited']: self.validateInput(field_type, source))
        self.addOreInput.clicked.connect(self.addOreInputField)
        self.summary_ore_delete.clicked.connect(self.removeOreInputField)

    def addOreInputField(self):
        if len(oreInputWidget.instances) < 3:
            new_ore_input_field = oreInputWidget()
            window.componentsSubcontainer.addWidget(new_ore_input_field.layoutWidget)
            new_ore_input_field.setParent(window.componentsSubcontainer_wrapper)
            self.temp_instances = oreInputWidget.instances
            oreInputWidget.instances.append(new_ore_input_field)
            alloy_selection = window.alloy_list.currentItem().text()
            if alloy_selection == 'New alloy':
                alloy_dict[alloy_selection] = {}
            alloy_info_chosen = alloy_dict[alloy_selection]
            print(alloy_selection, alloy_info_chosen)
            for ore_number, instance in enumerate(oreInputWidget.instances):
                if new_ore_input_field == instance:
                    new_ore_input_field.changeComponentInfo(ore_number, {})
            print(oreInputWidget.instances)

    def removeOreInputField(self):
        if len(oreInputWidget.instances) > 2:
            self.validateInput(['ratioMin_input', 'ratioMax_input'], 'handleAlloySelection')
            self.layoutWidget.setParent(None)
            window.componentsContainer.removeWidget(self)
            oreInputWidget.instances.remove(self)
            self.layoutWidget.deleteLater()
            self.deleteLater()
            alloy_selection = window.alloy_list.currentItem().text()
            alloy_info_chosen = alloy_dict[alloy_selection]
            for ore_number, instance in enumerate(oreInputWidget.instances):
                instance.changeComponentInfo(ore_number, alloy_info_chosen)
            print(oreInputWidget.instances)

    def changeComponentInfo(self, ore_number, alloy_info_chosen):
        ore_name = '- ore' + str(ore_number+1) + ': '
        self.summary_ore_name.setText(ore_name)

        if alloy_info_chosen != {}:
            self.summary_ore_unit_input.setText(alloy_info_chosen.get('mB/ore')[ore_number])
            self.summary_ore_ratioMin_input.setText(alloy_info_chosen.get('ratio_ore')[ore_number][0])
            self.summary_ore_ratioMax_input.setText(alloy_info_chosen.get('ratio_ore')[ore_number][1])
        else:
            self.summary_ore_unit_input.setText('')
            self.summary_ore_ratioMin_input.setText('')
            self.summary_ore_ratioMax_input.setText('')

    def validateInput(self, field_types, sources):
        for source in sources:
            for field_type in field_types:
                if source == 'textEdited':
                    if field_type == 'ratioMin_input':
                        self.summary_ore_ratioMin_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
                        self.summary_ore_ratioMin_input.setInputMask('')
                        self.summary_ore_ratioMin_input.setValidator(self.validatorRatio)
                        current_text = self.summary_ore_ratioMin_input.text()
                        print('Current text: ' + current_text + '')
                    elif field_type == 'ratioMax_input':
                        self.summary_ore_ratioMax_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
                        self.summary_ore_ratioMax_input.setInputMask('')
                        self.summary_ore_ratioMax_input.setValidator(self.validatorRatio)
                        current_text = self.summary_ore_ratioMax_input.text()
                        print('Current text: ' + current_text)
                elif source == 'returnPressed' or source == 'sendCalculateSignal' or source == 'handleAlloySelection':
                    if field_type == 'ratioMin_input':
                        previous_text = self.summary_ore_ratioMin_input.text()
                        self.summary_ore_ratioMin_input.setInputMask('')
                        current_text = self.summary_ore_ratioMin_input.text()
                        self.summary_ore_ratioMin_input.setValidator(self.validatorRatio)
                        try:
                            self.autofillInput(current_text, field_type)
                            new_text = self.summary_ore_ratioMin_input.text()
                            print('Current text: ' + new_text)
                        except:
                            self.summary_ore_ratioMin_input.setText(previous_text)
                            print('Previous text: ' + previous_text)
                        self.summary_ore_ratioMin_input.clearFocus()
                    elif field_type == 'ratioMax_input':
                        previous_text = self.summary_ore_ratioMax_input.text()
                        self.summary_ore_ratioMax_input.setInputMask('')
                        self.summary_ore_ratioMax_input.setValidator(self.validatorRatio)
                        current_text = self.summary_ore_ratioMax_input.text()
                        try:
                            self.autofillInput(current_text, field_type)
                            new_text = self.summary_ore_ratioMax_input.text()
                            print('Current text: ' + new_text)
                        except:
                            self.summary_ore_ratioMax_input.setText(previous_text)
                            print('Current text: ' + previous_text)
                        self.summary_ore_ratioMax_input.clearFocus()
        if source == 'handleAlloySelection' or source == 'sendCalculateSignal' or source == 'returnPressed':
            if self.summary_ore_ratioMin_input.text() == '':
                err_msg = 'Be advised: ratioMin has to be a number. Your input field was empty.'
                handleError(err_msg, 'app')
                if oreInputWidget.remind_input_field == 1:
                    msg_Box(err_msg + ' You will not be reminded again.', 'ERROR')
                    oreInputWidget.remind_input_field = 0
                self.summary_ore_ratioMin_input.setFocus()
                return False       
            elif self.summary_ore_ratioMax_input.text() == '':
                err_msg = 'Be advised: ratioMax has to be a number. Your input field was empty.'
                handleError(err_msg, 'app')
                if oreInputWidget.remind_input_field == 1:
                    msg_Box(err_msg + ' You will not be reminded again.', 'ERROR')
                    oreInputWidget.remind_input_field = 0
                self.summary_ore_ratioMax_input.setFocus()
                return False
            else:
                ratioMin = float(self.summary_ore_ratioMin_input.text().replace(',', '.'))
                ratioMax = float(self.summary_ore_ratioMax_input.text().replace(',', '.'))
                if ratioMin >= ratioMax:
                    err_msg = 'Be advised: ratioMin has to be smaller than ratioMax. You inserted ratioMin=' + self.summary_ore_ratioMin_input.text() + ' and ratioMax=' + self.summary_ore_ratioMax_input.text() + '. Check the input fields and try again.'
                    handleError(err_msg, 'app')
                    msg_Box(err_msg, 'ERROR')
                    self.summary_ore_ratioMin_input.setText('')
                    self.summary_ore_ratioMin_input.setFocus()
                    return False
    
    def autofillInput(self, current_text, field_type):
        if current_text == '':
            return False
        else:
            if field_type == 'ratioMin_input':
                if self.decimalDisplayChoice not in current_text:
                    if int(current_text) > 100:
                        self.summary_ore_ratioMin_input.setText('100')
                        self.summary_ore_ratioMin_input.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                    elif int(current_text) == 100:
                        self.summary_ore_ratioMin_input.setText('100')
                        self.summary_ore_ratioMin_input.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                    elif int(current_text) < 100:
                        text = current_text + self.decimalDisplayChoice + '00'
                        self.summary_ore_ratioMin_input.setText(text)
                        self.summary_ore_ratioMin_input.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                elif current_text[-1] == self.decimalDisplayChoice:
                    text = current_text + '00'
                    self.summary_ore_ratioMin_input.setText(text)
                    self.summary_ore_ratioMin_input.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                elif current_text[-2] == self.decimalDisplayChoice:
                    text = current_text + '0'
                    self.summary_ore_ratioMin_input.setText(text)
                    self.summary_ore_ratioMin_input.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            elif field_type == 'ratioMax_input':
                if self.decimalDisplayChoice not in current_text:
                    if int(current_text) > 100:
                        self.summary_ore_ratioMax_input.setText('100')
                        self.summary_ore_ratioMax_input.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                    elif int(current_text) == 100:
                        self.summary_ore_ratioMax_input.setText('100')
                        self.summary_ore_ratioMax_input.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                    elif int(current_text) < 100:
                        text = current_text + self.decimalDisplayChoice + '00'
                        self.summary_ore_ratioMax_input.setText(text)
                        self.summary_ore_ratioMax_input.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                elif current_text[-1] == self.decimalDisplayChoice:
                    text = current_text + '00'
                    self.summary_ore_ratioMax_input.setText(text)
                    self.summary_ore_ratioMax_input.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                elif current_text[-2] == self.decimalDisplayChoice:
                    text = current_text + '0'
                    self.summary_ore_ratioMax_input.setText(text)
                    self.summary_ore_ratioMax_input.setAlignment(Qt.AlignmentFlag.AlignHCenter)

    def adaptRatioSetup(self):
        self.validatorRatio = QRegularExpressionValidator(self.regex)
        self.summary_ore_ratioMin_input.setValidator(self.validatorRatio)
        self.summary_ore_ratioMax_input.setValidator(self.validatorRatio)
        if self.decimalDisplayChoice == '.':
            adapted_text = self.summary_ore_ratioMin_input.text().replace(',', self.decimalDisplayChoice)
            self.summary_ore_ratioMin_input.setText(adapted_text)
            adapted_text = self.summary_ore_ratioMax_input.text().replace(',', self.decimalDisplayChoice)
            self.summary_ore_ratioMax_input.setText(adapted_text)
        elif self.decimalDisplayChoice == ',':
            adapted_text = self.summary_ore_ratioMin_input.text().replace('.', self.decimalDisplayChoice)
            self.summary_ore_ratioMin_input.setText(adapted_text)
            adapted_text = self.summary_ore_ratioMax_input.text().replace('.', self.decimalDisplayChoice)
            self.summary_ore_ratioMax_input.setText(adapted_text)

class oreOutputWidget(QFrame, Ui_oreOutputWdgt):
    instances = []
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
    
    def changeComponentInfo(self, ore_number, alloy_type, alloy_results_dict, *args):
        ore_name = '- ore' + str(ore_number+1) + ':'
        self.summary_results_ore_name.setText(ore_name)
        self.summary_results_ore_number_output.setText(alloy_results_dict[alloy_type].get('n')[ore_number])
        self.summary_results_ore_unit_output.setText(alloy_results_dict[alloy_type].get('mB/ore')[ore_number])
        self.summary_results_ore_ratioMin_output.setText(alloy_results_dict[alloy_type].get('final_ratio_ore')[ore_number])

def msg_Box(msg, type):
    msg_Box = MessageBox()
    if type == 'ERROR':
        msg_Box.setWindowTitle("Error!")
        msg_Box.info_label.setText(msg + '\n\nDetails: \n' + "\n\n".join(errorOutputs))
    elif type == 'INFO':
        msg_Box.setWindowTitle("Info.")
        msg_Box.info_label.setText(msg)
    elif type == 'SAVE':
        msg_Box = QMessageBox()
        msg_Box.setWindowTitle("Save preset changes.")
        msg_Box.setText(msg)
        font = QFont()
        font.setFamily('Courier')
        msg_Box.setFont(font)
        #save_new_button = msg_Box.addButton('Save new', QMessageBox.ButtonRole.YesRole)
        overwrite_button = msg_Box.addButton('Overwrite', QMessageBox.ButtonRole.ApplyRole)
        cancel_button = msg_Box.addButton('No', QMessageBox.ButtonRole.NoRole)
        #save_new_button.clicked.connect(window.saveAlloyInfo)
        overwrite_button.clicked.connect(window.saveAlloyInfo)
    if type != None or type != '':
        msg_Box.exec()

def importAlloyInfo():
    try:
        info_msg = 'Calling ' + getAlloyOreInfo.__name__ + '()'
        handleInfo(info_msg, dir_name)

        alloy_types, alloy_dict = getAlloyOreInfo(skipChoice=True)
        info_msg = 'Succesfully imported all alloy info from AlloyOreInfo.txt'
        handleInfo(info_msg, dir_name)
        return alloy_types, alloy_dict
    except:
        err_msg = 'Something went wrong while initializing the Alloy Ore Info list. Please check the logfiles for app and TFG and restart the program.'
        handleError(err_msg, dir_name)
        msg_Box(err_msg, 'ERROR')
        return [], []

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()

window.show()

handleInfo('app.py initializing', dir_name)
alloy_types, alloy_dict = importAlloyInfo()
window.alloy_list.addItems(alloy_types)
handleInfo('app.py initialized', dir_name)

app.exec()