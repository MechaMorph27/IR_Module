from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class Splash(QWidget):
    finished = Signal()

    def __init__(self):
        super().__init__()

        # ================= WINDOW SIZE (SMALLER) =================
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(780, 420)

        self.progress_value = 0
        self.shine_pos = -200

        # ================= FADE IN =================
        self.setWindowOpacity(0)

        self.fade = QPropertyAnimation(self, b"windowOpacity")
        self.fade.setDuration(1200)
        self.fade.setStartValue(0)
        self.fade.setEndValue(1)
        self.fade.start()

        # ================= STYLE =================
        self.setStyleSheet("""
            QWidget{
                background-color:#0b0b0b;
            }

            QProgressBar{
                border:none;
                background-color:#1c1c1c;
                height:8px;
                border-radius:4px;
            }

            QProgressBar::chunk{
                border-radius:4px;
                background:qlineargradient(
                    x1:0, y1:0,
                    x2:1, y2:0,
                    stop:0 #0066ff,
                    stop:0.5 #33a1ff,
                    stop:1 #0066ff
                );
            }
        """)

        # ================= LAYOUT =================
        main = QVBoxLayout(self)
        main.setContentsMargins(30, 30, 30, 20)

        main.addStretch()

        # ================= LOGO =================
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignCenter)

        self.logo = QPixmap("logo1.png")

        self.logo = self.logo.scaled(
            620, 290,   # 🔥 INCREASED LOGO SIZE
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.logo_label.setPixmap(self.logo)

        main.addWidget(self.logo_label)

        main.addStretch()

        # ================= LOADING BAR =================
        bottom = QHBoxLayout()

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setTextVisible(False)  # remove internal %

        self.percent = QLabel("0%")
        self.percent.setFixedWidth(55)
        self.percent.setAlignment(Qt.AlignCenter)

        self.percent.setStyleSheet("""
            color:white;
            font-size:15px;
            font-weight:bold;
        """)

        bottom.addWidget(self.progress)
        bottom.addWidget(self.percent)

        main.addLayout(bottom)

        # ================= TIMER =================
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_loading)
        self.timer.start(15)

    # ================= LOADING UPDATE =================
    def update_loading(self):

        if self.progress_value < 100:

            self.progress_value += 1

            self.progress.setValue(self.progress_value)
            self.percent.setText(f"{self.progress_value}%")

            # shine movement
            self.shine_pos += 5

            if self.shine_pos > self.width() + 200:
                self.shine_pos = -200

            self.update()

        else:
            self.timer.stop()
            self.finished.emit()
            self.close()

    # ================= SHINE EFFECT =================
    def paintEvent(self, event):

        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        logo_rect = self.logo_label.geometry()

        gradient = QLinearGradient(
            self.shine_pos,
            logo_rect.top(),
            self.shine_pos + 120,
            logo_rect.top()
        )

        gradient.setColorAt(0.0, QColor(255, 255, 255, 0))
        gradient.setColorAt(0.5, QColor(255, 255, 255, 220))
        gradient.setColorAt(1.0, QColor(255, 255, 255, 0))

        painter.setClipRect(logo_rect)
        painter.fillRect(logo_rect, gradient)