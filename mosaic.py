"""
REV 3_3
Contributors : Adel, Adrien, Morgan
Last modification date : 2018-01-16
REV3
Association avec interface graphique + Triangles, losanges et hexagones

"""
from PIL import Image
import numpy as np
from variables import *
import reduction
import recover
import slicer
import create




def main(crop_length = CROP_LENGTH, crop_width = CROP_WIDTH):
    
    name = "Avion.jpg"
    
    #   OPEN IMAGE
    image = Image.open(PATH+name)
    tab=np.array(image)    
    
    #   CREATE COLOR MOSAIC
    tab_sub = reduction.get_sub_tab(tab, crop_length, crop_width)
    dam = slicer.damier(tab, crop_length, crop_width)  
    
    #   CHOSE IMAGES FROM COLORS
    images = recover.get_images(tab_sub)   
    
    #   CREATE FINAL IMAGE FROM IMAGES
    final, err = create.create(images, crop_length, crop_width)
    mosa = Image.fromarray(final)
    mosa.show()
   
   
    
def main_tri(crop = CROP):

    name = "Avion.jpg"

    #OPEN
    image = Image.open(PATH + name)
    tab = np.array(image)
    image.show()

    #CREATE COLOR MOSAIC
    mat_tab_sub = reduction.get_sub_tab_tri(tab, crop)

    #CHOSE IMAGES FROM COLORS
    mat_images = recover.get_images_tri(mat_tab_sub)

    #CREATE FINAL IMAGE
    final = create.create_tri(mat_images, crop)
    mosa = Image.fromarray(final)
    mosa.show()



def main_los(crop = CROP):
                                               
    name = "Avion.jpg"

    #OPEN
    image = Image.open(PATH + name)
    tab = np.array(image)

    #CREATE COLOR MOSAIC
    tab_sub = reduction.get_sub_tab_los(tab, crop)

    #CHOSE IMAGES FROM COLORS
    images = recover.get_images(tab_sub, True)

    #CREATE FINAL IMAGE
    final = create.create_los(images, crop)
    mosa = Image.fromarray(final)
    mosa.show()



def main_hex(crop = CROP):

    name = "Avion.jpg"

    #OPEN
    image = Image.open(PATH + name)
    tab = np.array(image)

    #CREATE COLOR MOSAIC
    tab_sub = reduction.get_sub_tab_hex(tab, crop)

    #CHOSE IMAGES FROM COLORS
    images = recover.get_images(tab_sub)

    #CREATE FINAL IMAGE
    final = create.create_hex(images, crop)
    mosa = Image.fromarray(final)
    mosa.show()
    


if __name__ == "__main__":
    
    main()
