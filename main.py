from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (QApplication, QMainWindow,QMessageBox, QWidget, QTableWidgetItem)
from PyQt5.QtGui import (QColor, QBrush)
from PyQt5.QtCore import (QSettings, Qt, QTimer)
from algolab import Backend
from algolab_socket import AlgoLabSocket
import pandas as pd, time, json, threading, sqlite3, sys
import sql

class LoginForm(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(264, 150)
        Form.setMinimumSize(QtCore.QSize(264, 150))
        Form.setMaximumSize(QtCore.QSize(264, 150))
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(13, 10, 241, 131))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_3.setMaxLength(30)
        self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_3.setCursorMoveStyle(QtCore.Qt.VisualMoveStyle)
        self.lineEdit_3.setClearButtonEnabled(True)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 2, 1, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_2.setMaxLength(50)
        self.lineEdit_2.setClearButtonEnabled(True)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox.setChecked(True)
        self.checkBox.setAutoRepeat(False)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 3, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit.setAutoFillBackground(False)
        self.lineEdit.setMaxLength(100)
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setShortcut("")
        self.pushButton_2.setCheckable(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 3, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.retranslateUi(Form)
        self.lineEdit_3.returnPressed.connect(self.pushButton_2.click) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.lineEdit, self.lineEdit_2)
        Form.setTabOrder(self.lineEdit_2, self.lineEdit_3)
        Form.setTabOrder(self.lineEdit_3, self.checkBox)
        Form.setTabOrder(self.checkBox, self.pushButton_2)
        self.loadApi()
        self.pushButton_2.clicked.connect(self.login_call)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Giriş Ekranı"))
        self.label.setText(_translate("Form", "API-Key:"))
        self.checkBox.setText(_translate("Form", "API-Key'imi Hatırla"))
        self.pushButton_2.setText(_translate("Form", "Giriş Yap"))
        self.label_2.setText(_translate("Form", "TC No:"))
        self.label_3.setText(_translate("Form", "Şifre:"))

    def login_call(self):
        
        def showErrorDialog(message):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Bir Hata Oluştu")
            msg.setInformativeText(message)
            msg.setWindowTitle("Hata")
            msg.exec_()
            
        global api_key, tc_no, sifre, algo
        api_key = self.lineEdit.text()
        self.saveApiKey()           
        tc_no = self.lineEdit_2.text()
        sifre = self.lineEdit_3.text()
        algo = Backend(api_key, tc_no, sifre, auto_login=True)
        global token
        token = algo.LoginUser()
        if not token.startswith("Başarısız:"):
            login_screen.hide()  # Ekranı sakla
            sms_screen.show()    # SMS ekranını göster         
            self.lineEdit.setText("")
            self.lineEdit_2.setText("")
            self.lineEdit_3.setText("")
        else:
            parts = token.split("Başarısız:")
            if len(parts) > 1:
                message = parts[1].strip()
                showErrorDialog(message)
            else:
                showErrorDialog("")    
 
    def saveApiKey(self):
        if self.checkBox.isChecked():
            settings = QSettings("Algolab", "API_UI")
            settings.setValue("api_key", self.lineEdit.text())
        else:
            settings = QSettings("Algolab", "API_UI")
            settings.setValue("api_key", "")

    def loadApiKey(self):
        settings = QSettings("Algolab", "API_UI")
        saved_api_key = settings.value("api_key", type=str)
        if saved_api_key:
            return saved_api_key
        return ""
    
    def loadApi(self):
        settings = QSettings("Algolab", "API_UI")
        saved_api_key = settings.value("api_key", type=str)
        if saved_api_key:
            self.lineEdit.setText(saved_api_key)
            
class LoginScreen(QWidget):
    def __init__(self):
        super(LoginScreen, self).__init__()
        self.ui = LoginForm()
        self.ui.setupUi(self)
        
