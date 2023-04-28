import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QInputDialog, QFileDialog
from PyQt5.QtCore import Qt, QProcess

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Creazione del layout principale
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        gridLayout = QGridLayout(centralWidget)

        # Aggiunta della label per visualizzare la lista dei dispositivi adb
        self.devicesLabel = QLabel("Dispositivi adb:")
        gridLayout.addWidget(self.devicesLabel, 0, 0)

        # Aggiunta del pulsante per eseguire il comando adb devices
        self.refreshButton = QPushButton("Aggiorna lista")
        self.refreshButton.clicked.connect(self.refreshDevicesList)
        gridLayout.addWidget(self.refreshButton, 1, 0)

        # Aggiunta del pulsante per creare una cartella
        self.createFolderButton = QPushButton("Crea cartella")
        self.createFolderButton.clicked.connect(self.createFolder)
        gridLayout.addWidget(self.createFolderButton, 2, 0)

        # Aggiunta del pulsante per scegliere un file apk
        self.fileButton = QPushButton("File")
        self.fileButton.clicked.connect(self.chooseFile)
        gridLayout.addWidget(self.fileButton, 3, 0)

        # Aggiunta del pulsante per installare il file apk
        self.installButton = QPushButton("Installa")
        self.installButton.clicked.connect(self.installFile)
        gridLayout.addWidget(self.installButton, 4, 0)

        # Aggiunta del pulsante per copiare il file apk sulla sdcard
        self.pushButton = QPushButton("Copia su sdcard")
        self.pushButton.clicked.connect(self.pushFile)
        gridLayout.addWidget(self.pushButton, 5, 0)

        # Esecuzione del comando adb devices all'avvio del programma
        self.refreshDevicesList()

    def refreshDevicesList(self):
        # Esecuzione del comando adb devices con QProcess
        adbProcess = QProcess()
        adbProcess.start("adb devices")
        adbProcess.waitForFinished(-1)

        # Lettura dell'output del comando adb devices
        output = adbProcess.readAllStandardOutput().data().decode()

        # Aggiornamento della label con la lista dei dispositivi adb
        self.devicesLabel.setText("Dispositivi adb:\n" + output)

    def createFolder(self):
        # Creazione di una finestra di dialogo per chiedere il nome della cartella
        folderName, okPressed = QInputDialog.getText(self, "Crea cartella", "Nome della cartella:", QLineEdit.Normal, "")
        if okPressed and folderName != "":
            # Creazione della cartella con il nome inserito dall'utente
            try:
                os.mkdir(folderName)
                QMessageBox.information(self, "Cartella creata", f"La cartella {folderName} è stata creata con successo.")
            except OSError:
                QMessageBox.warning(self, "Errore", f"Non è stato possibile creare la cartella {folderName}.")

    def chooseFile(self):
        # Apertura della finestra di dialogo per scegliere un file apk
        fileName, _ = QFileDialog.getOpenFileName(self, "Scegli file APK", "", "APK Files (*.apk)")
        if fileName:
            self.filePath = fileName
            QMessageBox.information(self, "File selezionato", f"Il file {fileName} è stato selezionato.")

    def installFile(self):
        # Esecuzione del comando adb install con il percorso del file apk selezionato
        adbProcess = QProcess()
        adbProcess.start(f"adb install {self.filePath}")
        adbProcess.waitForFinished(-1)

        # Lettura dell'output del comando adb install
        output = adbProcess.readAllStandardOutput().data().decode()

        # Visualizzazione del messaggio di successo o errore
        if "Success" in output:
            QMessageBox.information(self, "File installato", "Il file è stato installato con successo.")
        else:
            QMessageBox.warning(self, "Errore", "Non è stato possibile installare il file.")

    def pushFile(self):
        # Esecuzione del comando adb push con il percorso del file apk selezionato e la posizione sulla sdcard
        adbProcess = QProcess()
        adbProcess.start(f"adb push {self.filePath} /sdcard")
        adbProcess.waitForFinished(-1)

        # Lettura dell'output del comando adb push
        output = adbProcess.readAllStandardOutput().data().decode()

        # Visualizzazione del messaggio di successo o errore
        if "KB/s" in output:
            QMessageBox.information(self, "File copiato", "Il file è stato copiato sulla sdcard con successo.")
        else:
            QMessageBox.warning(self, "Errore", "Non è stato possibile copiare il file sulla sdcard.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())