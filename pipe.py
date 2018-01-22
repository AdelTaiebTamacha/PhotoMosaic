"""
REV 4_1
Contributors : Adel, Adrien, Morgan, Aurelien
Last modification date : 2018-01-19
REV4
Séparation fichiers

"""

from PIL import Image
import numpy as np
import recover
import reduction
import slicer
import create
from variables import *


def photomosaic(image, crop_length = CROP_LENGTH, crop_width = CROP_WIDTH, ui = None):
    """
    :param pix: pixel to which find a corespondant image
    :param data: the images data list
    :return: the path to corespondant image with color bond using the gray bond as first filter
	
    Autor Adrien      2018-01-09
    Modification:
    > Adel      2018-01-09    
    """
    
    #   Convert image
    tab = np.array(image)
    
    #   Create color mosaic
    tab_sub = reduction.get_sub_tab(tab, crop_length, crop_width)
    dam = slicer.damier(tab, crop_length, crop_width)
    
    #   CHOSE IMAGES FROM COLORS
    images = recover.get_images(tab_sub, False, ui)
    
    #   CREATE FINAL IMAGE FROM IMAGES
    final_table, err = create.create(images, crop_length, crop_width, ui)
    final_image = Image.fromarray(final_table)
    
    return final_image



def photomosaic_tri(image, crop = CROP, ui = None):

    #   Convert image
    tab = np.array(image)

    #CREATE COLOR MOSAIC
    mat_tab_sub = reduction.get_sub_tab_tri(tab, crop)

    #CHOSE IMAGES FROM COLORS
    mat_images = recover.get_images_tri(mat_tab_sub, ui)

    #CREATE FINAL IMAGE
    final = create.create_tri(mat_images, crop, ui)
    mosa = Image.fromarray(final)

    return mosa



def photomosaic_los(image, crop = CROP, ui = None):

    #   Convert image
    tab = np.array(image)

    #CREATE COLOR MOSAIC
    tab_sub = reduction.get_sub_tab_los(tab, crop)

    #CHOSE IMAGES FROM COLORS
    images = recover.get_images(tab_sub, True, ui)

    #CREATE FINAL IMAGE
    final = create.create_los(images, crop, ui)
    mosa = Image.fromarray(final)

    return mosa



def photomosaic_hex(image, crop = CROP, ui=None):
    
    #   Convert image
    tab = np.array(image)

    #CREATE COLOR MOSAIC
    tab_sub = reduction.get_sub_tab_hex(tab, crop)

    #CHOSE IMAGES FROM COLORS
    images = recover.get_images(tab_sub, True, ui)

    #CREATE FINAL IMAGE
    final = create.create_hex(images, crop, ui)
    mosa = Image.fromarray(final)

    return mosa
    
