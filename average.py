"""
REV 4_1
Contributors : Adel, Adrien, Morgan, Aurelien
Last modification date : 2018-01-19
REV4
Séparation fichiers

"""
import numpy as np
from variables import *



def get_moy_pix(area, crop = MOY_FACTOR):
    """
    :param area: area to get the color from, n.array
    :param crop: sample rate
    :return: the average color of the area
    
    Autor : Adel
    Modification :
    > Adrien    2017-11-23
    > Adel      2017-11-24
    > Adrien    2017-12-26
    > Adel      2017-12-27
    """
    
    #The average color (R,G,B)
    moy_pix = [0,0,0]
    
    #The shape of the area
    x,y,z = np.shape(area)

    #Number of pixels analyzed
    nb_pix = (x//crop)*(y//crop)
    
    #Sum all the pixel of the arrea by color
    for i in range(x//crop):
        for j in range(y//crop):
            for color in COLOR:
                
                #Calculate the average
                moy_pix[color] += area[crop*i,crop*j,color]/nb_pix
                
    #Return a pixel (R,G,B), universal integer 8bis (mandatory for Image)
    return np.array(moy_pix, np.uint8)

	
	
def get_moy_pix_tri(area, line, column):
    """
    :param: square to get the 2 triangles colors
    :return: the 2 average colors
    
    Autor: Adrien
    Modification :
    > Adel    2018-01-19	
    """

    #The average color (R,G,B)
    moy_pix = [[0,0,0] for k in range (2)]

    #The shape of the area
    x,y,z = np.shape(area)

    #Number of pixels analyzed by triangle
    nb_pix_max = (x*(x+1))/2
    nb_pix_min = (x*(x-1))/2

    ##Sum all the pixel of the area by color in each triangle
    #diagonal from bottom left to top right
        #  _____
	# |    /|
	# |  /  |
	# |/____|


    if (line + column)%2 == 0:
        for i in range (x):
            for j in range(x):
                for color in COLOR:
                    
                    #Averages : index 0 for left triangle, index 1 for right triangle
                    if i+j <= x-1:
                        moy_pix[0][color] += area[i,j,color]/nb_pix_max
                    else:
                        moy_pix[1][color] += area[i,j,color]/nb_pix_min
                        
    #diagonal from bottom right to top left
        #  _____
	# |\    |
	# |  \  |
	# |____\|
	
    else:
        for i in range (x):
            for j in range(x):
                for color in COLOR:
                    #Averages : 0 for left triangle, 1 for right triangle
                    if j <= i:
                        moy_pix[0][color] += area[i,j,color]/nb_pix_max
                    else:
                        moy_pix[1][color] += area[i,j,color]/nb_pix_min
                        
    #Return a matrix of 2 pixels (R,G,B), universal integer 8bis (mandatory for Image)
    return np.array(moy_pix, np.uint8)



def moy_pix(liste):
    """
    :param mat: mat to modify
    :param list_ind: list of the index to get the average
    :return: the new mat
    Autor: Adrien   2018-01-16
    """
    n = len(liste)
    pix = np.zeros((3), np.float64)

    #The average
    for k in range(n):
        for color in COLOR:
            pix[color] += liste[k][color]/n
            
    return pix
	
	


