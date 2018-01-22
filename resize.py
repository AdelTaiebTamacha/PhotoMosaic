"""
REV 4_1
Contributors : Adel, Adrien, Morgan, Aurelien
Last modification date : 2018-01-19
REV4
Séparation fichiers

"""
import numpy as np
import reduction


def resize(tab, size):
    """
    :param img: table to resize
    :param size: tuple of the desired size
    :return: the table of the resized image
	
    Autor Adel      2017-11-24
    Modification:
    > Adel  2017-12-26 
    > Adrien 2017-12-28
    > Adrien 2018-01-10
    """
    
    #Dimension of the table
    x, y, z = np.shape(tab)

    #New dimensions
    newlength = size[0]
    newwidth = size[1]

    #Ratio between the table size and the wanted pavage size
    ratio = int(min(x/newwidth, y/newlength))

    #Dimensions of the selection on the image
    length_select = newlength*ratio
    width_select = newwidth*ratio

    #First pixel choosen to center the selection
    first_x = (x-width_select)//2
    first_y = (y-length_select)//2
    
    #Reshape the image
    tab = tab[first_x : first_x + width_select, first_y : first_y + length_select]
        
    #Resize by dividing the size by ratio
    tab = reduction.get_sub_tab(tab, ratio, ratio)    
    
    return tab



def resize_tri(mat_tab, crop, line, column):
    """
    :param mat_tab: matrix of the 2 table to resize in triangles
    :param crop: crop of the tringle wanted
    :param line: the number of the line in mat_tab (2 ways to put 2 triangles in a square)
    :param column: the number of the column in mat_tab
    :return: the square table of the 2 triangles resized
    Autor : Bouba   2018-01-11
    """

    #First resize in a rectangle
    first_resize = [resize(mat_tab[0], (crop, crop)), resize(mat_tab[1], (crop, crop))]

    #New table
    new_tab = np.zeros((crop, crop, 3), np.uint8)

    # Create the resied image with the both triangle parts
	
	# Diagonal from bottom left to top right
	#  _____
	# |    /|
	# |  /  |
	# |/____|
    if (line + column)%2 == 0:
        for i in range (crop):
            for j in range(crop):
                    
                    ##Average
                    #Triangle left
                    if i+j <= crop-1: 
                        new_tab[i][j] = mat_tab[0][i][j]
                    #Triangle right
                    else: 
                        new_tab[i][j] = mat_tab[1][i][j]
						
	# Diagonal from bottom right to top left
	#  _____
	# |\    |
	# |  \  |
	# |____\|
    else:
        for i in range (crop):
            for j in range(crop):
                    #Average
                    #Triangle left
                    if j <= i:
                        new_tab[i][j] = mat_tab[0][i][j]
                    #Triangle right
                    else: 
                        new_tab[i][j] = mat_tab[1][i][j]

    return new_tab
