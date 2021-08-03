from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QToolBar, QAction, QPushButton, QLabel, \
    QWidget, QVBoxLayout, QGroupBox, QTabWidget, QLineEdit, QFormLayout, QStatusBar, QListWidget, QAbstractItemView, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
import sys
import os
import shutil
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.archive_retriever import ArchiveGetter
from src.dataWrapper import DataWrapper
from src.dataPusher import DataPusher

selected_list_of_files = []
selection_flag = False
second_trial_file_list = list()


class WelcomeWindow(QMainWindow):
    def __init__(self):
        # constructor for the window. Set basic parameters
        super(WelcomeWindow, self).__init__()
        self.setGeometry(250, 100, 800, 1000)
        self.setFixedSize(950, 600)
        self.setWindowTitle("pyMongolator")
        self.initial_screen()
        "add tab view in main window"
        self.tab_widget = TabOptionsWidget(self)
        self.setCentralWidget(self.tab_widget)
        self.show()

    def initial_screen(self):
        'background image and screen'
        welcome_label1 = QLabel(self)
        pixmap1 = QPixmap('C:/Users/Souvik.Roy/Documents/IOP_PythonFiles_Souvik/gi_logo_resized.png')
        welcome_label1.setPixmap(pixmap1)
        self.setCentralWidget(welcome_label1)
        self.resize(pixmap1.width(), pixmap1.height())


def show_details_from_retrieved_dict(dict_retrvd):
    'str_check to find out whether the count or the names are reqd'
    details_str = "Found:\t"
    for key, val in dict_retrvd.items():
        count = len(val) if len(val) > 0 else 0
        details_str += key + " files : " + str(count)+ "\n\t"
    return details_str[:-4]


class FileEdit(QLineEdit):
    def __init__(self, parent):
        super(FileEdit, self).__init__(parent)

        self.setDragEnabled(True)

    def dragEnterEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dropEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            filepath = str(urls[0].path())[1:]
            # any file type here
            # if filepath[-4:].upper() == ".txt":
            self.setText(filepath)
            # else:
            #     dialog = QMessageBox()
            #     dialog.setWindowTitle("Error: Invalid File")
            #     dialog.setText("Only .txt files are accepted")
            #     dialog.setIcon(QMessageBox.Warning)
            #     dialog.exec_()


class SecondWindow(QWidget):

    def __init__(self, list_input_all_files):
        super(SecondWindow, self).__init__()
        self.selected_list = []
        self.list_of_files = list_input_all_files
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout(self)
        self.list_widget = QListWidget(self)
        self.search_textbox = QLineEdit(self)

        self.search_btn = QPushButton('Search', self)
        self.search_btn.setFixedWidth(50)
        self.search_btn.setStyleSheet("background-color: blue; color:white")

        self.list_widget.addItems(self.list_of_files)

        'enabling multiple selection'
        self.list_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        'adding ADD button'
        self.add_btn = QPushButton('Add', self)
        self.add_btn.resize(50, 50)
        self.add_btn.setFixedWidth(85)
        self.add_btn.setStyleSheet("background-color: blue; color:white")
        'adding widgets in window'
        vbox.addWidget(self.search_textbox)
        vbox.addWidget(self.search_btn, alignment=Qt.AlignRight)
        vbox.addWidget(self.list_widget)
        vbox.addWidget(self.add_btn, alignment=Qt.AlignCenter)

        self.setLayout(vbox)

        self.setGeometry(200, 200, 700, 350)
        self.setWindowTitle('pyMongolator')
        self.show()

        'Signals'
        self.add_btn.clicked.connect(self.on_add_clicked)
        self.list_widget.itemSelectionChanged.connect(self.get_list_of_files)
        self.search_btn.clicked.connect(self.on_textChanged)

    def setter(self, templist_container):
        self.selected_list = templist_container

    def getter(self):
        return self.selected_list

    def binary_search(self, arr, l, r, x):
        selected_search_list = []
        while l <= r:
            mid = l + (r - l) // 2;
            # Check if x is present at mid
            if x in arr[mid]:
                selected_search_list.append(arr[mid])
                return mid
            # If x is greater, ignore left half
            elif arr[mid] < x:
                l = mid + 1
            # If x is smaller, ignore right half
            else:
                r = mid - 1
        # If we reach here, then the element
        # was not present
        return -1

    def filter(self, text, list_to_search_from):
        return_list = []
        for each in list_to_search_from:
            if text.lower() in each.lower():
                return_list.append(each)
        print(len(return_list))
        return return_list

    def on_textChanged(self):
        self.search_text = self.search_textbox.text()
        if len(self.filter(self.search_text, self.list_of_files)):
            self.list_widget.clear()
            self.list_widget.addItems(self.filter(self.search_text, self.list_of_files))
        else:
            QMessageBox.information(self, "pyMongolator", "Notification: No Results found!")

    def on_add_clicked(self):
        selected_items_from_listwidget = self.list_widget.selectedItems()
        selected_list_of_files = [i.text() for i in list(selected_items_from_listwidget)]
        QMessageBox.information(self, "pyMongolator", "Notification: File Selected")
        self.setter(self.selected_files_from_listWidget)
        self.close()

    def get_list_of_files(self):
        self.selected_items_from_listwidget = self.list_widget.selectedItems()
        self.selected_files_from_listWidget = [i.text() for i in list(self.selected_items_from_listwidget)]
        # static_list_selected_files = self.selected_files_from_listWidget
        second_trial_file_list = self.selected_files_from_listWidget


class TabOptionsWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.selected_files = list()
        self.to_prepare_list = []
        self._already_prepared_list = []
        self.converted_list = list()
        self._flag_for_prepare = False
        self._flag_for_second_window = False
        self._flag_for_display_prepare = False
        self._flag_for_no_items_selected_in_liswidget = True
        self._flag_for_selection_in_listwidget = False
        self._flag_for_clear_selection = False
        self._flag_second_window_already_loaded = False
        stylesheet = """ 
            QTabBar::tab:selected {background: white;}
            QTabWidget>QWidget>QWidget{background: white;}
            """

        self.setStyleSheet(stylesheet)
        'initialize tab screens'
        self.tabs = QTabWidget()
        self.tab1_home = QWidget()
        self.tab15_fileSaver = QWidget()
        self.tab2_arch = QWidget()
        self.tab3_prepare = QWidget()
        self.tab4_push_db = QWidget()

        'add tabs'
        self.tabs.addTab(self.tab1_home, "Home")
        self.tabs.addTab(self.tab15_fileSaver, "SaveAs")
        self.tabs.addTab(self.tab2_arch, "Archive")
        self.tabs.addTab(self.tab3_prepare, "Prepare")
        self.tabs.addTab(self.tab4_push_db, "ConnectDB")

        self.home_tab_UI()
        self.save_as_tab_UI()
        self.archive_tab_UI()
        self.prepare_tab_UI()
        self.push_into_db_tab_UI()

        "add tabs to widget"
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        "arbit variables ot be used later"
        self._archive_address_to_save = ""
        self._storage_dict_for_retrieved_files = {}

        # Signals #
        self.connect_btn.clicked.connect(self.onConnectArchiveBtnClicked)
        self.arch_address.textChanged.connect(self.onArchAddressChanged)
        self.show_details_btn.clicked.connect(self.onShowDetailsBtnClicked)
        self.prepare_btn.clicked.connect(self.onPrepareBtnClicked)
        # self.connect(self.tabs, pyqtSignal('currentChanged(int'),self.selector_function)
        self.tabs.currentChanged.connect(self.selector_function)
        self.clear_prepare_btn.clicked.connect(self.onClearSelectionListClicked)
        self.drgdrop_generate_button.clicked.connect(self.onDragdropGenerateBtnClicked)
        self.autofill_btn.clicked.connect(self.onAutoFillPrepareBtnClicked)
        self.reset_btn.clicked.connect(self.onResetFieldsBtnClicked)
        self.reset_saveAs_btn.clicked.connect(self.onResetSaveAsBtnClicked)
        self.list_widget_selected.currentItemChanged.connect(self.selectionInListOfPrepareChanged)
        self.list_widget_selected.itemSelectionChanged.connect(self.selectionChangedListWisgetPrepare)
        # self.list_of_files_listWidget.itemSelectionChanged.connect(self.get_list_of_files)
        self.push_into_DB_btn.clicked.connect(self.onPushDBbtnClicked)

    def selector_function(self, selected_index):
        if selected_index == 0:
            print("home tab selected")
            self._flag_for_prepare = False
            # self._flag_for_second_window = False
        elif selected_index == 1:
            print("save as tab selected")
            self._flag_for_prepare = False
            # self._flag_for_second_window = False
        elif selected_index == 2:
            self._flag_for_prepare = False
        elif selected_index == 3:
            'when first time going from archive to prepare tab after selcting files, this flag_for_display_prepare is True; also True when selection is amd in the second window'
            print('xxx:', self._flag_for_display_prepare)
            self.refresh_prepare_list()
            self._flag_for_second_window = False
            if not self._flag_for_display_prepare:
                self.autofill_btn.setEnabled(False)
                self.exp_type.setEnabled(False)
                self.etchant.setEnabled(False)
                self.etc_time.setEnabled(False)
                self.magnification.setEnabled(False)
                self.sample_no.setEnabled(False)
                self.load_mharndess.setEnabled(False)
                self.din_std.setEnabled(False)
                self.psd.setEnabled(False)
                self.type_psd.setEnabled(False)
                self.mfg_powder.setEnabled(False)
                self.charge_powder.setEnabled(False)
                self.lot_powder.setEnabled(False)
                self.default_psd_powder.setEnabled(False)
                self.additional_info.setEnabled(False)
            # seladf.hbox_spec.setEnabled(False)
            # self.generic_view_overall.setEnabled(False)
            else:
                self.autofill_btn.setEnabled(True)
                self.exp_type.setEnabled(True)
                self.etchant.setEnabled(True)
                self.etc_time.setEnabled(True)
                self.magnification.setEnabled(True)
                self.sample_no.setEnabled(True)
                self.load_mharndess.setEnabled(True)
                self.din_std.setEnabled(True)
                self.psd.setEnabled(True)
                self.type_psd.setEnabled(True)
                self.mfg_powder.setEnabled(True)
                self.charge_powder.setEnabled(True)
                self.lot_powder.setEnabled(True)
                self.default_psd_powder.setEnabled(True)
                self.additional_info.setEnabled(True)
            if not self._flag_for_prepare:
                'this is executed when no selection is done in the second window, and prepare tab is clicked while changing tabs: no selection done in second window'
                print("prepare tab")
                print('when this is find out')
            else:
                'when selection is made in the second window'
                print('find when this is printed')
                self.load_prepare_list()
                self.refresh_prepare_list()
                self._flag_for_display_prepare= True
        elif selected_index == 4:
            print("data base tab selected")
            self._flag_for_prepare = False
            # self._flag_for_second_window = False

    def home_tab_UI(self):
        "add code for each tab view: contents to be added"
        self.tab1_home.layout = QVBoxLayout(self)

        'welcome label'
        welcome_text_label = QLabel("pyMongolator")
        welcome_text_label.setFont(QFont("Calibri", 20))
        welcome_text_label.setAlignment(Qt.AlignCenter)
        welcome_text_label.setStyleSheet("font: bold; color: black;")

        'label about introduction of app'
        about_text_label = QLabel(self)
        about_text_label.setText("About: pyMongolator is an application developed as part of the Master Thesis of Souvik Roy under the guidance of Dr. Ing. Iris Raffeis and M.Eng. Frank Kyeremeh at the Giesserei Insitut, RWTH Aachen and Forschungscampus Digital Photonic Production der RWTH Aachen")
        about_text_label.setWordWrap(True)
        about_text_label.setFont(QFont("Calibri", 10))
        about_text_label.setAlignment(Qt.AlignJustify)
        about_text_label.setStyleSheet("color: black;")

        'label about functionality brief'
        func_text_label = QLabel(self)
        func_text_label.setText("Welcome to the pyMongolator. This is an application designed as a partial implementation of project Internet of Production, primarily aimed at in-situ automated data saving for different materials in a database. \n The application pyMongoPopulator is designed in Python, and is associated with data saving in MongoDb, the functionality is as follows: \n-     Saving of experiemtnal files in-situ in the Archive \n-     Creating metadata of the files under selection pin the archive\n-     Automatic saving of the metadata in the MongoDB  Database")
        func_text_label.setWordWrap(True)
        func_text_label.setFont(QFont("Calibri", 10))
        func_text_label.setAlignment(Qt.AlignJustify)
        func_text_label.setStyleSheet("color: black;")

        'copyright label'
        copyright_label = QLabel(self)
        copyright_label.setText("© Roy,Souvik (souvik.roy@rwth-aachen.de)")
        copyright_label.setFont(QFont("Calibri", 10))
        copyright_label.setStyleSheet("color: black")

        'image'
        welcome_img_label_iop = QLabel(self)
        pixmap_iop = QPixmap('/src\iop-rwth-logo-resized.jpg')
        welcome_img_label_iop.setPixmap(pixmap_iop)
        welcome_img_label_iop.setPixmap(QPixmap("/src\iop-rwth-logo-resized.jpg"))
        welcome_img_label_iop.setFixedSize(250, 80)

        hbox = QHBoxLayout(self)
        welcome_img_label1 = QLabel(self)
        pixmap1 = QPixmap('/src\dpp_logo_resized.png')
        welcome_img_label1.setPixmap(pixmap1)
        welcome_img_label1.setPixmap(QPixmap("/src\dpp_logo_resized.png"))
        welcome_img_label1.setFixedSize(250, 80)

        welcome_img_label2 = QLabel(self)
        pixmap2 = QPixmap('/src\gi_logo_resized.jpg')
        welcome_img_label2.setPixmap(pixmap2)
        welcome_img_label2.setPixmap(QPixmap("/src\gi_logo_resized.jpg"))
        welcome_img_label2.setFixedSize(250, 80)
        hbox.addWidget(welcome_img_label1)
        hbox.addWidget(welcome_img_label_iop)
        hbox.addWidget(welcome_img_label2)

        'rwth image'
        rwth_img2_label = QLabel(self)
        pixmap_rwth = QPixmap('/src\RWTH-Aachen-University.jpg')
        rwth_img2_label.setPixmap(pixmap_rwth)
        rwth_img2_label.setPixmap(
            QPixmap("/src\RWTH-Aachen-University.jpg"))
        rwth_img2_label.setFixedSize(900, 400)

        #  self.tab1_home.layout.addWidget(welcome_img_label_iop, alignment=Qt.AlignCenter)
        self.tab1_home.layout.addWidget(welcome_text_label)
        self.tab1_home.layout.addWidget(func_text_label)
        self.tab1_home.layout.addWidget(about_text_label)
        self.tab1_home.layout.addWidget(copyright_label, alignment=Qt.AlignLeft)
        self.tab1_home.layout.addLayout(hbox)
        self.tab1_home.layout.addWidget(rwth_img2_label)
        self.tab1_home.setLayout(self.tab1_home.layout)

    def save_as_tab_UI(self):
        self.tab15_fileSaver.layout = QVBoxLayout(self)
        'intro label'
        intro_label = QLabel('Files can be dragged and dropped here. With some additional information, the file will be named conventionally and saved into the archive. Files from the archive can then be sent to the database in a later stage. The necessary fields are marked with a *')
        intro_label.setFont(QFont("Calibri", 10))
        intro_label.setWordWrap(True)
        intro_label.setStyleSheet("color: black;")
        intro_label.setFixedHeight(50)

        'drag-drop box'
        drag_drop_groupbox = QGroupBox('File Save')
        'left part for drag and drop'
        left_vbox = QVBoxLayout(self)
        descr_drg_drop_label = QLabel('Drop selected file into the text box:')
        descr_drg_drop_label.setFixedHeight(20)
        self.drgDrop_file = FileEdit(self)
        self.drgDrop_file.setFixedHeight(75)
        self.drgDrop_file.setReadOnly(True)

        address_archive_label = QLabel('Address of the archive * :')
        address_archive_label.setFixedHeight(20)
        self.address_archive = QLineEdit(self)

        left_vbox.addWidget(QLabel('\n'))
        left_vbox.addWidget(descr_drg_drop_label)
        left_vbox.addWidget(self.drgDrop_file)
        left_vbox.addWidget(address_archive_label)
        left_vbox.addWidget(self.address_archive)

        'right part for filling details'
        right_vbox = QVBoxLayout(self)
        "name of operator"
        op_label = QLabel('Name of Operator * :')
        self.operator = QLineEdit(self)
        'date of operation'
        date_label = QLabel('Date (DD-MM-YYYY) * :')
        self.date = QLineEdit(self)
        'type of test'
        type_label = QLabel('Type of Experiment * :')
        self.type_test = QLineEdit(self)
        'material'
        material_label = QLabel('Material * :')
        self.material = QLineEdit(self)

        right_vbox.addWidget(material_label)
        right_vbox.addWidget(self.material)
        right_vbox.addWidget(type_label)
        right_vbox.addWidget(self.type_test)
        right_vbox.addWidget(op_label)
        right_vbox.addWidget(self.operator)
        right_vbox.addWidget(date_label)
        right_vbox.addWidget(self.date)

        middle_layer = QHBoxLayout(self)
        middle_layer.addLayout(left_vbox)
        middle_layer.addLayout(right_vbox)
        drag_drop_groupbox.setLayout(middle_layer)

        'generate button'
        self.drgdrop_generate_button = QPushButton(self)
        self.drgdrop_generate_button.setText("Generate")
        self.drgdrop_generate_button.setFixedWidth(85)
        self.drgdrop_generate_button.setGeometry(100, 200, 80, 50)
        self.drgdrop_generate_button.setStyleSheet("background-color: blue; color:white")
        'reset fields'
        self.reset_saveAs_btn = QPushButton()
        self.reset_saveAs_btn.setText("Reset")
        self.reset_saveAs_btn.setFixedWidth(85)
        self.reset_saveAs_btn.setStyleSheet("background-color: blue; color:white")

        'hbox for containing both buttons'
        hbox_save_as_bottom = QHBoxLayout()
        hbox_save_as_bottom.addWidget(self.reset_saveAs_btn)
        hbox_save_as_bottom.addWidget(self.drgdrop_generate_button)


        self.tab15_fileSaver.layout.addWidget(intro_label)
        self.tab15_fileSaver.layout.addWidget(drag_drop_groupbox)
        # self.tab15_fileSaver.layout.addWidget(self.drgdrop_generate_button, alignment=Qt.AlignHCenter)
        self.tab15_fileSaver.layout.addLayout(hbox_save_as_bottom)
        self.tab15_fileSaver.setLayout(self.tab15_fileSaver.layout)

    def archive_tab_UI(self):
        self.tab2_arch.layout = QVBoxLayout(self)

        'description label'
        descr_text_label = QLabel(self)
        descr_text_label.setText("The archive can be glanced from here. The Unique Address of the Archive has to be manually entered.\n \n")
        descr_text_label.setFont(QFont("Calibri", 10))
        descr_text_label.setWordWrap(True)
        descr_text_label.setStyleSheet("color: black;")
        descr_text_label.setFixedHeight(40)

        'instruction label'
        instruct_label = QLabel("Enter the address of the archive")
        instruct_label.setFont(QFont("Calibri", 10))
        instruct_label.setAlignment(Qt.AlignLeft)
        instruct_label.setStyleSheet("color: black;")
        instruct_label.setFixedSize(200, 20)

        'space to manually enter address of archive'
        self.arch_address = QLineEdit()

        'connect button'
        self.connect_btn = QPushButton(self)
        self.connect_btn.setText("Connect")
        self.connect_btn.setFixedWidth(85)
        self.connect_btn.setStyleSheet("background-color: blue; color:white")

        'label to display number of files and stuff'
        self.info_abt_files = QLabel()
        self.info_abt_files.setEnabled(False)
        self.info_abt_files.setFixedSize(200, 100)

        'show details btn'
        self.show_details_btn = QPushButton("Show Details")
        self.show_details_btn.setFixedWidth(85)
        self.show_details_btn.setStyleSheet("background-color: blue, color:white")
        self.show_details_btn.setVisible(False)
        'info and show details btn in a hbox for better viewing'
        hbox_info_details = QHBoxLayout()
        hbox_info_details.addWidget(self.info_abt_files)
        hbox_info_details.addWidget(self.show_details_btn)
        'image'
        rwth_img2_label = QLabel(self)
        pixmap_rwth = QPixmap('/src\RWTH-Aachen-University.jpg')
        rwth_img2_label.setPixmap(pixmap_rwth)
        rwth_img2_label.setPixmap(
            QPixmap("/src\RWTH-Aachen-University.jpg"))
        rwth_img2_label.setFixedSize(900, 400)

        'form layout containing all elements'
        '''form_box = QFormLayout()
        form_box.addRow(None, descr_text_label)
        form_box.addRow(instruct_label, self.arch_address)
        form_box.addRow(None, self.connect_btn)
        form_box.addRow(None, self.info_abt_files)
        form_box.addRow(None, self.show_details_btn)'''
        group_box = QGroupBox('Archive Connection')
        inner_group_box = QVBoxLayout()
        inner_group_box.addWidget(instruct_label)
        inner_group_box.addWidget(self.arch_address)
        inner_group_box.addWidget(self.connect_btn, alignment=Qt.AlignCenter)
        inner_group_box.addLayout(hbox_info_details)
        group_box.setLayout(inner_group_box)
        # self.tab2_arch.setLayout(form_box)
        self.tab2_arch.layout.addWidget(descr_text_label)
        self.tab2_arch.layout.addWidget(group_box)
        self.tab2_arch.layout.addWidget(rwth_img2_label)
        self.tab2_arch.setLayout(self.tab2_arch.layout)

    def prepare_tab_UI(self):
        self.tab3_prepare.layout = QVBoxLayout()
        self.dict = dict()
        'intro label'
        intro_text_prepare = QLabel()
        intro_text_prepare.setText("The selected files can be prepared here and then pushed into the database. Fields marked with * are compulsory")
        intro_text_prepare.setFont(QFont("Calibri", 10))
        intro_text_prepare.setAlignment(Qt.AlignJustify)
        intro_text_prepare.setStyleSheet("color: black;")
        intro_text_prepare.setFixedHeight(20)
        'list widget to display selected files'
        self.list_widget_selected = QListWidget(self)
        self.list_widget_selected.addItems(self.to_prepare_list)
        self.list_widget_selected.setFixedHeight(70)
        self.list_widget_selected.setStyleSheet("border: None")
        'label showing the selected file URL on Archive where self.to_prepare_list contains the selected item'
        # self.selected_item_from_SeconndWin = QLabel(self)
        # self.selected_item_from_SeconndWin = self.to_prepare_list
        'count button'
        self.clear_prepare_btn = QPushButton()
        'grouping into one box'
        metadata_generation_box = QGroupBox('Metadata Generation')

        self.clear_prepare_btn.setText("Clear Selection")
        self.clear_prepare_btn.setFixedWidth(85)
        self.clear_prepare_btn.setStyleSheet("background-color: blue; color: white")
        'prepare button'
        self.prepare_btn = QPushButton()
        self.prepare_btn.setText("Prepare Files")
        self.prepare_btn.setFixedWidth(85)
        self.prepare_btn.setStyleSheet("background-color: blue; color: white")
        'reset button'
        self.reset_btn = QPushButton()
        self.reset_btn.setText('Reset Fields')
        self.reset_btn.setFixedWidth(85)
        self.reset_btn.setStyleSheet("background-color: blue; color: white")
        'hbox for containing 2 buttons'
        hbox_prepare = QHBoxLayout()
        hbox_prepare.addWidget(self.clear_prepare_btn)
        hbox_prepare.addWidget(self.reset_btn)
        hbox_prepare.addWidget(self.prepare_btn)

        'seperate views with different fields for manual input: for converting into supported type of JSON'
        self.generic_view_overall = QVBoxLayout(self)

        'default fields to input'
        self.hbox_default = QHBoxLayout()
        material_label = QLabel('Material:')
        self.material_field = QLineEdit()
        operator_label = QLabel('Operator:')
        self.operator_field = QLineEdit()
        date_label = QLabel('Date: (DD-MM-YYYY)*')
        self.date_field = QLineEdit()
        'push button for autofill initial fields'
        self.autofill_btn = QPushButton('Autofill')
        self.autofill_btn.setStyleSheet("background-color: blue; color: white")
        self.autofill_btn.setFixedWidth(85)
        self.hbox_default.addWidget(material_label)
        self.hbox_default.addWidget(self.material_field)
        self.hbox_default.addWidget(operator_label)
        self.hbox_default.addWidget(self.operator_field)
        self.hbox_default.addWidget(date_label)
        self.hbox_default.addWidget(self.date_field)
        self.hbox_default.addWidget(self.autofill_btn)

        'specific fields'
        self.hbox_spec = QHBoxLayout()
        vbox_inside_left = QVBoxLayout()
        'type of experiment result'
        exp_label = QLabel('Type of Experiment:')
        self.exp_type = QLineEdit()
        'sample no.'
        sample_lbl = QLabel('Sample No.:')
        self.sample_no = QLineEdit()
        #  LOM/SEM
        'etchant'
        etchant_lbl = QLabel('Etchant')
        self.etchant = QLineEdit()
        'etching_time'
        etching_time_lbl = QLabel('Etching Time')
        self.etc_time = QLineEdit()
        'magnification'
        magn_lbl = QLabel('Magnification')
        self.magnification = QLineEdit()

        #  microhardness
        'load microh'
        load_hardness_lbl = QLabel('Load for Microhardness: ')
        self.load_mharndess = QLineEdit()
        #  tensile_test
        'din_standard tt'
        din_standrd_lbl = QLabel("DIN Standard:")
        self.din_std = QLineEdit()
        'adding first 7 fields in left vbox'
        vbox_inside_left.addWidget(exp_label)
        vbox_inside_left.addWidget(self.exp_type)
        vbox_inside_left.addWidget(sample_lbl)
        vbox_inside_left.addWidget(self.sample_no)
        vbox_inside_left.addWidget(etchant_lbl)
        vbox_inside_left.addWidget(self.etchant)
        vbox_inside_left.addWidget(etching_time_lbl)
        vbox_inside_left.addWidget(self.etc_time)
        vbox_inside_left.addWidget(magn_lbl)
        vbox_inside_left.addWidget(self.magnification)
        vbox_inside_left.addWidget(load_hardness_lbl)
        vbox_inside_left.addWidget(self.load_mharndess)
        vbox_inside_left.addWidget(din_standrd_lbl)
        vbox_inside_left.addWidget(self.din_std)

        # second vbox_right
        vbox_inside_right = QVBoxLayout()
        #  particle size distribution
        'psd'
        psd_lbl = QLabel('Particle Size Distribution (d10, d50, d90):')
        self.psd = QLineEdit()
        'graph_type i.e. x_area, xFemax, xc_min'
        type_axes_psd_lbl = QLabel("Type (x_area, xFe_max, xc_min): ")
        self.type_psd = QLineEdit()
        #  atomization
        'mfg.'
        mafg_lbl = QLabel('Manufacturer (Powder):')
        self.mfg_powder = QLineEdit()
        'charge'
        charge_lbl = QLabel('Charge (Powder):')
        self.charge_powder = QLineEdit()
        'lot'
        lot_lbl = QLabel('Lot (Powder):')
        self.lot_powder = QLineEdit()
        'default psd'
        default_psd_lbl = QLabel('Default PSD (d10, d50, d90):')
        self.default_psd_powder = QLineEdit()
        'additional info'
        additional_lbl = QLabel('Additional Info:')
        self.additional_info = QLineEdit()
        self.additional_info.setFixedHeight(20)
        'filling up boxes'
        vbox_inside_right.addWidget(psd_lbl)
        vbox_inside_right.addWidget(self.psd)
        vbox_inside_right.addWidget(type_axes_psd_lbl)
        vbox_inside_right.addWidget(self.type_psd)
        vbox_inside_right.addWidget(mafg_lbl)
        vbox_inside_right.addWidget(self.mfg_powder)
        vbox_inside_right.addWidget(charge_lbl)
        vbox_inside_right.addWidget(self.charge_powder)
        vbox_inside_right.addWidget(lot_lbl)
        vbox_inside_right.addWidget(self.lot_powder)
        vbox_inside_right.addWidget(default_psd_lbl)
        vbox_inside_right.addWidget(self.default_psd_powder)
        vbox_inside_right.addWidget(additional_lbl)
        vbox_inside_right.addWidget(self.additional_info)

        self.hbox_spec.addLayout(vbox_inside_left)
        self.hbox_spec.addLayout(vbox_inside_right)
        self.generic_view_overall.addLayout(self.hbox_default)
        self.generic_view_overall.addLayout(self.hbox_spec)
        metadata_generation_box.setLayout(self.generic_view_overall)
        'adding widgets in the view'
        self.tab3_prepare.layout.addWidget(intro_text_prepare)
        self.tab3_prepare.layout.addWidget(self.list_widget_selected)
        # self.tab3_prepare.layout.addWidget(self.count_label, alignment=Qt.AlignLeft)
        # self.tab3_prepare.layout.addWidget(self.prepare_btn, alignment=Qt.AlignHCenter)
        self.tab3_prepare.layout.addWidget(metadata_generation_box)
        self.tab3_prepare.layout.addLayout(hbox_prepare)
        self.tab3_prepare.setLayout(self.tab3_prepare.layout)

    def push_into_db_tab_UI(self):
        self.tab4_push_db.layout = QVBoxLayout()
        'introduction label'
        intro_pushDB_lbl = QLabel('This enables the user to push the prepared files into the Database. The database dealt with here is a MongoDB Database, and the connection string of the DB has to be entered. For more details on MongoDB, please refer to: https://www.mongodb.com/what-is-mongodb')
        intro_pushDB_lbl.setFont(QFont("Calibri", 10))
        intro_pushDB_lbl.setWordWrap(True)
        intro_pushDB_lbl.setAlignment(Qt.AlignJustify)
        intro_pushDB_lbl.setStyleSheet("color: black;")
        intro_pushDB_lbl.setFixedHeight(50)

        'list of files prepared'
        self.push_list = QListWidget(self)
        self.push_list.addItems(self._already_prepared_list)
        # 1. add files in qlistwidget with just names and add in layout. 2. add signal for text changed and finished in connect field 3. implement qpush button
        'label and field for manual input of mangoDB srv/connection string'
        group_box_pushDB = QGroupBox('Connection with Database')
        inner_xonn_mongo_box = QVBoxLayout()
        mongo_conn_lbl = QLabel('Please Enter the Connection String of the Database here: *')
        mongo_conn_lbl.setFont(QFont('Calibri', 10))
        mongo_conn_lbl.setWordWrap(True)
        mongo_conn_lbl.setAlignment(Qt.AlignLeft)
        mongo_conn_lbl.setStyleSheet('color:black;')
        self.mongo_conn_field = QLineEdit(self)

        inner_xonn_mongo_box.addWidget(mongo_conn_lbl)
        inner_xonn_mongo_box.addWidget(self.mongo_conn_field)
        group_box_pushDB.setLayout(inner_xonn_mongo_box)
        group_box_pushDB.setFixedSize(910, 90)

        # mongodb image
        mongo_label = QLabel(self)
        pixmap_mongo = QPixmap('/src\mongodb_kleinesbild.PNG')
        mongo_label.setPixmap(pixmap_mongo)
        mongo_label.setPixmap(QPixmap('/src\mongodb_kleinesbild.PNG'))
        mongo_label.setFixedSize(350, 150)

        'another image'
        rwth_img2_label = QLabel(self)
        pixmap_rwth = QPixmap('/src\RWTH-Aachen-University.jpg')
        rwth_img2_label.setPixmap(pixmap_rwth)
        rwth_img2_label.setPixmap(
            QPixmap("/src\RWTH-Aachen-University.jpg"))
        rwth_img2_label.setFixedSize(900, 400)

        'push into db button'
        self.push_into_DB_btn = QPushButton()
        self.push_into_DB_btn.setText("Push into DB")
        self.push_into_DB_btn.setFixedWidth(85)
        self.push_into_DB_btn.setStyleSheet("background-color: blue; color: white")

        'adding widgets in the view'
        self.tab4_push_db.layout.addWidget(intro_pushDB_lbl)
        self.tab4_push_db.layout.addWidget(group_box_pushDB)
        self.tab4_push_db.layout.addWidget(self.push_into_DB_btn, alignment=Qt.AlignCenter)
        self.tab4_push_db.layout.addWidget(rwth_img2_label)
        self.tab4_push_db.layout.addWidget(mongo_label, alignment=Qt.AlignLeft)
        self.tab4_push_db.setLayout(self.tab4_push_db.layout)

    def activate_all_fields(self):
        self.etchant.setEnabled(True)
        self.etc_time.setEnabled(True)
        self.magnification.setEnabled(True)
        self.load_mharndess.setEnabled(True)
        self.din_std.setEnabled(True)
        self.psd.setEnabled(True)
        self.type_psd.setEnabled(True)
        self.mfg_powder.setEnabled(True)
        self.lot_powder.setEnabled(True)
        self.charge_powder.setEnabled(True)
        self.default_psd_powder.setEnabled(True)

    def refresh_prepare_list(self):
        self.list_widget_selected.clear()
        self.list_widget_selected.addItems(self.to_prepare_list)

    def onDragdropGenerateBtnClicked(self):
        'formatting of file name according to convention'
        if self.material.text() and self.type_test.text() and self.drgDrop_file.text() and self.operator.text() and self.address_archive.text() and self.date.text():
            self.drgDrop_file_text = self.drgDrop_file.text()
            new_file_name = self.drgDrop_file_text[self.drgDrop_file_text.rfind('/'):self.drgDrop_file_text.rfind('.')] + '+' + self.material.text() + '+' + \
                            self.type_test.text() + '+' + self.operator.text() + '+' + 'dated=' + self.date.text() + \
                            self.drgDrop_file_text[self.drgDrop_file_text.rfind('.'):]
            dest = shutil.copy(self.drgDrop_file_text, self.address_archive.text()+new_file_name)
            QMessageBox.information(self, "pyMongolator", "Notification: File Saved")
        else:
            QMessageBox.information(self, "pyMongolator", "Error: Please fill out the mandatory fields")

    def onConnectArchiveBtnClicked(self):
        self._archive_address_to_save = self.arch_address.text()
        'show details'
        self.info_abt_files.setEnabled(True)
        'call to function to show all files retrieved from dict'
        a1 = ArchiveGetter(self._archive_address_to_save)
        self.dict = a1.get_files()
        self._storage_str_for_retrieved_files = show_details_from_retrieved_dict(self.dict)
        self.info_abt_files.setText(self._storage_str_for_retrieved_files)
        self.show_details_btn.setVisible(True)
        self._flag_for_second_window = True

    def onArchAddressChanged(self):
        for key in self.dict:
            self.dict[key] = []
        self.dict = ArchiveGetter(self._archive_address_to_save).get_files()
        self._storage_str_for_retrieved_files = show_details_from_retrieved_dict(self.dict)
        self.info_abt_files.setText(self._storage_str_for_retrieved_files)
        self._flag_for_second_window = True

    def load_prepare_list(self):
        temp_list = list()
        if len(self.to_prepare_list) == 0:
            self.to_prepare_list = self.second_win.getter()
        else:
            temp_list = self.second_win.getter()
            for each in temp_list:
                if each not in self.to_prepare_list:
                    self.to_prepare_list.append(each)
        print('self.to_prepare_list:', self.to_prepare_list)
        self.list_widget_selected.addItems(self.to_prepare_list)


    def onShowDetailsBtnClicked(self):
        '''tasks to perform on clicking show details button'''
        self.list_for_second_window = []
        if self._flag_for_second_window:
            for key, val in self.dict.items():
                for each_val in val:
                    self.list_for_second_window.append(each_val)
            # self._flag_for_second_window = True
        self.second_win = SecondWindow(self.list_for_second_window)
        self.second_win.show()
        self._flag_for_prepare = True
        self._flag_for_display_prepare = True

    def onPrepareBtnClicked(self):
        if not self._flag_for_no_items_selected_in_liswidget:
            if self.material_field.text() and self.operator_field.text() and self.date_field.text() and self.exp_type.text():
                'code for sending data to data wrapper'
                self.tuple_for_wrapping = (self.material_field.text(), self.operator_field.text(), self.date_field.text(),
                                           self.exp_type.text(), self.sample_no.text(), self.etchant.text(), self.etc_time.text(),
                                           self.magnification.text(), self.load_mharndess.text(), self.din_std.text(), self.psd.text(),
                                           self.type_psd.text(), self.charge_powder.text(), self.lot_powder.text(), self.mfg_powder.text(),
                                           self.default_psd_powder.text(), self.additional_info.text(), self.selected_item_prepare_list)
                parsed_element = self.selected_item_prepare_list
                dw = DataWrapper(self.tuple_for_wrapping)
                dw.wrapper()
                if dw.parser():
                    self.converted_list.append(dw.getter())
                    self._already_prepared_list.append(self.selected_item_prepare_list)
                    self.activate_all_fields()
                    self.onResetFieldsBtnClicked()
                    QMessageBox.information(self, "pyMongolator", "Success: 1 File Successfully Parsed")
                    self.to_prepare_list.remove(self.selected_item_prepare_list)
                    self.refresh_prepare_list()
                    print('remaining items in list: ', self.to_prepare_list)
            else:
                QMessageBox.information(self, "pyMongolator", "Error: Please fill out the mandatory fields")
        else:
            QMessageBox.information(self, "pyMongolator", "Error: Please Select a file")

    def onClearSelectionListClicked(self):
        self.to_prepare_list.clear()
        # self.list_widget_selected.addItems(self.to_prepare_list)
        self.list_widget_selected.clear()
        self._flag_for_clear_selection = True
        self.operator_field.setText("")
        self.material_field.setText("")
        self.exp_type.setText("")
        self.onResetFieldsBtnClicked()

    def onResetFieldsBtnClicked(self):
        self.sample_no.setText("")
        self.etchant.setText("")
        self.etc_time.setText("")
        self.magnification.setText("")
        self.load_mharndess.setText("")
        self.din_std.setText("")
        self.type_psd.setText("")
        self.psd.setText("")
        self.default_psd_powder.setText("")
        self.lot_powder.setText("")
        self.charge_powder.setText("")
        self.mfg_powder.setText("")
        self.additional_info.setText("")
        'date field empty'

    def onAutoFillPrepareBtnClicked(self):
        if self._flag_for_display_prepare and not self._flag_for_no_items_selected_in_liswidget and self._flag_for_selection_in_listwidget:
            if self.selected_item_prepare_list.count('+') >= 3:
                filename_fragments = self.selected_item_prepare_list.split('+')
                tmp_for_Date = filename_fragments[-1]
                self.operator_field.setText(filename_fragments[-2])
                self.date_field.setText(tmp_for_Date[tmp_for_Date.rfind('=')+1:tmp_for_Date.rfind('.')])
                self.material_field.setText(filename_fragments[-4])
                self.exp_type.setText(filename_fragments[-3])
                'insert code for selective manual input allowance'
                if filename_fragments[-3] in ['LOM', 'SEM', 'EBSD']:
                    self.load_mharndess.setEnabled(False)
                    self.din_std.setEnabled(False)
                    self.type_psd.setEnabled(False)
                elif filename_fragments[-3] in ['Tensile Test', 'tensile', 'Tensile', 'Torsion','Torsion Test', 'Wear Test','Wear', 'Crash Test', 'Crash', 'Charpy', 'Charpy Impact Test', 'Micorhardness']:
                    self.type_psd.setEnabled(False)
                    self.psd.setEnabled(False)
                    self.magnification.setEnabled(False)
                    self.default_psd_powder.setEnabled(False)
                    self.charge_powder.setEnabled(False)
                    self.lot_powder.setEnabled(False)
                    self.mfg_powder.setEnabled(False)
                    self.etchant.setEnabled(False)
                    self.etc_time.setEnabled(False)
                elif filename_fragments[-3] in ['Camsizer', 'PSD']:
                    self.magnification.setEnabled(False)
                    self.load_mharndess.setEnabled(False)
                    self.etchant.setEnabled(False)
                    self.etc_time.setEnabled(False)
                    self.din_std.setEnabled(False)
            else:
                QMessageBox.information(self, "pyMongolator", "Error: Incorrect Naming convention used.")
        else:
            QMessageBox.information(self, "pyMongolator", "Error: No Selection done")

    def onResetSaveAsBtnClicked(self):
        self.operator.setText("")
        self.date.setText("")
        self.type_test.setText("")
        self.material.setText("")
        self.address_archive.setText("")
        self.drgDrop_file.setText("")

    def selectionInListOfPrepareChanged(self):
        self._flag_for_selection_in_listwidget = True
        if self._flag_for_clear_selection:
            if self.list_widget_selected.currentRow():
                if self.list_widget_selected.currentRow() != -1:
                    self.selected_item_prepare_list = self.to_prepare_list[self.list_widget_selected.currentRow()]
                    self.activate_all_fields()
            else:
                self._flag_for_no_items_selected_in_liswidget = False

    def selectionChangedListWisgetPrepare(self):
        self._flag_for_selection_in_listwidget = True
        if self.list_widget_selected.selectedItems():
            if self.list_widget_selected.currentRow() != -1:
                self.selected_item_prepare_list = self.to_prepare_list[self.list_widget_selected.currentRow()]
                self._flag_for_no_items_selected_in_liswidget = False
                self.activate_all_fields()

    def onPushDBbtnClicked(self):
        self._connection_str = self.mongo_conn_field.text()
        dataPusher = DataPusher(self.converted_list, self._connection_str)
        num_success = dataPusher.processer()[0]
        display_str = "Versuch Erfolgreich!\nSuccessful attempts: {0}".format(dataPusher.processer()[0])
        QMessageBox.information(self, "pyMongolator", display_str)


'''if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WelcomeWindow()
    win.show()
    sys.exit(app.exec_())'''
