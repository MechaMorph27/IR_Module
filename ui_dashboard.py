import sys

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from bt3562_client import BT3562Client
from range_checker import check
from excel_logger import save
from config import CONFIG
from datetime import datetime
from setting import SettingsWindow
from theme_manager import load_theme, save_theme


# ================= ISSUE MANAGEMENT =================

from issue_store import (
    load_issues,
    add_issue,
    delete_issue
)

from security_manager import get_password



# ================= RESULT POPUP =================

class ResultPopup(QDialog):

    def __init__(self, result):

        super().__init__()


        self.result = result


        self.setWindowTitle(
            "Battery Tester System"
        )


        # Title bar logo

        self.setWindowIcon(
            QIcon("logo1.png")
        )


        self.setModal(True)


        self.setFixedSize(
            380,
            320
        )


        self.logo_pixmap = QPixmap(
            "logo1.png"
        )



        self.setStyleSheet("""

            QDialog {

                background-color:#0b0f14;

            }


            QLabel {

                color:white;

                font-weight:bold;

            }


            QComboBox {

                background-color:#1c1f26;

                color:white;

                border:1px solid #333;

                padding:6px;

                border-radius:5px;

            }


            QPushButton {

                background-color:#2d6cdf;

                color:white;

                font-weight:bold;

                padding:7px;

                border-radius:6px;

            }


            QPushButton:hover {

                background-color:#3b82f6;

            }

        """)



        layout = QVBoxLayout()


        layout.setContentsMargins(
            20,
            20,
            20,
            20
        )



        # ================= RESULT TEXT =================


        result_label = QLabel(
            result
        )


        result_label.setAlignment(
            Qt.AlignCenter
        )



        if result == "PASS":


            result_label.setStyleSheet("""
                color:#00ff88;
                font-size:60px;
                font-weight:bold;
            """)


        else:


            result_label.setStyleSheet("""
                color:#ff3b3b;
                font-size:60px;
                font-weight:bold;
            """)



        layout.addWidget(
            result_label
        )



        # ================= FAIL ISSUE AREA =================


        if result == "FAIL":


            issue_label = QLabel(
                "Issue :"
            )


            issue_label.setStyleSheet(
                "font-size:16px;"
            )



            self.issue_box = QComboBox()


            self.load_issue_list()



            layout.addWidget(
                issue_label
            )


            layout.addWidget(
                self.issue_box
            )



            button_row = QHBoxLayout()



            self.add_btn = QPushButton(
                "+"
            )


            self.delete_btn = QPushButton(
                "-"
            )



            self.add_btn.setFixedSize(
                45,
                35
            )


            self.delete_btn.setFixedSize(
                45,
                35
            )



            self.add_btn.clicked.connect(
                self.add_issue_flow
            )


            self.delete_btn.clicked.connect(
                self.delete_issue_flow
            )



            button_row.addStretch()


            button_row.addWidget(
                self.add_btn
            )


            button_row.addWidget(
                self.delete_btn
            )


            button_row.addStretch()



            layout.addLayout(
                button_row
            )



        layout.addStretch()



        # ================= OK BUTTON =================


        ok_btn = QPushButton(
            "OK"
        )


        ok_btn.setFixedSize(
            140,
            45
        )


        ok_btn.clicked.connect(
            self.accept
        )


        layout.addWidget(
            ok_btn,
            alignment=Qt.AlignCenter
        )



        self.setLayout(
            layout
        )



    # =====================================================
    # LOAD ISSUE LIST
    # =====================================================


    def load_issue_list(self):

        self.issue_box.clear()


        issues = load_issues()


        self.issue_box.addItems(
            issues
        )



    # =====================================================
    # ADD ISSUE (+)
    # =====================================================


    def add_issue_flow(self):


        password, ok = QInputDialog.getText(

            self,

            "Admin Authentication",

            "Enter Password:",

            QLineEdit.Password

        )



        if not ok:

            return



        if password != get_password():


            QMessageBox.critical(

                self,

                "Error",

                "Wrong Password"

            )


            return



        issue, ok = QInputDialog.getText(

            self,

            "Add Issue",

            "Enter Issue Name:"

        )



        if not ok:

            return



        if issue.strip():


            add_issue(
                issue
            )


            self.load_issue_list()



    # =====================================================
    # DELETE ISSUE (-)
    # =====================================================


    def delete_issue_flow(self):


        current = self.issue_box.currentText()



        if not current:

            return



        password, ok = QInputDialog.getText(

            self,

            "Admin Authentication",

            "Enter Password:",

            QLineEdit.Password

        )



        if not ok:

            return



        if password != get_password():


            QMessageBox.critical(

                self,

                "Error",

                "Wrong Password"

            )


            return



        delete_issue(
            current
        )


        self.load_issue_list()



    # =====================================================
    # GET SELECTED ISSUE
    # =====================================================


    def get_issue(self):


        if self.result == "FAIL":

            return self.issue_box.currentText()


        return ""



    # =====================================================
    # LOGO WATERMARK
    # =====================================================


    def paintEvent(self,event):


        super().paintEvent(
            event
        )



        if self.logo_pixmap.isNull():

            return



        painter = QPainter(
            self
        )


        painter.setRenderHint(
            QPainter.SmoothPixmapTransform
        )


        painter.setOpacity(
            0.08
        )



        logo = self.logo_pixmap.scaled(

            230,

            230,

            Qt.KeepAspectRatio,

            Qt.SmoothTransformation

        )



        x = (

            self.width()

            -

            logo.width()

        ) // 2



        y = (

            self.height()

            -

            logo.height()

        ) // 2



        painter.drawPixmap(

            x,

            y,

            logo

        )


