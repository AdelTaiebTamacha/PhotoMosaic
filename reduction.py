"""
REV 4_1
Contributors : Adel, Adrien, Morgan, Aurelien
Last modification date : 2018-01-19
REV4
Séparation fichiers

"""
import numpy as np
import average
from variables import *


def get_sub_tab(tab, crop_length = CROP_LENGTH, crop_width = CROP_WIDTH):
    """
    :param tab: table to subdivise
    :param crop: crop factor, how many pixel are in a smaller tab
    :return: the smaller sample table
    
    Autor : Adel
    Modification :
    > Adrien    2017-11-23
    > Adel      2017-11-24
    > Adel      2017-11-25
    > Adrien    2017-12-26
    > Adrien    2018-01-10
    """

    #Dimension of the table
    x, y, z = np.shape(tab)

    #Dimension of the subtable
    x, y = x//crop_width, y//crop_length

    #Choose the crop for the pixel average
    min_crop = min(crop_length, crop_width)
    if min_crop < 10 :
        crop = min_crop//2
    elif min_crop < 20 :
        crop = min_crop//5
    else :
        crop = MOY_FACTOR

    #Create an empty subtable with the previous dimension
    tab_sub = np.zeros((x, y, z), np.uint8)

    #Calculate each pixel (R,G,B) of the subtable
    for i in range(x):
        for j in range(y):
            tab_sub[i,j] = average.get_moy_pix(tab[i*crop_width:(i+1)*crop_width,j*crop_length:(j+1)*crop_length],crop)

    return tab_sub



def get_sub_tab_tri(tab, crop = CROP):
    """
    :param tab: table to subdivise in triangles
    :param crop: crop factor, how many pixel are in a smaller tab
    :return: the matrix of the smaller sample table
	
    Autor : Bouba   2018-01-16
    """

    #Dimension of the table
    x, y, z = np.shape(tab)

    #Dimension of the subtable
    x, y = x//crop, y//crop

    #Create an empty subtable with the previous dimension
    mat_tab_sub = np.zeros((x, y, TRIANGLE_DIMENSION, z), np.uint8)

    #Calculate each pixel (R,G,B) of the subtable
    for i in range(x):
        for j in range(y):
            mat_tab_sub[i,j] = average.get_moy_pix_tri(tab[i*crop:(i+1)*crop,j*crop:(j+1)*crop], i ,j)

    return mat_tab_sub



