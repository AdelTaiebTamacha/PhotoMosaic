"""
REV 4_1
Contributors : Adel, Adrien, Morgan, Aurelien
Last modification date : 2018-01-19
REV4
Séparation fichiers

"""
import numpy as np
import resize
from variables import *

def color_to_grayscale(tab, show_advance = NOT_SHOW):    
    """
    :param tab: the tab to convert into grayscale 
    :param show: print the average percentage (default : not showing)
    :return: the given tab with only grascale value
    
    Autor : Adel 2017-11-24
    Modification:
    > Adel       2017-11-25
    > Adel       2018-01-19
    """
    
    #Dimension of the table
    x, y, z = np.shape(tab)

    #Create an empty subtable with the previous dimension
    gray3 = np.zeros((x, y,z), np.uint8)

    #Calculate each pixel gray value of the table
    for i in range(x):
        for j in range(y):
 
            for color in COLOR:
                gray3[i,j,color] = tab[i,j,RED]*0.21 + tab[i,j,GREEN]*0.72 + tab[i,j,BLUE]*0.07
    
    return gray3



def fill_in(tab, pix):
    """
    :param tab: table to fill
    :param pix: the pixel color
    :return: the table filled with the given pixel
    
    Autor : Adrien    2017-11-20
    Modification :
    > Adel      2017-11-24
    """
    
    #Fill in the table
    for color in COLOR:
        tab[:,:,color].fill(pix[color])
        
    return tab


	
def fill_top_left(final, tab, beggi):
    """
    :param final: final table which has to be modified (fill in the triangle)
    :param tab: table of the image tu put in trangle
    :param beggi: tuple of the position of the first element in tab to put in beggi
    :return: the final table
	
    Autor : Bouba   2018-01-11
    """
	
    #Axial position of beggin
    beggi_x, beggi_y = beggi
    
    #Dimensions
    x, y, z = np.shape(tab)
    
    #Fill in the triangle
    for i in range(x):
        for j in range(x):
            if i+j < x-1:
                final[beggi_x + i, beggi_y + j] = tab[i,j]
    return final



def fill_top_right(final, tab, beggi):
    """
    :param final: final table which has to be modified (fill in the triangle)
    :param tab: table of the image tu put in trangle
    :param beggi: tuple of the position of the first element in tab to put in beggi
    :return: the final table
	
    Autor : Bouba   2018-01-11
    """
	
    #Axial position of beggin
    beggi_x, beggi_y = beggi

    #Dimensions
    x, y, z = np.shape(tab)
    
    #Fill in the triangle
    for i in range(x):
        for j in range(x):
            if j >= i:
                final[beggi_x + i, beggi_y + j] = tab[i,j]
    return final



def fill_bot_left(final, tab, beggi):
    """
    :param final: final table which has to be modified (fill in the triangle)
    :param tab: table of the image tu put in trangle
    :param beggi: tuple of the position of the first element in tab to put in beggi
    :return: the final table
	
    Autor : Bouba   2018-01-11
    """
	
    #Axial position of beggin
    beggi_x, beggi_y = beggi
    
    #Dimensions
    x, y, z = np.shape(tab)
    
    #Fill in the triangle
    for i in range(x):
        for j in range(x):
            if j < i:
                final[beggi_x + i, beggi_y + j] = tab[i,j]
    return final

	

def fill_bot_right(final, tab, beggi):
    """
    :param final: final table which has to be modified (fill in the triangle)
    :param tab: table of the image tu put in trangle
    :param beggi: tuple of the position of the first element in tab to put in beggi
    :return: the final table
	
    Autor : Bouba   2018-01-11
    """
	
    #Axial position of beggin
    beggi_x, beggi_y = beggi
    
    #Dimensions
    x, y, z = np.shape(tab)
    
    #Fill in the triangle
    for i in range(x):
        for j in range(x):
            if i+j >= x-1:
                final[beggi_x + i, beggi_y + j] = tab[i,j]
    return final