class SMS_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(263, 96)
        Form.setMinimumSize(QtCore.QSize(263, 96))
        Form.setMaximumSize(QtCore.QSize(263, 96))
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(10, 11, 209, 78))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_3.setClearButtonEnabled(True)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 0, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.sms_call)
        self.gridLayout.addWidget(self.pushButton_2, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.lineEdit_3, self.pushButton_2)
        self.lineEdit_3.returnPressed.connect(self.pushButton_2.click)
        
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Sms Doğrulama Ekranı"))
        self.label_3.setText(_translate("Form", "SMS Kodu:"))
        self.pushButton_2.setText(_translate("Form", "Doğrula"))
        self.label_5.setText(_translate("Form", "Response:"))

    def sms_call(self):
   
        def showErrorDialog(message):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Bir Hata Oluştu")
            msg.setInformativeText(message)
            msg.setWindowTitle("Hata")
            msg.exec_()
            
        def login_update(date, token, hash):
            try:
                sql.control()
                with sqlite3.connect('config.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('DELETE FROM login')
                    cursor.execute('''
                        INSERT INTO login (date, token, hash)
                        VALUES (?, ?, ?)
                    ''', (date, token, hash))
                    conn.commit()
            except Exception as e:
                print(f"login_update error: {e}")
                
        sms = self.lineEdit_3.text()
        data = algo.LoginUserControl(sms, token)
        if isinstance(data, dict):
            login_update(data['date'], data['token'], data['hash'])
            sms_screen.hide()
            global main_screen
            main_screen = MainScreen()
            main_screen.show()
            self.lineEdit_3.setText("")
        else:
            parts = data.split("Başarısız:")
            if len(parts) > 1:
                message = parts[1].strip()
                showErrorDialog(message)
            else:
                showErrorDialog("")                

class SMSScreen(QWidget):
    def __init__(self):
        super(SMSScreen, self).__init__()
        self.ui = SMS_Form()
        self.ui.setupUi(self)

class Main_Form(object):
    open_forms = []
    fetch_thread = None
    soket = None
    terminate_flag = False
    form_count = 0

    def __init__(self):
        self.lock = threading.Lock()
        self.stocks_data = {}
        self.data_count = 0
        if algo.api_key and algo.hash:
            self.initialize_socket()
            self.db_transaction()

    @classmethod
    def increase_form_count(cls):
        cls.form_count += 1

    @classmethod
    def decrease_form_count(cls):
        if cls.form_count > 0:
            cls.form_count -= 1

    def initialize_socket(self):
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                
                time.sleep(0.5)
                self.soket = AlgoLabSocket(algo.api_key, algo.hash, "H")
                if self.soket.connect():
                    # Bağlantı başarılı, veri gönder ve fetch_thread'i başlat
                    data = {"Type": "T", "Symbols": ["ALL"]}
                    self.soket.send(data)
                    self.fetch_thread = threading.Thread(target=self.fetch_data)
                    self.fetch_thread.start()
                    break  # Döngüden çık
                else:
                    self.message(f"Bağlantı başarısız, {attempt+1} deneme.")
            except Exception as e:
                self.message(f"Bağlantı sırasında bir hata oluştu: {e}")
        
        if not self.soket or not self.soket.connected:
            self.message("Soket bağlantısı kurulamadı...")
                
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(901, 838)
        MainWindow.setMinimumSize(QtCore.QSize(901, 838))
        MainWindow.setMaximumSize(QtCore.QSize(901, 838))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMaximumSize(QtCore.QSize(901, 787))
        self.centralwidget.setObjectName("centralwidget")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 590, 91, 16))
        self.label_4.setObjectName("label_4")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_2.setGeometry(QtCore.QRect(700, 50, 181, 531))
        self.tableWidget_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableWidget_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tableWidget_2.setLineWidth(1)
        self.tableWidget_2.setDragDropOverwriteMode(False)
        self.tableWidget_2.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.tableWidget_2.setAlternatingRowColors(True)
        self.tableWidget_2.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableWidget_2.setShowGrid(True)
        self.tableWidget_2.setWordWrap(False)
        self.tableWidget_2.setCornerButtonEnabled(False)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.horizontalHeader().setVisible(False)
        self.tableWidget_2.horizontalHeader().setDefaultSectionSize(74)
        self.tableWidget_2.horizontalHeader().setHighlightSections(False)
        self.tableWidget_2.horizontalHeader().setMinimumSectionSize(74)
        self.tableWidget_2.verticalHeader().setVisible(False)
        self.tableWidget_2.verticalHeader().setDefaultSectionSize(18)
        self.tableWidget_2.verticalHeader().setHighlightSections(False)
        self.tableWidget_2.verticalHeader().setMinimumSectionSize(18)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setEnabled(True)
        self.tableWidget.setGeometry(QtCore.QRect(20, 51, 671, 531))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.tableWidget.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.tableWidget.setInputMethodHints(QtCore.Qt.ImhNone)
        self.tableWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableWidget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tableWidget.setLineWidth(1)
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setAutoScroll(True)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setProperty("showDropIndicator", True)
        self.tableWidget.setDragDropOverwriteMode(False)
        self.tableWidget.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setWordWrap(False)
        self.tableWidget.setCornerButtonEnabled(False)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(70)
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(40)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(20)
        self.tableWidget.verticalHeader().setHighlightSections(False)
        self.tableWidget.verticalHeader().setMinimumSectionSize(10)
        self.tableWidget_3 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_3.setGeometry(QtCore.QRect(20, 612, 861, 161))
        self.tableWidget_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableWidget_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tableWidget_3.setLineWidth(1)
        self.tableWidget_3.setDragDropOverwriteMode(False)
        self.tableWidget_3.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.tableWidget_3.setAlternatingRowColors(True)
        self.tableWidget_3.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableWidget_3.setShowGrid(True)
        self.tableWidget_3.setWordWrap(False)
        self.tableWidget_3.setCornerButtonEnabled(False)
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(0)
        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3.horizontalHeader().setVisible(True)
        self.tableWidget_3.horizontalHeader().setDefaultSectionSize(80)
        self.tableWidget_3.horizontalHeader().setHighlightSections(False)
        self.tableWidget_3.horizontalHeader().setMinimumSectionSize(80)
        self.tableWidget_3.verticalHeader().setVisible(False)
        self.tableWidget_3.verticalHeader().setDefaultSectionSize(20)
        self.tableWidget_3.verticalHeader().setHighlightSections(False)
        self.tableWidget_3.verticalHeader().setMinimumSectionSize(20)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(790, 10, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(700, 30, 40, 16))
        self.label_5.setObjectName("label_5")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 30, 51, 20))
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 901, 26))
        self.menuBar.setTabletTracking(False)
        self.menuBar.setFocusPolicy(QtCore.Qt.NoFocus)
        self.menuBar.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.menuBar.setObjectName("menuBar")
        self.menuMen = QtWidgets.QMenu(self.menuBar)
        self.menuMen.setObjectName("menuMen")
        self.menuRaporlama = QtWidgets.QMenu(self.menuMen)
        self.menuRaporlama.setObjectName("menuRaporlama")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionTahta_A = QtWidgets.QAction(MainWindow)
        self.actionTahta_A.setObjectName("actionTahta_A")
        self.actionPortf_y_Excele_Aktar = QtWidgets.QAction(MainWindow)
        self.actionPortf_y_Excele_Aktar.setCheckable(False)
        self.actionPortf_y_Excele_Aktar.setObjectName("actionPortf_y_Excele_Aktar")
        self.actionEmirleri_Excele_Aktar = QtWidgets.QAction(MainWindow)
        self.actionEmirleri_Excele_Aktar.setObjectName("actionEmirleri_Excele_Aktar")
        self.actionOverall_Excele_Aktar = QtWidgets.QAction(MainWindow)
        self.actionOverall_Excele_Aktar.setObjectName("actionOverall_Excele_Aktar")
        self.actionHesap_Ekstresi_ek = QtWidgets.QAction(MainWindow)
        self.actionHesap_Ekstresi_ek.setObjectName("actionHesap_Ekstresi_ek")
        self.menuRaporlama.addAction(self.actionPortf_y_Excele_Aktar)
        self.menuRaporlama.addAction(self.actionEmirleri_Excele_Aktar)
        self.menuRaporlama.addAction(self.actionOverall_Excele_Aktar)
        self.menuRaporlama.addAction(self.actionHesap_Ekstresi_ek)
        self.menuMen.addAction(self.actionTahta_A)
        self.menuMen.addSeparator()
        self.menuMen.addAction(self.menuRaporlama.menuAction())
        self.menuBar.addAction(self.menuMen.menuAction())
        self.pushButton_3.clicked.connect(self.refresh)
        self.tableWidget.cellDoubleClicked.connect(self.row_was_clicked)
        self.actionTahta_A.triggered.connect(self.showTahta)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)      
          
    def message(self, message):
        """
        Durum çubuğunda mesaj gösterir. Mesaj başka bir mesaj gösterilene kadar kalıcıdır.

        Args:
            message (str): Gösterilecek mesaj.
        """
        print(message)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Ana Sayfa", "Ana Sayfa"))
        self.label_4.setText(_translate("MainWindow", "Emirler"))
        self.tableWidget.setSortingEnabled(True)
        self.pushButton_3.setText(_translate("MainWindow", "Yenile"))
        self.label_5.setText(_translate("MainWindow", "Overall"))
        self.label_3.setText(_translate("MainWindow", "Portföy"))
        self.menuMen.setTitle(_translate("MainWindow", "Menü"))
        self.menuRaporlama.setTitle(_translate("MainWindow", "Raporlama"))
        self.actionTahta_A.setText(_translate("MainWindow", "Tahta Aç"))
        self.actionPortf_y_Excele_Aktar.setText(_translate("MainWindow", "Portföyü Excele Aktar"))
        self.actionEmirleri_Excele_Aktar.setText(_translate("MainWindow", "Emirleri Excele Aktar "))
        self.actionOverall_Excele_Aktar.setText(_translate("MainWindow", "Overallı Excele Aktar"))
        self.actionHesap_Ekstresi_ek.setText(_translate("MainWindow", "Hesap Ekstresi Çek"))

    def row_was_clicked(self, row, column):
        symbol = self.tableWidget.item(row, 0).text()
        self.showTahta(symbol=symbol)
   
    def showTahta(self, symbol=""):
        if self.form_count < 5:
            new_form = TahtaScreen(main_screen=self)  # TahtaScreen sınıfının bir örneğini oluşturun
            form = new_form.ui  # Tahta_Form sınıfının bir örneğini elde edin
            self.open_forms.append(new_form)  # Yeni formu açık formlar listesine ekleyin
            new_form.show()  # Yeni formu gösterin
            if symbol:
                form.lineEdit.setText(symbol)
                form.OrderTable()
        else:
            self.message("Maksimum form sayısına ulaşıldı.")

    def refresh(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.pushButton_3.setEnabled(False)

        if self.get_portfolio() and self.get_transaction() and self.get_creditrisk():
            QApplication.restoreOverrideCursor()
            self.pushButton_3.setEnabled(True)
        else:
            QApplication.restoreOverrideCursor()
            self.pushButton_3.setEnabled(True)
            self.message("Oturum zaman aşımına uğradı.")
            self.reset()

    def reset(self):
        def showErrorDialog(message):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Bir Hata Oluştu")
            msg.setInformativeText(message)
            msg.setWindowTitle("Hata")
            msg.exec_()
        showErrorDialog("Oturumunuz sonlanmıştır. Lütfen internet bağlantınızı kontrol ettikten sonra programı tekrar çalıştırın.")
        for window in QApplication.topLevelWidgets():
            if window.isVisible():
                window.close()
            
    def get_portfolio(self): 
        try:
            f = algo.GetInstantPosition()
            if f["success"] == True:
                portfolio_data = f["content"]
            
            if not portfolio_data:
                return 
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)

            column_name_mapping = {
                "code": "Sembol",
                "explanation": "Acıklama",
                "totalstock": "Lot",
                "cost": "Maliyet",
                "tlamaount": "Miktar(TL)",
                "unitprice": "Fiyat",
                "profit": "Kar/Zarar"
            }

            headers = list(column_name_mapping.values())
            self.tableWidget.setColumnCount(len(headers))
            self.tableWidget.setHorizontalHeaderLabels(headers)

            # Adjust column widths
            table_width = self.tableWidget.width() - 20  # Subtracting 20 to account for the scrollbar width
            column_width = int(table_width / len(headers))  # Convert to int to avoid TypeError
            for i in range(len(headers)):
                self.tableWidget.setColumnWidth(i, column_width)

            def format_value(column_name, value):
                """Format the value based on column name."""
                columns_with_two_decimal = ["Lot", "Maliyet", "Miktar(TL)","Fiyat", "Kar/Zarar"]
                if column_name in columns_with_two_decimal:
                    try:
                        return "{:.2f}".format(float(value))
                    except ValueError:
                        return value
                return str(value)

            for position in portfolio_data:
                if position.get("code") == '-':  # Eğer code değeri '-' ise, bu satırı atla
                    continue
                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)

                for col, original_key in enumerate(column_name_mapping.keys()):
                    value = position.get(original_key, "")
                    display_key = column_name_mapping[original_key]
                    formatted_value = format_value(display_key, value)
                    self.tableWidget.setItem(row_position, col, QTableWidgetItem(formatted_value))
            return True
        except Exception as e:
            error_message = str(e)
            self.message(f"get_portfolio error: {error_message}")
            return False
            
    def get_creditrisk(self):
        try:
            # İlk DataFrame'i al
            limit = algo.GetSubAccounts()
            if limit and limit.get("success"):
                df_limit = pd.DataFrame(limit["content"])
            time.sleep(0.5)
            # İkinci DataFrame'i al
            f = algo.RiskSimulation()
            if f.get("success", False):
                portfolio_data = f.get("content", [])
                print(portfolio_data)
                if portfolio_data:
                    df_portfolio = pd.DataFrame([portfolio_data], index=[0])
                    # Belirtilen başlıkları ve tradeLimit sütununu seç
                    selected_columns = ['t1', 't2', 't0overall', 't1overall', 't2overall', 't0capitalrate', 't1capitalrate', 't2capitalrate', 'netoverall', 'credit0']
                    if 'tradeLimit' in df_limit.columns:
                        trade_limit_value = df_limit['tradeLimit'].iloc[0] 
                        df_portfolio['tradeLimit'] = trade_limit_value
                        selected_columns.append('tradeLimit')

                    # Sadece belirtilen sütunları içeren bir DataFrame oluştur
                    df_selected = df_portfolio[selected_columns]

                    # Sütun isimlerini değiştir
                    new_column_names = ['T1 Nakit Akışı', 'T2 Nakit Akışı', 'T0 Overall', 'T1 Overall', 'T2 Overall', 'T0 Marj Oranı', 'T1 Marj Oranı', 'T2 Marj Oranı', 
                                        'Net Overall', 'Kredili Alım', 'İşlem Limiti']
                    df_selected.columns = new_column_names

                    # DataFrame'i düzleştir
                    flat_data = pd.Series(df_selected.iloc[0])

                    # Tablo widget'ını ayarla
                    self.tableWidget_2.setRowCount(len(flat_data))
                    self.tableWidget_2.setColumnCount(2)  # İki sütun: biri başlık için, diğeri değer için

                    # Tablo başlıklarını ayarla
                    headers = ["Header", "Value"]
                    self.tableWidget_2.setHorizontalHeaderLabels(headers)

                    # Tabloya başlıklar ve değerler ekle
                    for i, (header, value) in enumerate(flat_data.items()):
                        self.tableWidget_2.setItem(i, 0, QTableWidgetItem(header))
                        self.tableWidget_2.setItem(i, 1, QTableWidgetItem(str(value)))
                    self.tableWidget_2.resizeColumnsToContents()
            return True
        except Exception as e:
            error_message = str(e)
            self.message(f"get_creditrisk error: {error_message}")
            return False
            
    def get_transaction(self): 
        try:
            f = algo.GetTodaysTransaction()
            if f["success"] == True:
                portfolio_data = f["content"]
            if not portfolio_data:  # If the portfolio is empty, stop here
                return True
            
            # Clear the QTableWidget
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.setColumnCount(0)
                   
            column_name_mapping = {
                "transactionId": "Referans",
                "timetransaction": "Emir Zamanı",
                "ticker": "Sembol",
                "buysell": "Yön",
                "ordersize": "Lot",
                "remainingsize": "Bekleyen Lot",
                "fillunit": "Gerçekleşen Lot",
                "price": "Fiyat",
                "amount": "Miktar",
                "description": "Statü"
            }

            # Specify the desired columns based on the mapped names
            headers = list(column_name_mapping.values())

            # Set the number of columns and the headers
            self.tableWidget_3.setColumnCount(len(headers))
            self.tableWidget_3.setHorizontalHeaderLabels(headers)

            def format_value(column_name, value):
                """Format the value based on column name."""
                columns_with_two_decimal = ["Miktar","Fiyat"]
                columns_with_zero_decimal = ["Lot", "Bekleyen Lot", "Gerçekleşen Lot"]

                if column_name in columns_with_two_decimal:
                    try:
                        return "{:.2f}".format(float(value))
                    except ValueError:
                        return value
                elif column_name in columns_with_zero_decimal:
                    try:
                        return "{:.0f}".format(float(value))
                    except ValueError:
                        return value
                return str(value)

            for position in portfolio_data:
                row_position = self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(row_position)

                for col, original_key in enumerate(column_name_mapping.keys()):
                    value = position.get(original_key, "")
                    display_key = column_name_mapping[original_key]
                    formatted_value = format_value(display_key, value)
                    self.tableWidget_3.setItem(row_position, col, QTableWidgetItem(formatted_value))
            self.tableWidget_3.resizeColumnsToContents()
            return True
        except Exception as e:
            self.message(f"get_transaction error: {e}")
            return False

    def db_transaction(self): 
        try:
            f = algo.GetTodaysTransaction()
            if f["success"] == True:
                portfolio_data = [
                    {
                        "ref_number": order["transactionId"],
                        "symbol": order["ticker"],
                        "lot": float(order["remainingsize"]),
                        "price": float(order["waitingprice"]),
                        "direction": "BUY" if order["buysell"] == "Alış" else "SELL",
                        "equityStatusDescription": order["equityStatusDescription"]
                    }
                    for order in f["content"]
                ]
            else:
                self.message("No portfolio data found")
                return

            if len(portfolio_data) == 0:
                self.message("No orders found.")
                return
            sql.control()
            with sqlite3.connect('config.db') as conn:
                cursor = conn.cursor()
                #Önceki değerleri sil
                cursor.execute('DELETE FROM transactions;')
                conn.commit()
                # Her bir sembol için veritabanını güncelle
                for order in portfolio_data:
                    if order['lot'] > 0:
                        cursor.execute('''
                            INSERT OR REPLACE INTO transactions (ref_number, symbol, lot, price, direction)
                            VALUES (?, ?, ?, ?, ?)
                        ''', ( order['ref_number'], order['symbol'], order['lot'], order['price'], order['direction']))
                        conn.commit()
                    else:
                        continue
            conn.close()
        except Exception as e:
            self.message(f"db_transaction error: {e}")

    def fetch_data(self):
        try:
            while self.soket.connected and not self.terminate_flag:
                data = self.soket.recv()
                if data:
                    msg = json.loads(data)
                    msg_type = msg.get("Type")
                    content = msg.get("Content", {})
                    market = content.get('Market')
                    symbol = content.get('Symbol')
                    if msg_type =="O":
                        print(content)
                        status = content.get('Status')
                        r = content.get('Comment')
                        if "Referans Numaranız:" in r:
                            # Assuming 'r' is a string, you can use the split method on it
                            ref_number = r.split("Referans Numaranız:")[1].split(";")[0].strip()
                        else:
                            ref_number = r
                        symbol = content.get('Symbol')
                        lot = int(content.get('Lot'))
                        direction = content.get('Direction')
                        direction = 'BUY' if content.get('Direction') == 0 else 'SELL'
                        price = content.get('Price')
                        if status == 2: # Gerçekleşti
                            try:
                                sql.control()
                                with sqlite3.connect('config.db') as conn:
                                    cursor = conn.cursor()
                                    # SQL sorgusu ile siparişi sil
                                    cursor.execute('DELETE FROM transactions WHERE ref_number = ?', (ref_number,))
                                    # Değişiklikleri kaydet
                                    conn.commit()
                            except sqlite3.Error as e:
                                # Veritabanı işlemi sırasında bir hata olursa yazdır
                                print(f"Veritabanından {ref_number} referans numaralı gerçekleşen emri silerken bir hata meydana geldi: {e}")
                            print(f"{symbol} sembolü için {ref_number} numaralı; {lot} lot {price} fiyatlı {direction} emir gerçekleşti.")
                        if status == 3: # Kısmi Gerçekleşti
                            try:
                                sql.control()
                                with sqlite3.connect('config.db') as conn:
                                    cursor = conn.cursor()

                                    # Mevcut lot miktarını çek
                                    cursor.execute('SELECT lot FROM transactions WHERE ref_number = ?', (ref_number,))
                                    mevcut_lot = cursor.fetchone()
                                    if mevcut_lot is not None:
                                        mevcut_lot = mevcut_lot[0]

                                        # Kısmen gerçekleşen lot miktarını hesapla
                                        kalan_lot = mevcut_lot - lot

                                        # SQL sorgusu ile lot miktarını güncelle
                                        if kalan_lot != 0:
                                            cursor.execute('UPDATE transactions SET lot = ? WHERE ref_number = ?', (kalan_lot, ref_number))
                                        else:
                                            cursor.execute('DELETE FROM transactions WHERE ref_number = ?', (ref_number,))
                                        # Değişiklikleri kaydet
                                        conn.commit()
                            except sqlite3.Error as e:
                                # Veritabanı işlemi sırasında bir hata olursa yazdır
                                print(f"Veritabanında {ref_number} referans numaralı kısmi gerçekleşen emrin lot miktarını güncellerken bir hata meydana geldi: {e}")
                            print(f"{symbol} sembolü için {ref_number} numaralı; {lot} lot {price} fiyatlı {direction} emir kısmen gerçekleşti.")

                        else:
                            ORDER_STATUS = {0: "Bekleyen",
                            1: "Teslim Edildi",
                            2: "Gerçekleşti",
                            3: "Kısmi Gerçekleşti",
                            4: "İptal Edildi",
                            5: "Değiştirildi",
                            6: "Askıya Alındı",
                            7: "Süresi Doldu",
                            8: "Hata"}
                            text = ORDER_STATUS.get(status, "Bilinmeyen Durum")
                            print(f"{symbol} sembolü için {ref_number} numaralı; {lot} lot {price} fiyatlı {direction} emirinin durumu değişti: {text}")

                    elif msg_type == "T" and market == "IMKBH" and len(symbol) <= 5:
                        with self.lock:
                            # Veri sözlüğüne sembolü ve içeriği ekle
                            self.stocks_data[symbol] = {
                                'Price': content.get('Price'),
                                'Change': content.get('Change'),
                                'High': content.get('High'),
                                'ChangePercentage': content.get('ChangePercentage'),
                                'Low': content.get('Low')
                            }
                            # Veri sayısını artır
                            self.data_count += 1
                            
                            # Her 100 veride bir veritabanını güncelle
                            if self.data_count >= 100:
                                self.update_database(self.stocks_data)
                                self.stocks_data.clear()  # Sözlüğü temizle
                                self.data_count = 0  # Sayacı sıfırla
                            
        except Exception as e:
            self.message(f"fetch_data error: {e}")
            self.soket.close()
            self.message("Socket kapatıldı.")

    def update_database(self, stocks_data):
        try:
            sql.control()
            with sqlite3.connect('config.db') as conn:
                cursor = conn.cursor()
                # Her bir sembol için veritabanını güncelle
                for symbol, content in stocks_data.items():
                    cursor.execute('''
                        INSERT OR REPLACE INTO stocks (symbol, price, change, high, change_percentage, low)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (symbol, content['Price'], content['Change'], content['High'], content['ChangePercentage'], content['Low']))
                # Değişiklikleri kaydet
                conn.commit()
            conn.close()
        except Exception as e:
            self.message(f"update_database error: {e}")  

class MainScreen(QMainWindow):  
    def __init__(self):
        super(MainScreen, self).__init__()
        self.ui = Main_Form()
        self.ui.setupUi(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.session_refresh)
        self.timer.start(900000) 
        
    def closeEvent(self, event):
        for window in QApplication.topLevelWidgets():
            if window.isVisible():
                window.close()
        Main_Form.terminate_flag = True
        event.accept()
        QApplication.quit()
        
    def session_refresh(self):
        try:
            resp = algo.SessionRefresh()
            if resp == False:
                print(f"Oturum süresi yenileme hatası: {resp}")
        except Exception as e:
            self.message(f"Error on session_refresh: {e}")  
    
class Tahta_Form(QtWidgets.QWidget):
    
    def __init__(self, parent=None):
        super(Tahta_Form, self).__init__(parent)
        self.setupUi(self)
        self.last_price = None  
        self.stocks_data = {}
        self.updating_order_table = False
        self.deleting_order = False
        self.eq = False

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(240, 643)
        Form.setMinimumSize(QtCore.QSize(240, 643))
        Form.setMaximumSize(QtCore.QSize(240, 643))
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 221, 621))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_22 = QtWidgets.QLabel(self.layoutWidget)
        self.label_22.setObjectName("label_22")
        self.gridLayout.addWidget(self.label_22, 3, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 2, 2, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.layoutWidget)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 10, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 2, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 2, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.layoutWidget)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 10, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineEdit.setText("")
        self.lineEdit.setMaxLength(5)
        self.lineEdit.setFrame(True)
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 2)
        self.label_12 = QtWidgets.QLabel(self.layoutWidget)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 10, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 1, 0, 1, 1)
        self.label_25 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_25.setFont(font)
        self.label_25.setObjectName("label_25")
        self.gridLayout.addWidget(self.label_25, 6, 0, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.layoutWidget)
        self.label_21.setObjectName("label_21")
        self.gridLayout.addWidget(self.label_21, 3, 1, 1, 1)
        self.label_24 = QtWidgets.QLabel(self.layoutWidget)
        self.label_24.setObjectName("label_24")
        self.gridLayout.addWidget(self.label_24, 3, 2, 1, 1)
        self.label_23 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_23.setFont(font)
        self.label_23.setObjectName("label_23")
        self.gridLayout.addWidget(self.label_23, 6, 1, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_26.setFont(font)
        self.label_26.setObjectName("label_26")
        self.gridLayout.addWidget(self.label_26, 6, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.tableWidget_4 = QtWidgets.QTableWidget(self.layoutWidget)
        self.tableWidget_4.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_4.sizePolicy().hasHeightForWidth())
        self.tableWidget_4.setSizePolicy(sizePolicy)
        self.tableWidget_4.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.tableWidget_4.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.tableWidget_4.setInputMethodHints(QtCore.Qt.ImhNone)
        self.tableWidget_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableWidget_4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tableWidget_4.setLineWidth(1)
        self.tableWidget_4.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget_4.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_4.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget_4.setAutoScroll(True)
        self.tableWidget_4.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.tableWidget_4.setProperty("showDropIndicator", True)
        self.tableWidget_4.setDragDropOverwriteMode(False)
        self.tableWidget_4.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.tableWidget_4.setAlternatingRowColors(True)
        self.tableWidget_4.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget_4.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_4.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidget_4.setShowGrid(True)
        self.tableWidget_4.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget_4.setWordWrap(False)
        self.tableWidget_4.setCornerButtonEnabled(False)
        self.tableWidget_4.setRowCount(0)
        self.tableWidget_4.setObjectName("tableWidget_4")
        self.tableWidget_4.setColumnCount(0)
        self.tableWidget_4.horizontalHeader().setVisible(True)
        self.tableWidget_4.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_4.horizontalHeader().setDefaultSectionSize(48)
        self.tableWidget_4.horizontalHeader().setHighlightSections(False)
        self.tableWidget_4.horizontalHeader().setMinimumSectionSize(20)
        self.tableWidget_4.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget_4.verticalHeader().setVisible(False)
        self.tableWidget_4.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget_4.verticalHeader().setDefaultSectionSize(17)
        self.tableWidget_4.verticalHeader().setHighlightSections(False)
        self.tableWidget_4.verticalHeader().setMinimumSectionSize(10)
        self.verticalLayout.addWidget(self.tableWidget_4)
        self.tableWidget_4.installEventFilter(self)
        self.lineEdit.returnPressed.connect(self.OrderTable)
        self.tableWidget_4.setHorizontalHeaderLabels(["Fiyat", "Alış", "Satış"])
        self.tableWidget_4.itemChanged.connect(self.on_item_changed)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_22.setText(_translate("Form", ""))
        self.label_9.setText(_translate("Form", "Değişim:"))
        self.label_14.setText(_translate("Form", ""))
        self.label_8.setText(_translate("Form", "Tavan:"))
        self.label_7.setText(_translate("Form", "Taban:"))
        self.label_11.setText(_translate("Form", ""))
        self.label_12.setText(_translate("Form", ""))
        self.label_10.setText(_translate("Form", ""))
        self.label_25.setText(_translate("Form", "Yüksek:"))
        self.label_21.setText(_translate("Form", ""))
        self.label_24.setText(_translate("Form", ""))
        self.label_23.setText(_translate("Form", "Düşük"))
        self.label_26.setText(_translate("Form", "Değişim %:"))
        self.tableWidget_4.setSortingEnabled(False)
                
    def OrderTable(self):
        try:
            def get_price_increment(price):
                if 0.01 <= price < 20.00:
                    return  0.01
                elif 20.00 <= price < 50.00:
                    return  0.02
                elif 50.00 <= price < 100.00:
                    return  0.05
                elif 100 <= price < 250:
                    return  0.10
                elif 250 <= price < 500:
                    return  0.25
                elif 500 <= price < 1000:
                    return  0.50
                elif 1000 <= price < 2500:
                    return  1.00
                elif price >= 2500:
                    return  2.50
            def get_price_range(price, taban, tavan):
                increment = get_price_increment(price)
                price_range = []

                # Taban fiyatından başlayarak tavan fiyatına kadar kademeleri oluşturma:
                new_price = taban
                while new_price <= tavan:
                    price_range.append(round(new_price, 2))
                    increment = get_price_increment(new_price)
                    new_price = round(new_price + increment, 2)
                return price_range

            Symbol = self.lineEdit.text()
            self.lineEdit.setText("")
            eqinfo = algo.GetEquityInfo(Symbol)
            if eqinfo != False and eqinfo["content"]["lst"] != "-":
                taban = float(eqinfo["content"]["flr"])
                tavan = float(eqinfo["content"]["clg"])
                price = float(eqinfo["content"]["lst"])
                self.label_10.setText(f"{Symbol}")
                self.label_22.setText(f"{tavan}")
                self.label_21.setText(f"{taban}")
                price_range = get_price_range(price, taban, tavan)
                price_range.reverse()  # Listeyi ters çevir
                # QTableWidget'a ekleme işlemi:
                self.tableWidget_4.setRowCount(len(price_range))
                self.tableWidget_4.setColumnCount(3)  # Fiyat, Alım, Satım için 3 kolon
                self.tableWidget_4.setHorizontalHeaderLabels(["Fiyat", "Alış", "Satış"])
                # Adjust column widths
                table_width = self.tableWidget_4.width() - 20  # Subtracting 20 to account for the scrollbar width
                column_width = int(table_width / 3) # Convert to int to avoid TypeError
                for i in range(3):
                    self.tableWidget_4.setColumnWidth(i, column_width)
                    
                for row, current_price in enumerate(price_range):
                    # Fiyat kolonu için hücre:
                    item_price = QTableWidgetItem(str(current_price))

                    # Fiyat hücresini değiştirilemez yap:
                    item_price.setFlags(item_price.flags() & ~Qt.ItemIsEditable)
                    self.tableWidget_4.setItem(row, 0, item_price)
                # Mevcut fiyatı bul ve tabloyu bu fiyata kaydır
                current_price_index = price_range.index(price)  # Mevcut fiyatın index'ini bul
                self.tableWidget_4.selectRow(current_price_index)  # Mevcut satırı seç
                current_item = self.tableWidget_4.item(current_price_index, 0)  # Mevcut fiyatın hücresini al
                # Eğer tablo yüksekliği toplam satır sayısından az ise kaydırma işlemi gerekir
                if self.tableWidget_4.verticalScrollBar().isVisible():
                    self.tableWidget_4.scrollToItem(current_item, QtWidgets.QAbstractItemView.PositionAtCenter)  # Hücreyi ortala
                self.tableWidget_4.clearSelection()
                self.update_OrderTable(Symbol)
                self.setup_timer()
            elif eqinfo["message"] == 'Beklenmedik bir hata oluştu.':
                print("Oturum Zaman Aşımına Uğradı.")
                self.reset()
        except Exception as e:
            print(f"Hata: {e}")
 
    def reset(self):
        def showErrorDialog(message):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Bir Hata Oluştu")
            msg.setInformativeText(message)
            msg.setWindowTitle("Hata")
            msg.exec_()
        showErrorDialog("Oturumunuz sonlanmıştır. Lütfen internet bağlantınızı kontrol ettikten sonra programı tekrar çalıştırın.")
        for window in QApplication.topLevelWidgets():
            if window.isVisible():
                window.close()

    def update_OrderTable(self, symbol):
        try:
            self.updating_order_table = True 
            sql.control()
            with sqlite3.connect('config.db') as conn:
                cursor = conn.cursor()
                
                # Belirtilen sembol için tüm emirleri sorgula
                cursor.execute('''
                    SELECT price, SUM(lot), direction FROM transactions
                    WHERE symbol = ? GROUP BY price, direction
                ''', (symbol,))

                orders = cursor.fetchall()
                # Öncelikle, tüm alış ve satış sütunlarını sıfırla
                for row in range(self.tableWidget_4.rowCount()):
                    self.tableWidget_4.setItem(row, 1, QTableWidgetItem(""))  # Alış sütununu sıfırla
                    self.tableWidget_4.setItem(row, 2, QTableWidgetItem(""))  # Satış sütununu sıfırla

                # Tablonun her bir satırını dolaş ve uygun emirleri yerleştir
                for row in range(self.tableWidget_4.rowCount()):
                    item_price = self.tableWidget_4.item(row, 0)
                    if item_price is not None:
                        price = float(item_price.text())
                        # Sorgulanan emirler içinde uygun fiyatı bul ve yerleştir
                        for order_price, order_lot, order_direction in orders:
                            if price == order_price:
                                # Eğer alım emri ise
                                if order_direction == "BUY":
                                    # Alım sütununa lot miktarını ekle
                                    self.tableWidget_4.setItem(row, 1, QTableWidgetItem(str(order_lot)))
                                # Eğer satım emri ise
                                elif order_direction == "SELL":
                                    # Satım sütununa lot miktarını ekle
                                    self.tableWidget_4.setItem(row, 2, QTableWidgetItem(str(order_lot)))

                # Reset the updating_order_table flag
                self.updating_order_table = False
        except Exception as e:
            print(f"update_OrderTable error: {e}") 
            self.updating_order_table = False  

    def status_update_OrderTable(self, symbol):
        try:
            self.updating_order_table = True 
            sql.control()
            with sqlite3.connect('config.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT price, SUM(lot), direction FROM transactions
                    WHERE symbol = ? GROUP BY price, direction
                ''', (symbol,))
                orders = cursor.fetchall()

                # Veritabanından gelen emirleri bir sözlükte sakla
                db_orders = {(order_price, order_direction): order_lot for order_price, order_lot, order_direction in orders}

                # Tablodaki mevcut verileri bir sözlükte sakla, yalnızca dolu olanları al
                table_orders = {}
                for row in range(self.tableWidget_4.rowCount()):
                    item_price = self.tableWidget_4.item(row, 0)
                    if item_price is not None and item_price.text().strip() != "":
                        price = float(item_price.text())
                        buy_item = self.tableWidget_4.item(row, 1)
                        sell_item = self.tableWidget_4.item(row, 2)
                        buy_lot = buy_item.text() if buy_item and buy_item.text().strip() != "" else None
                        sell_lot = sell_item.text() if sell_item and sell_item.text().strip() != "" else None
                        if buy_lot or sell_lot:
                            table_orders[price] = {"BUY": buy_lot, "SELL": sell_lot}
                formatted_table_orders = {}
                for price, orders in table_orders.items():
                    for direction, lot in orders.items():
                        if lot:  # Sadece dolu olan lotları dahil et
                            formatted_table_orders[(price, direction)] = int(lot)

                # Eğer veriler aynıysa, işlem yapma
                if formatted_table_orders == db_orders:
                    pass
                else:
                    # Fark varsa, güncelleme işlemlerini yap
                    for row in range(self.tableWidget_4.rowCount()):
                        item_price = self.tableWidget_4.item(row, 0)
                        if item_price is not None and item_price.text().strip() != "":
                            price = float(item_price.text())
                            for direction in ["BUY", "SELL"]:
                                col = 1 if direction == "BUY" else 2
                                if (price, direction) in db_orders:
                                    # Veritabanında varsa güncelle
                                    lot = db_orders[(price, direction)]
                                    self.tableWidget_4.setItem(row, col, QTableWidgetItem(str(lot)))
                                else:
                                    # Veritabanında yoksa sıfırla
                                    self.tableWidget_4.setItem(row, col, QTableWidgetItem(""))

                # Reset the updating_order_table flag
                self.updating_order_table = False
        except Exception as e:
            print(f"update_OrderTable error: {e}")
            self.updating_order_table = False

    def update_portfolio(self, refno, symbol, lot, price, direction):
        try:
            with sqlite3.connect('config.db') as conn:  # Veritabanı adını ve yolu doğru olduğundan emin olun
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO transactions (ref_number, symbol, lot, price, direction)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(ref_number) DO UPDATE SET
                    symbol = excluded.symbol,
                    lot = excluded.lot,
                    price = excluded.price,
                    direction = excluded.direction
                ''', (refno, symbol, lot, price, direction))
                
                # Değişiklikleri kaydet
                conn.commit()
            # Bağlantıyı kapat
            conn.close()
        except Exception as e:
            print(f"update_portfolio error: {e}")
          
    def setup_timer(self):
        # Timer'ı kur
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.process_socket_data)
        self.timer.start(1000)  # Milisaniye cinsinden zaman aralığını ayarla (1000 ms = 1 saniye)

    def process_socket_data(self):
        try:
            symbol = self.label_10.text()
            sql.control()
            with sqlite3.connect('config.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM stocks WHERE symbol = ?", (symbol,))
                symbol_data = cursor.fetchone()

            if symbol_data:
                # Sorgu sonucu (symbol, price, change, high, change_percentage, low) olarak dönecek
                _, price, change, high, change_percentage, low = symbol_data

                # Etiketleri güncelle
                self.label_11.setText(f"{high}")
                self.label_12.setText(f"{low}")
                self.label_14.setText(f"{change_percentage}")
                self.label_24.setText(f"{change}")

                # Eğer yeni fiyat, son fiyattan farklıysa, satırı renklendir.
                if price is not None and price != self.last_price:
                    self.color_row(price)
                    self.last_price = price  # Son fiyatı güncelle.
            else:
                if not self.eq: 
                    eqinfo = algo.GetEquityInfo(symbol)
                    if eqinfo != False and eqinfo["content"]["lst"] != "-":
                        price = float(eqinfo["content"]["flr"])
                    if price is not None and price != self.last_price:
                                        self.color_row(price)
                                        self.last_price = price  # Son fiyatı güncelle.
                    self.eq = True                 
            self.status_update_OrderTable(symbol)
            
        except sqlite3.Error as e:
            print(f"Veritabanı hatası: {e}")
        except Exception as e:
            print(f"process_socket_data error: {e}")

    def color_row(self, price):
        try:
            yellow_brush = QBrush(QColor(255, 255, 0))
            white_brush = QBrush(QColor(255, 255, 255))

            for row in range(self.tableWidget_4.rowCount()):
                item = self.tableWidget_4.item(row, 0)
                if not item:  # Eğer hücre boşsa yeni bir QTableWidgetItem oluştur
                    item = QTableWidgetItem()
                    self.tableWidget_4.setItem(row, 0, item)

                try:
                    current_price = float(item.text())
                    if current_price == price:
                        item.setBackground(yellow_brush)
                    else:
                        item.setBackground(white_brush)  # Diğer fiyatları beyazla boyayarak temizle
                except ValueError:
                    pass  # Metni float'a dönüştürme hatası. Gerekirse burada bir işlem yapabilirsiniz.
                
            self.tableWidget_4.viewport().update()
        except Exception as e:
            print(f"color_row error: {e}")

    def on_item_changed(self, item):
        if self.updating_order_table or self.deleting_order:
            return
        if item.column() == 1 or item.column() == 2:
            self.send_order(item)

    def send_order(self, item):
        try:
            def delete_order(ref_number):
                # Algoritmadan siparişi silme işlemi
                delete = algo.DeleteOrder(id=ref_number, subAccount="")
                if delete and delete.get("success"):
                    try:
                        sql.control()
                        with sqlite3.connect('config.db') as conn:
                            cursor = conn.cursor()
                            # SQL sorgusu ile siparişi sil
                            cursor.execute('DELETE FROM transactions WHERE ref_number = ?', (ref_number,))
                            # Değişiklikleri kaydet
                            conn.commit()
                    except sqlite3.Error as e:
                        # Veritabanı işlemi sırasında bir hata olursa yazdır
                        print(f"Veritabanından {ref_number} referans numaralı emri silerken bir hata meydana geldi: {e}")

                    print(f"Referans numarası {ref_number} olan emir veritabanından silindi.")
                else:
                    # Eğer emir silme başarısızsa uyarı ver
                    print(f"Referans numarası {ref_number} olan emir silinemedi.")      
            
            def order_api(symbol, direction, price, lot):
                try:
                    order = algo.SendOrder(
                        symbol=symbol, 
                        direction=direction, 
                        pricetype="limit", 
                        lot=f"{lot}", 
                        price=f"{price}", 
                        sms=False, 
                        email=False,
                        subAccount=""
                    )
                    
                    if order and order.get("success"):

                        content = order["content"]

                        # "Referans Numaraniz:" ifadesini arayip ona gore basari veya basarisizlik loglari yazdirma
                        if "Referans Numaranız:" in content:
                            ref_number = content.split("Referans Numaranız:")[1].split(";")[0].strip()
                            print(f"{direction} {lot} lot {symbol} order sent at {price} price. Reference Number: {ref_number}")
                            self.update_portfolio(ref_number,symbol,lot,price,direction)
                            
                        else:
                            print(f"Error on {direction} {symbol} {lot} lot at {price}. Response: {content}")
                    else:
                        print(f"Failed to send order {direction} {symbol} {lot} lot at {price}. Response: {order}")
                except Exception as e:
                    print(f"Error while send_order function on {direction} {symbol}: {e}")
                    
            value = item.text().strip()
            column = item.column()
            row = item.row()
            price_item = self.tableWidget_4.item(row, 0)
            symbol = self.label_10.text()

            if not price_item:
                print("Price information is missing.")
                return

            price = float(price_item.text())
            lot = float(value)
            direction = 'BUY' if column == 1 else 'SELL'
            sql.control()
            with sqlite3.connect('config.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT ref_number FROM transactions
                    WHERE symbol = ? AND price = ? AND direction = ?
                ''', (symbol, price, direction))
                result = cursor.fetchone()
                
                if result:
                    ref_number = result[0]
                    delete_order(ref_number)
            order_api(symbol, direction, price, lot)
        except Exception as e:
            print(f"send_order error: {e}")

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.KeyPress and source is self.tableWidget_4:
            # Delete tuşuna basılırsa
            if event.key() == QtCore.Qt.Key_Delete:
                selected_items = self.tableWidget_4.selectedItems()
                if selected_items:
                    current_item = self.tableWidget_4.currentItem()
                    if current_item is not None:
                        row = current_item.row()
                        column = current_item.column()
                        # Eğer 'Alış' veya 'Satış' kolonu seçiliyse ve boş değilse
                        if column in [1, 2] and current_item.text() != '':
                            # Lot miktarını al
                            lot_item = current_item.text()  
                            lot = int(lot_item) if lot_item else 0
                            # Hücreyi temizle ve delete_order fonksiyonunu çağır
                            self.delete_order(row, column, lot)
                            current_item.setText('')  # Hücreyi boşalt
                    return True
        return super(Tahta_Form, self).eventFilter(source, event)

    def delete_order(self, row, column, lot):
        
        def send_delete(id):
            delete = algo.DeleteOrder(id=id, subAccount="")
            if delete and delete.get("success"):
                try:
                    content = delete["content"]
                    content_json = json.dumps(content)
                    print("Emir Silindi, " + content_json)
                except Exception as e:
                    print(f"delete_order fonksiyonunda hata olustu: {e}")
        try:
            self.updating_order_table = True 
            price_item = self.tableWidget_4.item(row, 0)  # Fiyat hücresini al
            order_type = 'BUY' if column == 1 else 'SELL'
            symbol = self.label_10.text()  # Sembol değerini label_10'dan al
            if price_item:
                price = float(price_item.text())
                sql.control()
                with sqlite3.connect('config.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        SELECT ref_number FROM transactions
                        WHERE symbol = ? AND price = ? AND lot = ? AND direction = ?
                    ''', (symbol, price, lot, order_type))
                    result = cursor.fetchone()
                    if result:
                        # Eğer kayıt varsa, referans numarası ile delete işlemi yap
                        ref_number = result[0]
                        send_delete(ref_number)
                        # Kaydı veritabanından sil
                        cursor.execute('DELETE FROM transactions WHERE ref_number = ?', (ref_number,))
                        conn.commit()
                        print(f"Order with reference {ref_number} has been deleted.")
                    else:
                        print(f"No order found with the provided criteria: {symbol}, {price}, {lot}, {order_type}")
        except Exception as e:
            print(f"delete_order error: {e}")
        finally:
            self.tableWidget_4.item(row, column).setText('')
            self.updating_order_table = False 
           
class TahtaScreen(QWidget):
    def __init__(self, main_screen):
        super(TahtaScreen, self).__init__()
        self.ui = Tahta_Form()
        self.ui.setupUi(self)
        Main_Form.increase_form_count()  # Yeni form açıldığında form_count artır

    def closeEvent(self, event):
        Main_Form.decrease_form_count()  # Form kapandığında form_count azalt
        event.accept()  # Pencerenin kapatılmasını kabul et

if __name__ == "__main__":
    sql.control()
    app = QApplication(sys.argv)
    login_form = LoginForm()
    sms_screen = SMSScreen()
    api_key = login_form.loadApiKey()
    algo = Backend(api_key=api_key, username="", password="")
    if algo.autologin():
        main_screen = MainScreen()
        main_screen.show()
    else:
        login_screen = LoginScreen()
        login_screen.show()
    sys.exit(app.exec_())