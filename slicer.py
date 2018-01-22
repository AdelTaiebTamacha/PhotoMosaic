"""
REV 4_1
Contributors : Adel, Adrien, Morgan, Aurelien
Last modification date : 2018-01-19
REV4
Séparation fichiers

"""
import numpy as np
import reduction
import fill
from variables import *

#Default values
NOT_SHOW = False


def damier(tab, crop_length = CROP_LENGTH, crop_width = CROP_WIDTH):
    """
    :param tab: table to subdivise
    :param crop: crop factor, how many pixel are in a subdivision
    :return: the subdivised table
    
    Autor : Adrien  2017-11-23
    Modification :
    > Adel      2017-11-24  Ajout des logs
    > Adel      2017-11-25  Modification des fonctions pour prendre en compte la bonne instanciation de get_sub_tab()
    > Adel      2017-12-25  Modification du return : tableau du damier, tableau des echantillons damier
    > Adrien    2017-12-28  Différentitaion crops longueur et largeur
    > Adrien    2017-12-28  Logique : Supression du return : on prend une tableau et on renvoie un tableau damier
    """

    #Create an empty subtable with the previous dimension
    tab_sub = reduction.get_sub_tab(tab,crop_length, crop_width)

    #Dimension of the table
    x, y, z = np.shape(tab)
    dam = np.zeros((x,y,z), np.uint8)

    #Pavage
    pav = np.zeros((crop_width, crop_length, z), np.uint8)

    #Fill in each subdivision to have a damier
    for i in range(x//crop_width):
        for j in range(y//crop_length):
            pix = tab_sub[i,j]
            dam[i*crop_width:(i+1)*crop_width,j*crop_length:(j+1)*crop_length] = fill.fill_in(pav, pix)
            
    return dam



def mosaic(image, crop_length = CROP_LENGTH, crop_width = CROP_WIDTH, show = NOT_SHOW):
    """
    :param image: image to do a mosaic
    :param crop: crop factor, how many pixel are in subdivision
    :return: the sample tab and the mosaic (Image)
    
    Autor : Adrien  2017-11-23
    Modification :
    > Adel      2017-11-24
    > Adel      2017-11-25
    > Adel      2017-12-25
    > Adrien    2017-12-28
    > Adrien    2017-12-28
    """
    
    #Create a table of the image
    tab = np.array(image)    
    
    #Make a mosaic
    dam = damier(tab, crop_length, crop_width)
    
    #Show the mosaic
    mosa = Image.fromarray(dam)
    if show:
        mosa.show()