def get_sub_tab_los(tab, crop = CROP):
    """
    :param tab: table to sbdivise in losanges
    :param crop: crop factor of the losange
    :return: the table of average pixels
	
    Autor : Bouba    2018-01-16
    Modification :
    > Adel 	2018-01-19
    """

    # Make the table of triangles
    table_tri = get_sub_tab_tri(tab, crop)

    #Dimension of the table
    x, y, z = np.shape(tab)
    x = 2*(x//(2*crop))
    y = 2*(y//(2*crop))
    
    #Dimensions of the subtable
    new_x = x+1
    y_firstline = y//2 + 1
    

    #Create an empty subtable with new dimension
    tab_sub = np.zeros((new_x, y_firstline, 3), np.uint8)
    
    #Calculate each pixel (R,G,B) of the subtable
    for i in range(new_x):
        for j in range(y_firstline):
            #Lines pairs
            if i%2 == 0:

                #First line
                if i==0:
                    #First column --> triangle top left
                    if j==0: 
                        tab_sub[i,j] = table_tri[0,0,0]
                    #Last column --> triangle top right
                    elif j==y_firstline-1: 
                        tab_sub[i,j] = table_tri[0,2*j-1,1]
                    #Middle --> triangles top
                    else: 
                        tab_sub[i,j] = average.moy_pix([table_tri[i,2*j-1,1],table_tri[i,2*j,0]])

                #First column
                elif j==0 :
                    #Last line --> triangle bottom left
                    if i == new_x-1: 
                        tab_sub[i,j] = table_tri[i-1,j,0]
                    #Middle --> triangle left
                    else: 
                        tab_sub[i,j] = average.moy_pix([table_tri[i-1,j,0], table_tri[i,j,0]])

                #Last line
                elif i==new_x-1:
                    #Last column --> triangle bottom right
                    if j == y_firstline-1: 
                        tab_sub[i,j] = table_tri[i-1,2*j-1,1]
                    #Middle --> triangle bottom
                    else: 
                        tab_sub[i,j] = average.moy_pix([table_tri[i-1,2*j-1,1], table_tri[i-1,2*j,0]])

                #Last column --> triangle right
                elif j == y_firstline-1: 
                        tab_sub[i,j] = average.moy_pix([table_tri[i-1,2*j-1,1], table_tri[i,2*j-1,0]])

                #Middle --> Losanges
                else : 
                    tab_sub[i,j] = average.moy_pix([table_tri[i-1,2*j-1,1], table_tri[i-1,2*j,0], table_tri[i,2*j-1,1], table_tri[i,2*j,0]])

            #Lines not pair
            elif j != y_firstline-1: 
                tab_sub[i,j] = average.moy_pix([table_tri[i-1,2*j,1], table_tri[i-1,2*j+1,0], table_tri[i,2*j,1], table_tri[i,2*j+1,0]])

    return tab_sub



def get_sub_tab_hex(tab, crop = CROP):
    """
    :param tab: table to sbdivise in hexagones
    :param crop: crop factor of the hexagone
    :return: the table of average pixels
	
    Autor : Bouba   2018-01-16
    """

    #Dimension of the table
    x, y, z = np.shape(tab)

    #Resize
    x_square, y_square = x//crop, y//crop
    
    if x_square%2 == 1:
        x_square -= 1
    if y_square%2 == 0:
        y_square -= 1


    first_mat = np.zeros((x_square, y_square, 2, 3), np.uint8)

    #New matrix dimensions : subdivisions in hexagons
    columns = y_square//2 + 1
    lines = (x_square + 1)//2 + 1

    ##First mat with triangles and squares
	
    #First line in triangles
    mat = tab[:crop,:y_square*crop,:]
    new_mat = get_sub_tab_tri(mat, crop)
    first_mat[0,:y_square] = new_mat

    for i in range(1,x_square):

        #Odd lines in squares
        if i%2 == 1:
            intermediate_tab = get_sub_tab(tab[i*crop:(i+1)*crop,:y_square*crop,:], crop, crop)
            for k in range(np.shape(intermediate_tab)[1]):
                first_mat[i,k] = [intermediate_tab[0][k], intermediate_tab[0][k]]

        #Even lines in triangles
        else:
            #Triangles like the bottom of losanges
            if (i//2)%2 == 1:
                intermediate_tab = get_sub_tab_tri(tab[(i-1)*crop:(i+1)*crop, :y_square*crop, :], crop)
                first_mat [i, :y_square] = intermediate_tab[1,:,:]
            #Triangle like the top of losanges
            else:
                intermediate_tab = get_sub_tab_tri(tab[i*crop:(i+1)*crop, :y_square*crop, :], crop)
                first_mat [i, :] = intermediate_tab[:,:,:]

    #New table for subdivions in hexagons
    tab_sub = np.zeros((lines, columns, 3), np.uint8)
    
    for i in range(lines):
        for j in range(columns):

            #First line
            if i == 0:
                #First column --> triangle top left
                if j==0:
                    tab_sub[i,j] = first_mat[0,0,0]
                #Last column --> triangle top right
                elif j == columns-1:
                    tab_sub[i,j] = first_mat[0,2*j-1, 1]
                # Middle --> Triangle top
                else:
                    tab_sub[i,j] = average.moy_pix([first_mat[i,2*j-1,1], first_mat[i,2*j,0]])

            #Last line
            elif i == lines-1:
                #First column --> triangle bottom left
                if j ==0:
                    tab_sub[i,j] = first_mat[2*(i-1),0, 0]
                #Last column --> triangle bottom right
                elif j == columns-1 :
                    tab_sub[i,j] = first_mat[2*(i-1),2*j-1,1]
                #Middle --> Triangle bottom
                else:
                    tab_sub[i,j] = average.moy_pix([first_mat[2*(i-1),2*j-1,1], first_mat[2*(i-1),2*j,0]])

            #First column and pair line --> Semi-Hexagon left
            elif j == 0 and i%2 == 0: 
                tab_sub[i,j] = average.moy_pix([first_mat[2*i-2,0,0], first_mat[2*i-1,0,0], first_mat[2*i-1,0,1], first_mat[2*i,0,0]])

            #Last column and pair line --> Semi-Hexagon right
            elif j == columns-1 and i%2 == 0: 
                tab_sub[i,j] = average.moy_pix([first_mat[2*i-2,2*j-1,1], first_mat[2*i-1,2*j-1,0], first_mat[2*i-1,2*j-1,1], first_mat[2*i,2*j-1,1]])

            #Middle --> Hexagons
            elif j!= columns-1:
                #For impair lines
                if i%2 == 1:
                    tab_sub[i,j] = average.moy_pix([first_mat[2*i-2,2*j,1], first_mat[2*i-2,2*j+1,0], first_mat[2*i-1,2*j,0], first_mat[2*i-1,2*j,1], first_mat[2*i-1,2*j+1,0], first_mat[2*i-1,2*j+1,1], first_mat[2*i,2*j,1], first_mat[2*i,2*j+1,0]])
                #For pair lines
                else:
                    tab_sub[i,j] = average.moy_pix([first_mat[2*i-2,2*j-1,1], first_mat[2*i-2,2*j,0], first_mat[2*i-1,2*j-1,0], first_mat[2*i-1,2*j-1,1], first_mat[2*i-1,2*j,0], first_mat[2*i-1,2*j,1], first_mat[2*i,2*j-1,1], first_mat[2*i,2*j, 0]])

    return tab_sub
