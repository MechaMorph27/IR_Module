from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from config import CONFIG
from config_store import save_config
from security_manager import get_password, save_password
from theme_store import load_theme, save_theme


class SettingsWindow(QDialog):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon("logo1.png"))
        self.setFixedSize(700,500)

        self.original = CONFIG["limits"].copy()
        self.edit_mode = False

        self.theme = load_theme()

        # background logo
        self.logo = QPixmap("logo1.png")

        self.setStyleSheet("""
        QDialog{
            background-color:#0b0f14;
            color:white;
        }

        QLabel{
            color:white;
            font-size:13px;
            font-weight:bold;
        }

        QLineEdit{
            background-color:#1c1f26;
            color:white;
            border:1px solid #333;
            padding:5px;
            border-radius:5px;
        }

        QPushButton{
            background-color:#2d6cdf;
            color:white;
            padding:8px;
            border-radius:6px;
            font-weight:bold;
        }

        QPushButton:hover{
            background-color:#3b82f6;
        }
        """)

        self.build_ui()
        self.update_ui_mode()

    def build_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(
            15,
            10,
            15,
            10
        )

        layout.setSpacing(5)

        title = QLabel("SELECT RANGE")

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setStyleSheet("""
        font-size:20px;
        font-weight:bold;
        color:#33a1ff;
        """)

        layout.addWidget(title)

        layout.addSpacing(10)

        grid = QGridLayout()

        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(8)

        self.cell_v_max = QLineEdit(
            str(CONFIG["limits"]["cell_v_max"])
        )

        self.cell_v_min = QLineEdit(
            str(CONFIG["limits"]["cell_v_min"])
        )

        self.cell_ir_max = QLineEdit(
            str(CONFIG["limits"]["cell_ir_max"])
        )

        self.cell_ir_min = QLineEdit(
            str(CONFIG["limits"]["cell_ir_min"])
        )

        self.module_v_max = QLineEdit(
            str(CONFIG["limits"]["module_v_max"])
        )

        self.module_v_min = QLineEdit(
            str(CONFIG["limits"]["module_v_min"])
        )

        self.module_ir_max = QLineEdit(
            str(CONFIG["limits"]["module_ir_max"])
        )

        self.module_ir_min = QLineEdit(
            str(CONFIG["limits"]["module_ir_min"])
        )

        cell_title = QLabel(
            "CELL (B- TO B13)"
        )

        module_title = QLabel(
            "MODULE"
        )

        cell_title.setAlignment(
            Qt.AlignCenter
        )

        module_title.setAlignment(
            Qt.AlignCenter
        )
