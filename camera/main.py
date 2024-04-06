import sys
from custome_errors import *
sys.excepthook = my_excepthook
from PyQt6.QtMultimedia import QCamera,QImageCapture,QMediaCaptureSession,QMediaRecorder,QAudioInput,QMediaFormat
from PyQt6.QtMultimediaWidgets import QVideoWidget
import update
import gui
import guiTools
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
language.init_translation()
class main (qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(app.name + _("version : ") + str(app.version))
        layout=qt.QVBoxLayout()
        self.camera=QCamera()
        self.camera.start()
        self.video=QVideoWidget()
        self.media=QMediaCaptureSession()
        self.audio=QAudioInput(self)
        self.media.setAudioInput(self.audio)
        self.media.setCamera(self.camera)
        self.media.setVideoOutput(self.video)
        layout.addWidget(self.video)
        self.photo=QImageCapture(self)
        self.media.setImageCapture(self.photo)
        self.recorder=QMediaRecorder()
        self.format=QMediaFormat()
        self.format.setAudioCodec(self.format.AudioCodec.MP3)
        self.recorder.setMediaFormat(self.format)
        self.media.setRecorder(self.recorder)
        self.setting=qt.QPushButton(_("settings"))
        self.setting.setDefault(True)
        self.setting.clicked.connect(lambda: settings(self).exec())
        layout.addWidget(self.setting)
        w=qt.QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)

        mb=self.menuBar()
        self.path=None
        folder=qt1.QAction(_("select folder"),self)
        mb.addAction(folder)
        folder.triggered.connect(self.on_select)
        takePhoto=qt1.QAction(_("take photo"),self)
        mb.addAction(takePhoto)
        takePhoto.triggered.connect(lambda:self.photo.captureToFile(self.path))
        video=mb.addMenu(_("video recorder"))
        self.record=qt1.QAction(_("record"),self)
        video.addAction(self.record)
        self.record.triggered.connect(self.on_record)
        self.pause=qt1.QAction(_("pause"),self)
        video.addAction(self.pause)
        self.pause.setDisabled(True)
        self.pause.triggered.connect(self.on_pause)
        self.stop=qt1.QAction(_("stop"),self)
        video.addAction(self.stop)
        self.stop.setDisabled(True)
        self.stop.triggered.connect(self.on_stop)
        help=mb.addMenu(_("help"))
        helpFile=qt1.QAction(_("help file"),self)
        help.addAction(helpFile)
        helpFile.triggered.connect(lambda:guiTools.HelpFile())
        helpFile.setShortcut("f1")
        cus=help.addMenu(_("contact us"))
        telegram=qt1.QAction("telegram",self)
        cus.addAction(telegram)
        telegram.triggered.connect(lambda:guiTools.OpenLink(self,"https://t.me/mesteranasm"))
        telegramc=qt1.QAction(_("telegram channel"),self)
        cus.addAction(telegramc)
        telegramc.triggered.connect(lambda:guiTools.OpenLink(self,"https://t.me/tprogrammers"))
        githup=qt1.QAction(_("Github"),self)
        cus.addAction(githup)
        githup.triggered.connect(lambda: guiTools.OpenLink(self,"https://Github.com/mesteranas"))
        X=qt1.QAction(_("x"),self)
        cus.addAction(X)
        X.triggered.connect(lambda:guiTools.OpenLink(self,"https://x.com/mesteranasm"))
        email=qt1.QAction(_("email"),self)
        cus.addAction(email)
        email.triggered.connect(lambda: guiTools.sendEmail("anasformohammed@gmail.com","project_type=GUI app={} version={}".format(app.name,app.version),""))
        Github_project=qt1.QAction(_("visite project on Github"),self)
        help.addAction(Github_project)
        Github_project.triggered.connect(lambda:guiTools.OpenLink(self,"https://Github.com/mesteranas/{}".format(settings_handler.appName)))
        Checkupdate=qt1.QAction(_("check for update"),self)
        help.addAction(Checkupdate)
        Checkupdate.triggered.connect(lambda:update.check(self))
        licence=qt1.QAction(_("license"),self)
        help.addAction(licence)
        licence.triggered.connect(lambda: Licence(self))
        donate=qt1.QAction(_("donate"),self)
        help.addAction(donate)
        donate.triggered.connect(lambda:guiTools.OpenLink(self,"https://www.paypal.me/AMohammed231"))
        about=qt1.QAction(_("about"),self)
        help.addAction(about)
        about.triggered.connect(lambda:qt.QMessageBox.information(self,_("about"),_("{} version: {} description: {} developer: {}").format(app.name,str(app.version),app.description,app.creater)))
        self.setMenuBar(mb)
        if settings_handler.get("update","autoCheck")=="True":
            update.check(self,message=False)
    def closeEvent(self, event):
        self.camera.stop()
        if settings_handler.get("g","exitDialog")=="True":
            m=guiTools.ExitApp(self)
            m.exec()
            if m:
                event.ignore()
        else:
            self.close()
    def on_select(self):
        file=qt.QFileDialog(self)
        file.setFileMode(file.FileMode.Directory)
        if file.exec()==file.DialogCode.Accepted:
            self.path=file.selectedFiles()[0]
    def on_record(self):
        self.recorder.setOutputLocation(qt2.QUrl.fromLocalFile(self.path))
        self.recorder.record()
        self.record.setDisabled(True)
        self.stop.setDisabled(False)
        self.pause.setDisabled(False)
    def on_stop(self):
        self.recorder.stop()
        self.record.setDisabled(False)
        self.stop.setDisabled(True)
        self.pause.setDisabled(True)
    def on_pause(self):
        self.recorder.pause()
        self.pause.setDisabled(True)
        self.record.setDisabled(False)

App=qt.QApplication([])
w=main()
w.show()
App.setStyle('fusion')
App.exec()