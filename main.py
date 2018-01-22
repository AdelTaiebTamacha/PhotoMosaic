##############################################################################
########                           PREPROCESSEUR
###############################################################################


from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets

import sys
from PIL import Image
from PIL.ImageQt import ImageQt

import pipe
import interface
import database
from variables import *

###############################################################################
########                           FENETRE
###############################################################################

class MainWindow(QtWidgets.QMainWindow):
    """
    Qt Window Creation
    """
    
    def __init__(self, QWidget_parent=None):
        super(MainWindow, self).__init__(QWidget_parent)
        
        # Create and attach the Qt Designer component to this widget
        self.ui = interface.Ui_MainWindow()
        self.ui.setupUi(self)
        
        #       SIGNALS AND SLOTS
        #Button
        self.ui.bt_ouvrir.clicked.connect(self.loadImage)
        self.ui.bt_lancer.clicked.connect(self.start)
        self.ui.bt_charger.clicked.connect(self.loadBase)
        
        #Slider
        self.ui.hsld_subdiv_hori.valueChanged['int'].connect(self.changeCrop_hori)
        self.ui.sb_subdiv_hori.valueChanged['int'].connect(self.changeCrop_hori)
        self.ui.hsld_subdiv_verti.valueChanged['int'].connect(self.changeCrop_verti)
        self.ui.sb_subdiv_verti.valueChanged['int'].connect(self.changeCrop_verti)
        
        #Radio Button
        self.ui.rb_rect.toggled.connect(self.changeMode_Rect)
        self.ui.rb_tri.toggled.connect(self.changeMode_Tri)
        self.ui.rb_los.toggled.connect(self.changeMode_Los)
        self.ui.rb_hex.toggled.connect(self.changeMode_Hex)
        
        #Menu
        self.ui.actionOuvrir_Image.triggered.connect(self.loadImage)
        self.ui.actionEnregistrer.triggered.connect(self.saveImage)
        self.ui.actionEnregistrer_sous.triggered.connect(self.saveAsImage)
        self.ui.actionSelectionner_images.triggered.connect(self.loadBase)
        self.ui.actionLancer.triggered.connect(self.start)
                                            
        #Local variables
        self.image = None
        self.imagePath = ""
        self.mosa = None
        self.crop_hori = 10
        self.crop_verti = 10
        self.selector = 0
        self.save_path = ""
        
        
    def changeMode_Rect(self, event):
        self.selector = RECT
        self.ui.frame_verti.setEnabled(True)
        
    def changeMode_Tri(self, event):
        self.selector = TRI
        self.ui.frame_verti.setEnabled(False)
        
    def changeMode_Los(self, event):
        self.selector = LOS
        self.ui.frame_verti.setEnabled(False)
        
    def changeMode_Hex(self, event):
        self.selector = HEX
        self.ui.frame_verti.setEnabled(False)
        
    def loadImage(self,event):
        """
        :param event: rising event
        
        Autor : Adel    2018-01-02
        Modification :
        
        """
        
        self.ui.pb_avance.setValue(100)
        
        #Open dialog to select image
        fileName = QtWidgets.QFileDialog.getOpenFileName(
                        self,
                        "Ouvrir un fichier d'image",
                        #"C:/Users/Dieu/Documents/Python/WinPython-64bit-3.6.3.0Qt5/mine/DATA", 
                        QtCore.QDir.homePath(),
                        "Fichiers d'image (*.jpg *.jpeg *.gif *.png)"
                    )
        
        #Change the displayed image and change the path
        if fileName:
            
            #Set the new image
            self.imagePath = fileName[0]
            self.image = Image.open(self.imagePath)
            
            #Set the default value of crop
            width, height = self.image.size
            self.ui.hsld_subdiv_hori.setValue(width//100)
            self.ui.hsld_subdiv_verti.setValue(height//100)
            
            #Create Qt image with the right dimensions
            pixmap = QtGui.QPixmap(fileName[0])
            pixmap = pixmap.scaled(380, 220, QtCore.Qt.KeepAspectRatio)
            
            #Display the image            
            self.ui.lbl_image.setPixmap(pixmap)
        
        self.ui.pb_avance.setValue(0)


    def loadBase(self,event):
        """
        :param event: rising event
        Load the file of the database
                
        Autor : Adel    2018-01-02
        Modification :
        > 
        """
        
        #Open dialog to select images
        dirName = QtWidgets.QFileDialog.getExistingDirectory(
                        self,
                        "Selectionner le dossier image",
                        QtCore.QDir.homePath(),
                    )
        
        #Change the displayed image and change the path
        if dirName:
            print(dirName[0])
            database.update_data_base(database.D_DATA_FILE, dirName, self.ui)


			
    def saveImage(self, event):
        """
        :param event: rising event
        Save the mosaic
        
        Autor : Adel    2018-01-02
        Modification :
        > 
        """
        self.mosa.save(self.save_path+"mosa.jpg")
        
        
        
    def saveAsImage(self, event):
        """
        :param event: rising event
        Save the mosaic with an other name/location    
        
        Autor : Adel    2018-01-02
        Modification :
        > 
        """
           
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "", "All Files (*)")
        if fileName:
            #print(fileName)
            self.mosa.save(fileName)
        self.save_path = fileName


		
    def start(self, event):
        """
        :param event: rising event
        Base sur le main de MosaicREV3_1
        
        Autor : Adel    2018-01-02
        Modification :
        > 
        """

        #   GET THE MOSAIC
        if self.selector == RECT : self.mosa = pipe.photomosaic(self.image, self.crop_hori, self.crop_verti, self.ui)
        elif self.selector == TRI : self.mosa = pipe.photomosaic_tri(self.image, self.crop_hori, self.ui)
        elif self.selector == LOS : self.mosa = pipe.photomosaic_los(self.image, self.crop_hori, self.ui)
        elif self.selector == HEX : self.mosa = pipe.photomosaic_hex(self.image, self.crop_hori, self.ui)

        #   CONVERT TO Qt IMAGE AND UPDATE VIEW
        qt_im = ImageQt(self.mosa)
        pixmap = QtGui.QPixmap.fromImage(qt_im)
        self.ui.lbl_mosaic.setPixmap(pixmap)
		
		
		#	SAVE IMAGE
        self.mosa.save(self.save_path+"mosa_temp.jpg")
		
        
    
    def changeCrop_hori(self, event):
        """
        :param event: rising event
        Update crop value
        
        Autor : Adel    2018-01-02
        Modification :
        > 
        """
        self.crop_hori = event

    def changeCrop_verti(self, event):
        """
        :param event: rising event
        Update crop value
        
        Autor : Adel    2018-01-02
        Modification :
        > 
        """
        self.crop_verti = event


if __name__ == "__main__":
   
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
    
    