# ================= DASHBOARD =================

class Dashboard(QWidget):

    def __init__(self, op, shift):

        super().__init__()

        self.op = op
        self.shift = shift

        self.device = BT3562Client(
            CONFIG["ip"]
        )

        self.points = CONFIG["points"]

        self.i = 0
        self.results = []
        self.detail_rows = []

        self.setWindowTitle(
            "Battery Tester System"
        )

        self.setWindowIcon(
            QIcon("logo1.png")
        )

        self.showMaximized()

        self.logo_pixmap = QPixmap(
            "logo1.png"
        )

        self.setStyleSheet("""
            QWidget{
                background-color:#0b0f14;
                color:white;
                font-size:13px;
            }

            QLineEdit{
                background-color:rgba(10,15,25,70);
                border:1px solid rgba(255,255,255,0.12);
                padding:6px;
                border-radius:6px;
                color:white;
                font-weight:bold;
            }

            QTableWidget{
                background-color:rgba(10,15,25,60);
                color:white;
                gridline-color:rgba(255,255,255,0.08);
                font-weight:bold;
            }

            QHeaderView::section{
                background-color:rgba(20,30,50,120);
                color:white;
                font-weight:bold;
                padding:6px;
            }

            QPushButton{
                background-color:rgba(45,108,223,180);
                color:white;
                font-weight:bold;
                padding:7px;
                border-radius:8px;
            }

            QPushButton:hover{
                background-color:rgba(59,130,246,220);
            }
        """)

        main = QVBoxLayout()

        # ================= HEADER =================

        header = QHBoxLayout()

        op_lbl = QLabel(
            f"Operator: {op}"
        )

        sh_lbl = QLabel(
            f"Shift: {shift}"
        )

        op_lbl.setStyleSheet(
            "font-size:18px;font-weight:bold;"
        )

        sh_lbl.setStyleSheet(
            "font-size:18px;font-weight:bold;"
        )

        header.addStretch()
        header.addWidget(op_lbl)
        header.addSpacing(120)
        header.addWidget(sh_lbl)
        header.addStretch()

        main.addLayout(header)

        # ================= MODULE AREA =================

        row = QHBoxLayout()

        lbl_module = QLabel(
            "Module ID:"
        )

        lbl_module.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        self.module = QLineEdit()

        self.module.setPlaceholderText(
            "Scan Module ID"
        )

        self.module.setFixedSize(
            220,
            34
        )

        self.module.returnPressed.connect(
            self.start_test
        )

        self.settings_btn = QPushButton(
            "⚙"
        )

        self.settings_btn.setFixedSize(
            42,
            42
        )

        self.settings_btn.clicked.connect(
            self.open_settings
        )

        row.addStretch()
        row.addWidget(lbl_module)
        row.addSpacing(8)
        row.addWidget(self.module)
        row.addStretch()
        row.addWidget(self.settings_btn)

        main.addLayout(row)

        # ================= TOP CONTROLS =================

        top = QHBoxLayout()

        self.reset_btn = QPushButton(
            "RESET"
        )

        self.reset_btn.setFixedSize(
            130,
            50
        )

        self.reset_btn.setStyleSheet("""
            QPushButton{
                background-color:#e53935;
                color:white;
                font-weight:bold;
                font-size:20px;
                border-radius:8px;
            }

            QPushButton:hover{
                background-color:#ff5252;
            }
        """)

        self.reset_btn.clicked.connect(
            self.reset_all
        )

        ready_style = """
            QLabel{
                background-color:rgba(30,40,60,180);
                border:1px solid rgba(255,255,255,0.12);
                border-radius:10px;
                font-size:20px;
                font-weight:bold;
                padding:8px;
            }
        """

        self.point = QLabel(
            "READY"
        )

        self.point.setAlignment(
            Qt.AlignCenter
        )

        self.point.setFixedSize(
            150,
            50
        )

        self.point.setStyleSheet(
            ready_style
        )

        self.status = QLabel(
            "READY"
        )

        self.status.setAlignment(
            Qt.AlignCenter
        )

        self.status.setFixedSize(
            150,
            50
        )

        self.status.setStyleSheet(
            ready_style
        )

        top.addStretch()
        top.addWidget(self.reset_btn)
        top.addWidget(self.point)
        top.addWidget(self.status)
        top.addStretch()

        main.addLayout(top)


        # ================= TABLE =================

        self.table = QTableWidget(
            len(self.points),
            4
        )

        self.table.setHorizontalHeaderLabels(
            [
                "Points",
                "Voltage (V)",
                "IR (mΩ)",
                "Status"
            ]
        )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        main.addWidget(
            self.table
        )

        self.setLayout(
            main
        )

        QTimer.singleShot(
            300,
            self.focus_module
        )

    # ================= BACKGROUND LOGO =================

    def paintEvent(
        self,
        event
    ):

        super().paintEvent(event)

        if self.logo_pixmap.isNull():
            return

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.SmoothPixmapTransform
        )

        painter.setOpacity(
            0.06
        )

        scaled = self.logo_pixmap.scaled(
            700,
            700,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        x = (
            self.width()
            -
            scaled.width()
        ) // 2

        y = (
            self.height()
            -
            scaled.height()
        ) // 2

        painter.drawPixmap(
            x,
            y,
            scaled
        )

    # ================= SETTINGS =================

    def open_settings(self):

        dlg = SettingsWindow()

        dlg.exec()

    def focus_module(self):

        self.module.setFocus()

    # ================= START TEST =================

    def start_test(self):

        self.mid = self.module.text().strip()

        if not self.mid:
            return

        self.module.setReadOnly(True)

        self.i = 0

        self.results = []

        self.detail_rows = []

        self.run_next()

    # ================= RUN =================

    def run_next(self):

        if self.i >= len(self.points):

            self.finish()

            return

        self.current = self.points[self.i]

        self.point.setText(
            self.current
        )

        QTimer.singleShot(
            300,
            self.measure
        )

    # ================= MEASURE =================

    def measure(self):

        v, ir = map(
            float,
            self.device.read().split(",")
        )

        status, _ = check(
            self.current,
            v,
            ir
        )

        self.results.append(
            status
        )

        self.table.setItem(
            self.i,
            0,
            QTableWidgetItem(
                self.current
            )
        )

        self.table.setItem(
            self.i,
            1,
            QTableWidgetItem(
                str(v)
            )
        )

        self.table.setItem(
            self.i,
            2,
            QTableWidgetItem(
                str(ir)
            )
        )

        item = QTableWidgetItem(
            status
        )

        if status == "PASS":

            item.setForeground(
                QColor("#00ff88")
            )

        else:

            item.setForeground(
                QColor("#ff3b3b")
            )

        self.table.setItem(
            self.i,
            3,
            item
        )

        self.detail_rows.append({

            "Module": self.mid,

            "Point": self.current,

            "Voltage": v,

            "IR": ir,

            "Status": status

        })

        self.i += 1

        QTimer.singleShot(
            400,
            self.run_next
        )

    # ================= FINISH =================

    def finish(self):

        result = (
            "PASS"
            if all(r == "PASS" for r in self.results)
            else "FAIL"
        )

        self.status.setText(
            result
        )

        issue = ""

        if result == "FAIL":

            popup = ResultPopup(result)

            if popup.exec() == QDialog.Accepted:
                issue = popup.selected_issue

        else:

            ResultPopup(result).exec()

        summary = {

            "Date":
            datetime.now().strftime("%d-%m-%Y"),

            "Time":
            datetime.now().strftime("%H:%M:%S"),

            "Shift":
            self.shift,

            "Operator":
            self.op,

            "Module":
            self.mid,

            "Result":
            result,

            "Issue":
            issue

        }

        save(
            summary,
            self.detail_rows
        )


    # ================= RESET =================

    def reset_all(self):

        self.module.setReadOnly(
            False
        )

        self.module.clear()

        self.i = 0

        self.results = []

        self.detail_rows = []

        self.point.setText(
            "READY"
        )

        self.status.setText(
            "READY"
        )

        self.table.clearContents()

        self.focus_module()