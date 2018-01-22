"""
REV 4_1
Contributors : Adel, Adrien, Morgan, Aurelien
Last modification date : 2018-01-19
REV4
Séparation fichiers

"""
from PIL import Image
import numpy as np
import resize
import fill
from variables import *


def create(images, crop_length = CROP_LENGTH, crop_width = CROP_WIDTH, ui = None):
    """
    :param images: array of the selected images 
    :return: the image
	
    Autor Adel      2017-11-25
    Modification:
    >Adel    2017-12-26 
    >Adrien  2017-12-28  
    """
    
    #Dimension of the table
    x, y = np.shape(images)    
    final = np.zeros((x*crop_width,y*crop_length,3), np.uint8)
    
    #Fail attempt of importation/process
    err = []
    
    #Import and process
    for i in range(x):
        for j in range(y):
            try:    
                img = Image.open(images[i][j])
                tab = np.array(img)
                img.close()
                tab = resize.resize(tab, (crop_length, crop_width))
                final[i*crop_width:(i+1)*crop_width , j*crop_length:(j+1)*crop_length] = tab
                if ui != None: ui.pb_avance.setValue(int((100 * (i * y + j) / (x * y) + 1)/2 + 50))
                
            except OSError:
                print("erreur de lecture sur ",images[i][j])
                err.append(images[i][j])
            
            except ValueError:
                print("erreur de valeur sur ",images[i][j], i,j)
                err.append(images[i][j])
                           
    return final, err



def create_tri(mat_images, crop = CROP, ui = None):
    """
    :param images: array of the selected images 
    :return: the image
    Autor Adrien      2018-01-11 
    """
    
    #Dimension of the table
    x, y, z = np.shape(mat_images)    
    final = np.zeros((x*crop,y*crop, 3), np.uint8)
    
    #Import and process
    for i in range(x):
        for j in range(y):    
                img_0, img_1 = Image.open(mat_images[i][j][0]), Image.open(mat_images[i][j][1])
                mat_tab = [np.array(img_0), np.array(img_1)]
                img_0.close(), img_1.close()
                tab = resize.resize_tri(mat_tab, crop, i, j)
                final[i*crop:(i+1)*crop , j*crop:(j+1)*crop] = tab
                if ui != None: ui.pb_avance.setValue(int((100 * (i * y + j) / (x * y) + 1)/2 +50))
                           
    return final



def create_los(images, crop, ui = None):
    """
    :param images: table of the selected images
    :return: the image

    Autor : Adrien   2018-01-16
    """

    #Dimension of the table
    x, y = np.shape(images)
    final = np.zeros(((x-1)*crop,(y-1)*2*crop, 3), np.uint8)
    
    #Borne for y
    borne_y = y-1

    ##Import and process

    # Squares for the odd lines
    for i in range(1,x,2): 
        for j in range(borne_y):
            img = Image.open(images[i][j])
            tab = np.array(img)
            img.close()
            
            if j==y-1:
                tab = resize.resize(tab, (crop, 2*crop))
                final[(i-1)*crop:(i+1)*crop,j*2*crop:(2*j+1)*crop] = tab
            else:
                tab = resize.resize(tab, (2*crop, 2*crop))
                final[(i-1)*crop:(i+1)*crop,j*2*crop:(j+1)*2*crop] = tab
            if ui != None: ui.pb_avance.setValue(int((100 * ((i * y + j) / (x * y) + 1)/4+50)))


    #Triangles for the even lines
    for i in range(0,x,2): 
        for j in range(y):
            img = Image.open(images[i][j])
            tab = np.array(img)
            img.close()
            
            if i==0 and j==0:
                beggining = (0,0)
            elif j == 0:
                beggining = ((i-1)*crop,0)
            elif i == 0:
                beggining = (0, (2*j-1)*crop)
            else:
                beggining = ((i-1)*crop, (2*j-1)*crop)
                
            final = fill.fill_los(final, tab, crop, beggining, i, x, j, y)
            if ui != None: ui.pb_avance.setValue(int((100 * ((i) * y + j) / (x * y) + 1)/4 + 75))

    return final



def create_hex(images, crop, ui=None):
    """
    :param images: table of the selected images
    :return: the image

    Autor : Adrien  2018-01-16
    """

    #Dimensions
    lines, columns = np.shape(images)

    #New dimensions
    x = 2*lines - 3
    y = 2*(columns-1)
    final = np.zeros((x*crop, y*crop, 3), np.uint8)

	
    #Process
    for i in range(lines):
        
        #Odd lines for entire hexagons 
        if i%2 == 1:
            borne_y = columns-1
			
        #Even lines for not only entire hexagons
        else:
            borne_y = columns
            
        for j in range(borne_y):
            img = Image.open(images[i][j])
            tab = np.array(img)
            img.close()

            #Beggining index depend on lines and columns
            if i==0 and j==0:
                beggining = (0,0)
            elif i == 0:
                beggining = (0, (2*j-1)*crop)
            elif i%2 == 1:
                beggining = (2*(i-1)*crop,2*j*crop)
            else:
                if j == 0:
                    beggining = (2*(i-1)*crop, 0)
                else:
                    beggining = (2*(i-1)*crop, (2*j-1)*crop)
            
            final = fill.fill_hex(final, tab, crop, beggining, i, lines, j, columns)
            if ui != None:ui.pb_avance.setValue(int((100 * (i * columns + j) / (lines * columns) + 1)/2 + 50))

    return final
