"""
REV 4_1
Contributors : Adel, Adrien, Morgan, Aurelien
Last modification date : 2018-01-19
REV4
Séparation fichiers

"""
import numpy as np
import database as db
import selecter
from variables import *


def get_images(tab, entier = False, ui = None):
    """
    :param tab: table of the pixel to search for
    :return: list of the selected images
    Autor Adel      2017-11-25
    
    Modification:
    > Adrien	2018-01-16
    """
  
    #Get the images data
    data = db.get_image_base("DATA.txt")
        
    #Dimension of the table
    x, y, z = np.shape(tab)
    
    #Array holding the selected images
    images = [ [0 for j in range(y)] for i in range(x)]
    
    
    #Find the image for each pixels
    for i in range(x):

        #If all lines have the same number of images
        if entier and i%2 == 1:
            borne_y = y-1
        else:
            borne_y = y
        
        for j in range(borne_y):
            images[i][j] = selecter.select_color_image(tab[i,j],data)
            if ui != None: ui.pb_avance.setValue(int((100*(i*y+j)/(x*y)+1)/2))
            
    return images



def get_images_tri(tab, ui = None):
    """
    :param tab: table of the pixel to search for
    :return: list of the selected images
	
    Autor Adrien      2018-01-11
    """
  
    #Get the images data
    data = db.get_image_base("DATA.txt")
        
    #Dimension of the table
    x, y, z, w = np.shape(tab)
    
    #Array holding the selected images
    mat_images = [ [[0 for k in range(2)] for j in range(y)] for i in range(x)]
    
    
    #Find the image for each pixels
    for i in range(x):
        for j in range(y):
            for k in range(TRIANGLE_DIMENSION):              
                mat_images[i][j][k] = selecter.select_color_image(tab[i,j,k],data)
				
                if ui != None: ui.pb_avance.setValue(int((100*(i*y+j)/(x*y)+1)/2))
                
    return mat_images
   