def fill_los(final, tab, crop, beggi, i, x, j, y):
    """
    :param final: table which has to be modified
    :param tab: table of the image xhich has to be on the final table
    :param beggi: tuple of the beggining index
    :param crop: crop of the triangle wanted
    :param: i line, x number of lines, j column, y number of column 
    :return: the final table modified

    Autor : Bouba   2018-01-11
    """

    #Beggining index
    beggi_x, beggi_y = beggi
    
    #Triangle top left in a square or rectangle
    if (i,j) == (0,0):
        tab = resize.resize(tab, (crop, crop))
        final = fill_top_left(final, tab, beggi)
        
    #Triangle top right
    elif (i,j)==(0,y-1):
        tab = resize.resize(tab, (crop, crop))
        final = fill_top_right(final, tab, beggi)
        
    #Triangle bottom left
    elif (i,j)==(x-1,0):
        tab = resize.resize(tab, (crop, crop))
        final = fill_bot_left(final, tab, beggi)
        
    #Triangle bottom right
    elif (i,j) == (x-1, y-1):
        tab = resize.resize(tab, (crop, crop))
        final = fill_bot_right(final, tab, beggi)

    #Triangle left
    elif j==0:
        tab = resize.resize(tab, (crop, 2*crop))
        final = fill_bot_left(final, tab[:crop,:crop], beggi)
        final = fill_top_left(final, tab[crop:2*crop,:crop], (beggi_x+crop, beggi_y))
                
    #Triangle right
    elif j==y-1:
        tab = resize.resize(tab, (crop, 2*crop))
        final = fill_bot_right(final, tab[:crop,:crop], beggi)
        final = fill_top_right(final, tab[crop:2*crop,:crop], (beggi_x+crop, beggi_y))
        
    #Triangle top
    elif i==0:
        tab = resize.resize(tab, (2*crop, crop))
        final = fill_top_right(final, tab[:,:crop], beggi)
        final = fill_top_left(final, tab[:,crop:2*crop], (beggi_x, beggi_y+crop))
        
    #Triangle bottom
    elif i==x-1:
        tab = resize.resize(tab, (2*crop, crop))
        final = fill_bot_right(final, tab[:crop,:crop], beggi)
        final = fill_bot_left(final, tab[:crop,crop:2*crop], (beggi_x, beggi_y+crop))
    
    #Losange
    else:
        tab = resize.resize(tab, (2*crop, 2*crop))
        final = fill_bot_right(final, tab[:crop,:crop], beggi)
        final = fill_bot_left(final, tab[:crop, crop:2*crop], (beggi_x, beggi_y+crop))
        final = fill_top_right(final, tab[crop:2*crop, :crop], (beggi_x+crop, beggi_y))
        final = fill_top_left(final, tab[crop:2*crop, crop:2*crop], (beggi_x+crop, beggi_y+crop))

    return final



def fill_hex(final, tab, crop, beggi, i, x, j, y):
    """
    :param final: table which has to be modified
    :param tab: table of the image which has to be on the final table
    :param beggi: tuple of the beggining index
    :param crop: crop of the triangle wanted
    :param: i line, x number of lines, j column, y number of column 
    :return: the final table modified
	
    Autor : Bouba   2018-01-16
    """

    #Beggining index
    beggi_x, beggi_y = beggi

    #Triangle top left in a square or rectangle
    if (i,j) == (0,0):
        tab = resize.resize(tab, (crop, crop))
        final = fill_top_left(final, tab, beggi)
        
    #Triangle top right
    elif (i,j)==(0,y-1):
        tab = resize.resize(tab, (crop, crop))
        final = fill_top_right(final, tab, beggi)
        
    #Triangle bottom left
    elif (i,j)==(x-1,0):
        tab = resize.resize(tab, (crop, crop))
        final = fill_bot_left(final, tab, beggi)
        
    #Triangle bottom right
    elif (i,j) == (x-1, y-1):
        tab = resize.resize(tab, (crop, crop))
        final = fill_bot_right(final, tab, beggi)

    #Triangle top
    elif i==0:
        tab = resize.resize(tab, (2*crop, crop))
        final = fill_top_right(final, tab[:,:crop], beggi)
        final = fill_top_left(final, tab[:,crop:2*crop], (beggi_x, beggi_y+crop))
        
    #Triangle bottom
    elif i==x-1:
        tab = resize.resize(tab, (2*crop, crop))
        final = fill_bot_right(final, tab[:crop,:crop], beggi)
        final = fill_bot_left(final, tab[:crop,crop:2*crop], (beggi_x, beggi_y+crop))

    #Semi-hexagon left
    elif j==0 and i%2 == 0:
        tab = resize.resize(tab,(crop, 3*crop))
        final = fill_bot_left(final, tab[:crop,:], beggi)
        final = fill_top_left(final, tab[2*crop:,:], (beggi_x + 2*crop, beggi_y))
        final[beggi_x + crop:beggi_x + 2*crop, beggi_y: beggi_y + crop] = tab[crop:2*crop, :]

    #Semi-hexagon right
    elif j == y-1 and i%2 == 0:
        tab = resize.resize(tab,(crop, 3*crop))
        final = fill_bot_right(final, tab[:crop,:], beggi)
        final = fill_top_right(final, tab[2*crop:,:], (beggi_x + 2*crop, beggi_y))
        final[beggi_x + crop:beggi_x + 2*crop, beggi_y: beggi_y + crop] = tab[crop:2*crop, :]

    #Hexagon
    else:
        tab = resize.resize(tab, (2*crop, 3*crop))
        final = fill_bot_right(final, tab[:crop, :crop], beggi)
        final = fill_bot_left(final, tab[:crop, crop:], (beggi_x, beggi_y + crop))
        final = fill_top_left(final, tab[2*crop:,crop:], (beggi_x + 2*crop, beggi_y + crop))
        final = fill_top_right(final, tab[2*crop:, :crop], (beggi_x + 2*crop, beggi_y))
        final[beggi_x + crop: beggi_x + 2*crop, beggi_y: beggi_y + 2*crop] = tab[crop:2*crop, :]
        
    return final