\
        grid.addWidget(
            cell_title,
            0,
            1,
            1,
            2
        )

        grid.addWidget(
            module_title,
            0,
            4,
            1,
            2
        )

        grid.addWidget(
            QLabel("Voltage"),
            1,
            1
        )

        grid.addWidget(
            QLabel("IR"),
            1,
            2
        )

        separator_top = QLabel("|")
        separator_top.setAlignment(
            Qt.AlignCenter
        )

        grid.addWidget(
            separator_top,
            1,
            3
        )

        grid.addWidget(
            QLabel("Voltage"),
            1,
            4
        )

        grid.addWidget(
            QLabel("IR"),
            1,
            5
        )

        grid.addWidget(
            QLabel("MAX"),
            2,
            0
        )

        grid.addWidget(
            self.cell_v_max,
            2,
            1
        )

        grid.addWidget(
            self.cell_ir_max,
            2,
            2
        )

        separator_max = QLabel("|")
        separator_max.setAlignment(
            Qt.AlignCenter
        )

        grid.addWidget(
            separator_max,
            2,
            3
        )

        grid.addWidget(
            self.module_v_max,
            2,
            4
        )

        grid.addWidget(
            self.module_ir_max,
            2,
            5
        )

        grid.addWidget(
            QLabel("MIN"),
            3,
            0
        )

        grid.addWidget(
            self.cell_v_min,
            3,
            1
        )

        grid.addWidget(
            self.cell_ir_min,
            3,
            2
        )

        separator_min = QLabel("|")

        separator_min.setAlignment(
            Qt.AlignCenter
        )

        grid.addWidget(
            separator_min,
            3,
            3
        )

        grid.addWidget(
            self.module_v_min,
            3,
            4
        )

        grid.addWidget(
            self.module_ir_min,
            3,
            5
        )

        layout.addLayout(grid)

        layout.addSpacing(8)

        theme_title = QLabel(
            "DASHBOARD THEME"
        )

        theme_title.setAlignment(
            Qt.AlignCenter
        )

        theme_title.setStyleSheet("""
        font-size:18px;
        font-weight:bold;
        color:#33a1ff;
        """)

        layout.addWidget(
            theme_title
        )

        self.theme_btn = QPushButton(
            "CHANGE THEME"
        )

        self.theme_btn.setFixedSize(
            200,
            40
        )


        self.theme_btn.clicked.connect(
            self.theme_flow
        )

        layout.addWidget(
            self.theme_btn,
            alignment=Qt.AlignCenter
        )

        # reduced empty space
        layout.addSpacing(8)


        self.create_buttons(
            layout
        )

        self.setLayout(
            layout
        )

    def create_buttons(self,layout):
        btn_row = QHBoxLayout()

        self.reset_btn = QPushButton(
            "RESET"
        )

        self.edit_btn = QPushButton(
            "EDIT"
        )

        self.save_btn = QPushButton(
            "SAVE"
        )

        self.change_pass_btn = QPushButton(
            "CHANGE PASSWORD"
        )

        self.close_btn = QPushButton(
            "CLOSE"
        )

        self.reset_btn.setFixedSize(
            120,
            40
        )

        self.edit_btn.setFixedSize(
            120,
            40
        )

        self.save_btn.setFixedSize(
            120,
            40
        )

        self.change_pass_btn.setFixedSize(
            170,
            40
        )

        self.close_btn.setFixedSize(
            120,
            40
        )

        self.reset_btn.clicked.connect(
            self.reset_flow
        )

        self.edit_btn.clicked.connect(
            self.edit_flow
        )

        self.save_btn.clicked.connect(
            self.save_flow
        )

        self.change_pass_btn.clicked.connect(
            self.change_password_flow
        )

        self.close_btn.clicked.connect(
            self.close
        )

        btn_row.addStretch()


        btn_row.addWidget(
            self.reset_btn
        )

        btn_row.addWidget(
            self.edit_btn
        )

        btn_row.addWidget(
            self.save_btn
        )

        btn_row.addWidget(
            self.change_pass_btn
        )

        btn_row.addWidget(
            self.close_btn
        )


        btn_row.addStretch()


        layout.addLayout(
            btn_row
        )

    # =====================================================
    # EDIT MODE
    # =====================================================

    def update_ui_mode(self):


        fields = [

            self.cell_v_max,
            self.cell_v_min,

            self.cell_ir_max,
            self.cell_ir_min,

            self.module_v_max,
            self.module_v_min,

            self.module_ir_max,
            self.module_ir_min

        ]

        if self.edit_mode:


            for field in fields:

                field.setReadOnly(False)

            self.edit_btn.hide()

            self.save_btn.show()

            self.change_pass_btn.show()

        else:

            for field in fields:

                field.setReadOnly(True)

            self.edit_btn.show()

            self.save_btn.hide()

            self.change_pass_btn.hide()

    # =====================================================
    # EDIT AUTHENTICATION
    # =====================================================

    def edit_flow(self):

        pwd,ok = QInputDialog.getText(

            self,

            "Admin Authentication",

            "Enter Password:",

            QLineEdit.Password
        )

        if not ok:
            return
        
        if pwd != get_password():

            QMessageBox.critical(

                self,

                "Error",

                "Wrong Password"

            )

            return

        self.edit_mode = True

        self.update_ui_mode()

    # =====================================================
    # SAVE RANGE
    # =====================================================

    def save_flow(self):


        try:

            CONFIG["limits"] = {

                "cell_v_min":
                float(self.cell_v_min.text()),

                "cell_v_max":
                float(self.cell_v_max.text()),

                "cell_ir_min":
                float(self.cell_ir_min.text()),

                "cell_ir_max":
                float(self.cell_ir_max.text()),

                "module_v_min":
                float(self.module_v_min.text()),

                "module_v_max":
                float(self.module_v_max.text()),

                "module_ir_min":
                float(self.module_ir_min.text()),

                "module_ir_max":
                float(self.module_ir_max.text())

            }

        except ValueError:

            QMessageBox.warning(

                self,

                "Error",

                "Enter valid values"

            )

            return

        save_config(
            CONFIG
        )

        self.edit_mode = False

        self.update_ui_mode()

        QMessageBox.information(

            self,

            "Saved",

            "Settings Updated Successfully"

        )

    # =====================================================
    # RESET RANGE
    # =====================================================

    def reset_flow(self):


        pwd,ok = QInputDialog.getText(

            self,

            "Admin Authentication",

            "Enter Password:",

            QLineEdit.Password

        )

        if not ok:

            return

        if pwd != get_password():


            QMessageBox.critical(

                self,

                "Error",

                "Wrong Password"

            )

            return

        CONFIG["limits"] = self.original.copy()

        save_config(
            CONFIG
        )

        self.load_values()

        QMessageBox.information(

            self,

            "Reset",

            "Values Restored"

        )

    def change_password_flow(self):
        dialog=QDialog(self)
        dialog.setWindowTitle("Change Password")
        dialog.setFixedSize(350,230)
        layout=QVBoxLayout(dialog)

        old=QLineEdit()
        old.setEchoMode(QLineEdit.Password)
        old.setPlaceholderText("Current Password")

        new=QLineEdit()
        new.setEchoMode(QLineEdit.Password)
        new.setPlaceholderText("New Password")

        confirm=QLineEdit()
        confirm.setEchoMode(QLineEdit.Password)
        confirm.setPlaceholderText("Confirm Password")

        btn=QPushButton("UPDATE")

        layout.addWidget(old)
        layout.addWidget(new)
        layout.addWidget(confirm)
        layout.addWidget(btn)

        def update():
            if old.text()!=get_password():
                QMessageBox.critical(dialog,"Error","Wrong Password")
                return

            if new.text()!=confirm.text():
                QMessageBox.warning(dialog,"Error","Password mismatch")
                return

            if not new.text().strip():
                return

            save_password(new.text())

            QMessageBox.information(
                dialog,
                "Success",
                "Password Updated"
            )

            dialog.accept()

        btn.clicked.connect(update)
        dialog.exec()

    # ================= THEME =================

    def theme_flow(self):

        pwd,ok=QInputDialog.getText(
            self,
            "Admin Authentication",
            "Enter Password:",
            QLineEdit.Password
        )

        if not ok:
            return

        if pwd!=get_password():
            QMessageBox.critical(
                self,
                "Error",
                "Wrong Password"
            )
            return

        dialog=QDialog(self)
        dialog.setWindowTitle("Dashboard Theme")
        dialog.setFixedSize(350,350)

        layout=QVBoxLayout(dialog)

        colors=[
            ("Dashboard Background","background"),
            ("Text Colour","text"),
            ("Button Colour","button"),
            ("Input Box Colour","input"),
            ("Table Colour","table")
        ]

        for name,key in colors:

            btn=QPushButton(name)

            btn.clicked.connect(
                lambda checked=False,k=key:self.pick_color(k)
            )

            layout.addWidget(btn)

        save_btn=QPushButton("SAVE & LOCK")

        save_btn.clicked.connect(
            lambda:self.save_theme_changes(dialog)
        )

        layout.addWidget(save_btn)

        dialog.exec()

    def pick_color(self,key):

        color=QColorDialog.getColor()

        if color.isValid():

            self.theme[key]=color.name()

    def save_theme_changes(self,dialog):

        self.theme["locked"]=True

        save_theme(
            self.theme
        )

        QMessageBox.information(
            self,
            "Theme",
            "Theme Saved Successfully"
        )

        dialog.accept()

    # ================= LOAD VALUES =================

    def load_values(self):

        self.cell_v_max.setText(
            str(CONFIG["limits"]["cell_v_max"])
        )

        self.cell_v_min.setText(
            str(CONFIG["limits"]["cell_v_min"])
        )

        self.cell_ir_max.setText(
            str(CONFIG["limits"]["cell_ir_max"])
        )

        self.cell_ir_min.setText(
            str(CONFIG["limits"]["cell_ir_min"])
        )

        self.module_v_max.setText(
            str(CONFIG["limits"]["module_v_max"])
        )

        self.module_v_min.setText(
            str(CONFIG["limits"]["module_v_min"])
        )

        self.module_ir_max.setText(
            str(CONFIG["limits"]["module_ir_max"])
        )

        self.module_ir_min.setText(
            str(CONFIG["limits"]["module_ir_min"])
        )

    # ================= BACKGROUND LOGO =================

    def paintEvent(self,event):

        super().paintEvent(event)

        if self.logo.isNull():
            return

        painter=QPainter(self)

        painter.setRenderHint(
            QPainter.SmoothPixmapTransform
        )

        painter.setOpacity(0.06)

        logo=self.logo.scaled(
            350,
            350,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        x=(self.width()-logo.width())//2
        y=(self.height()-logo.height())//2

        painter.drawPixmap(
            x,
            y,
            logo
        )