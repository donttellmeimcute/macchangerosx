import re
import os
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QComboBox, QVBoxLayout, QWidget, QMessageBox, QInputDialog
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.mac_input = QLineEdit()
        self.execute_button = QPushButton('Execute')
        self.save_button = QPushButton('Save')
        self.mac_list = QComboBox()

        self.execute_button.clicked.connect(self.execute_command)
        self.save_button.clicked.connect(self.save_mac)
        self.mac_list.currentIndexChanged.connect(self.select_mac)

        self.mac_input.textChanged.connect(self.format_mac_input)

        layout = QVBoxLayout()
        layout.addWidget(self.mac_input)
        layout.addWidget(self.execute_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.mac_list)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_mac_addresses()  # Load addresses at the start

    def format_mac_input(self):
        mac = self.mac_input.text()
        mac = re.sub('[^0-9a-fA-F]', '', mac)  # Remove non-hex characters
        mac = ':'.join(mac[i:i+2] for i in range(0, len(mac), 2))  # Add colons every 2 characters
        mac = mac[:17]  # Limit to 12 characters for MAC address and 5 colons
        self.mac_input.setText(mac.upper())  # Convert to uppercase and update the input field

    def execute_command(self):
        mac = self.mac_input.text()
        password, ok = QInputDialog.getText(self, "Root Password", "Enter root password:", QLineEdit.EchoMode.Password)
        if ok:
            command = f'echo {password} | sudo -S ifconfig en0 ether {mac}'  # Use sudo -S to pass the password
            subprocess.run(command, shell=True)
            
            # Alert the user that MAC address has been changed
            QMessageBox.information(self, "MAC Address Changed", "MAC address has been changed successfully.")
            QMessageBox.information(self, "MAC Address Changed", "Please reconnect to the network for the changes to take effect.")
            
            # Execute ifconfig to see the new MAC address
            subprocess.run("ifconfig", shell=True)

    def save_mac(self):
        mac = self.mac_input.text()
        with open('mac_addresses.txt', 'a') as f:
            f.write(mac + '\n')
        self.mac_list.addItem(mac)

    def select_mac(self, index):
        mac = self.mac_list.itemText(index)
        self.mac_input.setText(mac)

    def load_mac_addresses(self):
        if os.path.exists('mac_addresses.txt'):
            with open('mac_addresses.txt', 'r') as f:
                addresses = f.read().splitlines()
                self.mac_list.addItems(addresses)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
