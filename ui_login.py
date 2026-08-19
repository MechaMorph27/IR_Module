from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from ui_dashboard import Dashboard
from security_manager import get_password, save_password

# ✔ NEW IMPORT
from operator_store import load_operators, add_operator


class Login(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Battery Tester System")
        self.setWindowIcon(QIcon("logo1.png"))
        self.setFixedSize(420, 280)

        self.setStyleSheet("background-color:#0f1115;")

        # ================= OPERATORS (UPDATED) =================
        self.operators = load_operators()   # ✔ CHANGED HERE

        # ================= BACKGROUND =================
        self.bg_logo = QLabel(self)

        pixmap = QPixmap("logo1.png").scaled(
            260, 260,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.bg_logo.setPixmap(pixmap)
        self.bg_logo.setAlignment(Qt.AlignCenter)
        self.bg_logo.setAttribute(Qt.WA_TransparentForMouseEvents)

        # ================= CARD =================
        self.card = QFrame(self)
        self.card.setFixedSize(370, 220)

        self.card.setStyleSheet("""
            QFrame {
                background-color: rgba(20,22,30,200);
                border-radius:12px;
                border:1px solid rgba(51,161,255,80);
            }
        """)

        label_style = """
            font-size:16px;
            font-weight:bold;
            color:#33a1ff;
        """

        combo_style = """
            QComboBox {
                background-color:#1c1f26;
                color:white;
                border:1px solid #333;
                padding:5px;
                border-radius:4px;
            }

            QComboBox QAbstractItemView {
                background-color:#1c1f26;
                color:white;
                selection-background-color:#2d6cdf;
            }
        """

        # ================= OPERATOR =================
        op_row = QHBoxLayout()

        op_label = QLabel("Operator:")
        op_label.setFixedWidth(90)
        op_label.setStyleSheet(label_style)

        self.name = QComboBox()
        self.name.addItems(self.operators)   # ✔ UPDATED
        self.name.setStyleSheet(combo_style)

        self.add_btn = QPushButton("+")
        self.add_btn.setFixedSize(40, 35)
        self.add_btn.clicked.connect(self.open_admin_password_box)

        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color:#2d6cdf;
                color:white;
                font-size:18px;
                font-weight:bold;
                border-radius:5px;
            }
            QPushButton:hover {
                background-color:#3b82f6;
            }
        """)

        op_row.addWidget(op_label)
        op_row.addWidget(self.name)
        op_row.addWidget(self.add_btn)

        # ================= SHIFT =================
        shift_row = QHBoxLayout()

        shift_label = QLabel("Shift:")
        shift_label.setFixedWidth(90)
        shift_label.setStyleSheet(label_style)

        self.shift = QComboBox()
        self.shift.addItems(["A", "B"])
        self.shift.setStyleSheet(combo_style)

        shift_row.addWidget(shift_label)
        shift_row.addWidget(self.shift)

        # ================= START =================
        self.btn = QPushButton("START")
        self.btn.setFixedWidth(140)
        self.btn.clicked.connect(self.go)

        self.btn.setStyleSheet("""
            QPushButton {
                background-color:#2d6cdf;
                color:white;
                font-weight:bold;
                padding:8px;
                border-radius:6px;
            }
            QPushButton:hover {
                background-color:#3b82f6;
            }
        """)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(20, 20, 20, 20)

        card_layout.addLayout(op_row)
        card_layout.addSpacing(15)
        card_layout.addLayout(shift_row)
        card_layout.addSpacing(25)
        card_layout.addWidget(self.btn, alignment=Qt.AlignCenter)

    # ==================================================
    # ADMIN AUTH BOX (UNCHANGED)
    # ==================================================
    def open_admin_password_box(self):

        dialog = QDialog(self)
        dialog.setWindowTitle("Admin Authentication")
        dialog.setFixedSize(380, 240)

        layout = QVBoxLayout(dialog)

        title = QLabel("ADMIN AUTHENTICATION")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:20px;font-weight:bold;color:#33a1ff;")

        password = QLineEdit()
        password.setEchoMode(QLineEdit.Password)
        password.setPlaceholderText("Enter Admin Password")

        btn_ok = QPushButton("OK")
        btn_change = QPushButton("Change Password")
        btn_cancel = QPushButton("Cancel")

        def check():
            return password.text() == get_password()

        def on_ok():
            if check():
                dialog.accept()
                self.open_add_operator_box()
            else:
                QMessageBox.critical(dialog, "Error", "Wrong Password")

        def on_change():
            if not check():
                QMessageBox.critical(dialog, "Error", "Wrong Password")
                return
            dialog.accept()
            self.open_change_password_box()

        btn_ok.clicked.connect(on_ok)
        btn_change.clicked.connect(on_change)
        btn_cancel.clicked.connect(dialog.reject)

        layout.addWidget(title)
        layout.addWidget(password)
        layout.addWidget(btn_ok)
        layout.addWidget(btn_change)
        layout.addWidget(btn_cancel)

        dialog.exec()

    # ==================================================
    # ADD OPERATOR (UPDATED → SAVE TO FILE)
    # ==================================================
    def open_add_operator_box(self):

        name, ok = QInputDialog.getText(
            self,
            "Add Operator",
            "Enter Operator Name:"
        )

        if not ok:
            return

        name = name.strip()

        if not name:
            return

        # ✔ SAVE OPERATOR PERMANENTLY
        add_operator(name)

        # refresh combo
        self.name.clear()
        self.name.addItems(load_operators())
        self.name.setCurrentText(name)

    # ==================================================
    # CHANGE PASSWORD (UNCHANGED)
    # ==================================================
    def open_change_password_box(self):

        dialog = QDialog(self)
        dialog.setWindowTitle("Change Password")
        dialog.setFixedSize(360, 220)

        layout = QVBoxLayout(dialog)

        current = QLineEdit()
        current.setEchoMode(QLineEdit.Password)
        current.setPlaceholderText("Current Password")

        new_pass = QLineEdit()
        new_pass.setEchoMode(QLineEdit.Password)
        new_pass.setPlaceholderText("New Password")

        confirm = QLineEdit()
        confirm.setEchoMode(QLineEdit.Password)
        confirm.setPlaceholderText("Re-enter Password")

        btn_save = QPushButton("Save")
        btn_cancel = QPushButton("Cancel")

        def save():
            if current.text() != get_password():
                QMessageBox.critical(dialog, "Error", "Wrong Current Password")
                return

            if new_pass.text() != confirm.text():
                QMessageBox.warning(dialog, "Error", "Passwords do not match")
                return

            save_password(new_pass.text())
            QMessageBox.information(dialog, "Success", "Password Changed Successfully")
            dialog.accept()

        btn_save.clicked.connect(save)
        btn_cancel.clicked.connect(dialog.reject)

        layout.addWidget(current)
        layout.addWidget(new_pass)
        layout.addWidget(confirm)
        layout.addWidget(btn_save)
        layout.addWidget(btn_cancel)

        dialog.exec()

    # ==================================================
    # START
    # ==================================================
    def go(self):

        op = self.name.currentText().strip()

        if not op:
            QMessageBox.warning(self, "Error", "Select operator")
            return

        # ✔ AUTO SAVE EVEN ON START
        add_operator(op)

        self.w = Dashboard(op, self.shift.currentText())
        self.w.show()
        self.close()

    # ================= CENTER =================
    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.bg_logo.resize(self.size())

        if self.bg_logo.pixmap():
            self.bg_logo.move(
                (self.width() - self.bg_logo.pixmap().width()) // 2,
                (self.height() - self.bg_logo.pixmap().height()) // 2
            )

        self.card.move(
            (self.width() - self.card.width()) // 2,
            (self.height() - self.card.height()) // 2
        )