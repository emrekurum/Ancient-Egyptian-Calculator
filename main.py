import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QVBoxLayout, QMessageBox, QLabel # type: ignore
from PyQt5.QtGui import QIcon, QFont, QPixmap # type: ignore
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QPoint, QTimer, QDateTime # type: ignore
import pygame  # pygame ile müzik çalma

class Calculator(QWidget):
    def __init__(self):
        super().__init__()

        # Gündüz ve Gece modu için iki arka plan resmi
        self.day_background = QPixmap("day_background.jpg")  # Gündüz teması
        self.night_background = QPixmap("night_background.jpg")  # Gece teması

        # Arka plan için QLabel
        self.background_label = QLabel(self)
        self.background_label.setScaledContents(True)

        # Giriş-Çıkış ve diğer bileşenleri başlat
        self.initUI()
        self.playDayMusic()  # Gündüz müzigini başlat

        # Gizli kombinasyon için tuş geçmişi
        self.key_history = []

        # Bilgisayar saatine göre gece veya gündüz modunu ayarla
        current_hour = QDateTime.currentDateTime().time().hour()
        if 6 <= current_hour < 18:
            self.setDayBackground()
        else:
            self.setNightBackground()
            self.playNightMusic()

    def initUI(self):
        # Pencere başlığı
        self.setWindowTitle("Antik Mısır Temalı Hesap Makinesi")
        self.setGeometry(100, 100, 800, 600)  # Pencere boyutunu genişlet

        # Ekran (Line Edit)
        layout = QVBoxLayout(self)
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setPlaceholderText("0")
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFont(QFont("Courier", 16))
        self.display.setStyleSheet("background-color: rgba(255, 255, 255, 200); padding: 10px;")
        layout.addWidget(self.display)

        # Animasyon Simgesi
        self.animated_icon = QLabel(self)
        self.animated_icon.setPixmap(QPixmap("icon_0.png").scaled(50, 50))
        self.animated_icon.setVisible(False)
        layout.addWidget(self.animated_icon)

        # İkon dosya adları ve buton değerleri
        button_icons = [
            ('icon_0.png', '7'), ('icon_1.png', '8'), ('icon_2.png', '9'), ('icon_3.png', '/'),
            ('icon_4.png', '4'), ('icon_5.png', '5'), ('icon_6.png', '6'), ('icon_7.png', '*'),
            ('icon_8.png', '1'), ('icon_9.png', '2'), ('icon_10.png', '3'), ('icon_11.png', '-'),
            ('icon_12.png', '0'), ('icon_13.png', 'C'), ('icon_14.png', '='), ('icon_15.png', '+')
        ]

        # Grid layout for buttons
        buttonsLayout = QGridLayout()
        row, col = 0, 0
        for icon_file, button_value in button_icons:
            button = QPushButton()
            button.setIcon(QIcon(icon_file))
            button.setIconSize(QSize(50, 50))
            button.clicked.connect(lambda _, val=button_value: self.onButtonClick(val))
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(210, 180, 140, 180);
                    border: 1px solid #8B4513;
                    border-radius: 15px;
                    padding: 10px;
                    font-size: 18px;
                    font-weight: bold;
                    color: #8B4513;
                }
                QPushButton:hover {
                    background-color: rgba(222, 184, 135, 200);
                    border: 2px solid #A0522D;
                }
            """)
            buttonsLayout.addWidget(button, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        layout.addLayout(buttonsLayout)
        self.setLayout(layout)

    def playDayMusic(self):
        # pygame ile gündüz müzigini başlat
        pygame.mixer.init()
        pygame.mixer.music.load("day_music.mp3")  # Gündüz müzigi dosyanızın adı burada yer almalı
        pygame.mixer.music.play(-1)  # -1 döngü anlamına gelir, müzik sonsuz döngüde çalar

    def playNightMusic(self):
        # pygame ile gece müzigini başlat
        pygame.mixer.music.load("night_music.mp3")  # Gece müzigi dosyanızın adı burada yer almalı
        pygame.mixer.music.play(-1)  # -1 döngü anlamına gelir, müzik sonsuz döngüde çalar

    def setDayBackground(self):
        # Gündüz arka planını ayarla
        self.background_label.setPixmap(self.day_background)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.background_label.lower()

    def setNightBackground(self):
        # Gece arka planını ayarla
        self.background_label.setPixmap(self.night_background)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.background_label.lower()

    def resizeEvent(self, event):
        # Pencere boyutu değiştiğinde arka planı yeniden ayarla
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    def switchToNightMode(self):
        # Gece moduna geçiş
        self.setNightBackground()  # Gece arka planı
        self.playNightMusic()  # Gece müzigi

    def onButtonClick(self, value):
        if value == 'C':
            self.display.clear()
            self.key_history.clear()
        elif value == '=':
            try:
                result = eval(self.display.text())
                self.display.setText(str(result))
                self.showAnimation()
            except:
                self.display.setText("Error")
        else:
            self.display.setText(self.display.text() + value)
            self.key_history.append(value)
            self.checkSecretCombination()

    def showAnimation(self):
        self.animated_icon.setVisible(True)
        self.animated_icon.move(175, 175)

        self.animation = QPropertyAnimation(self.animated_icon, b"pos")
        self.animation.setDuration(1500)
        self.animation.setStartValue(QPoint(175, 175))
        self.animation.setEndValue(QPoint(175, 50))
        self.animation.start()
        self.animation.finished.connect(lambda: self.animated_icon.setVisible(False))

    def checkSecretCombination(self):
        secret_combination = ['7', '3', '1']
        if self.key_history[-3:] == secret_combination:
            self.showSecretMessage()

    def showSecretMessage(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Gizli Bilgi: Eski Mısır'da piramitler gökyüzü ile yeryüzünü bağlayan bir simgeydi.")
        msg.setWindowTitle("Gizli Mısır Mesajı")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

def main():
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
