"""
REV 4_1
Contributors : Adel, Adrien, Morgan, Aurelien
Last modification date : 2018-01-19
REV4
Séparation fichiers

"""
from variables import *
import random as rd


def select_gray_image(pix, data, eps = EPS):
    """
    :param pix: pixel to which find a corespondant image
    :param data: the images data list
    :return: the path to corespondant image with gray bond
	
    Autor Adel      2017-11-25
    Modification:
    > Morgan    2017-12-27
    """

    red = pix[RED]
    green = pix[GREEN]
    blue = pix[BLUE]
    gray = red*0.21 + green*0.72 + blue*0.07   
    l=[]
    
    
    for line in data:
        if -eps+gray <= int(line[D_GRAY]) <= eps+10+gray:
            l.append(line[D_PATH])
            
    n = len(l)
    if n == 0 :
        return select_gray_image(pix, data, eps + 10)
    if n==1:
        return l[0]
    elif n>1 :
        return rd.choice(l)

		

def select_color_image(pix, data, eps=EPS):
    """
    :param pix: pixel to which find a corespondant image
    :param data: the images data list
    :return: the path to corespondant image with color bond using the gray bond as first filter
	
    Autor Morgan      2017-12-11
    Modification:
    > Adel      2017-12-26
    > Morgan    2017-12-27       
    """

    red = pix[RED]
    green = pix[GREEN]
    blue = pix[BLUE]
    gray = red*0.21 + green*0.72 + blue*0.07    
    l=[]    
    
    for line in data:

        if -eps+gray <= int(line[D_GRAY]) <= eps+10+gray:
           
            if -eps+blue <= int(line[D_BLUE]) <= eps+10+blue:
                if -eps+red <= int(line[D_RED]) <= eps+10+red:
                    if -eps+green <= int(line[D_GREEN]) <= eps+10+green:
                        l.append(line[D_PATH])   
            
            
    n = len(l)
    if n == 0 :
        return select_color_image (pix, data, eps + 10)
    elif n==1:
        return l[0]
    else: #n>1
        return rd.choice(l)
	
	

def select_color_image_2(pix, data, eps=EPS):
    """
    :param pix: pixel to which find a corespondant image
    :param data: the images data list
    :return: the path to corespondant image with color bond using the gray bond as first filter
	
    Autor Morgan      2017-12-11
    Modification: 
    > Morgan    2017-12-27
    """
    
    red = pix[RED]
    green = pix[GREEN]
    blue = pix[BLUE]
    gray = red*0.21 + green*0.72 + blue*0.07    
    l=[]
    
    
    for line in data:
        if -eps+gray <= int(line[D_GRAY]) <= eps+1+gray:
            l+= [line]
    i = len(l)
    if i==0 :
        return select_color_image (pix, data, eps + 1)
    else :
        for line in l :
            if not -eps+blue <= int(line[D_BLUE]) <= eps+1+blue:
                l -= [line]
                i -= 1
        if i==0 :
            return select_color_image (pix, data, eps + 1)
        else :   
            for line in l:
                if not -eps+red <= int(line[D_RED]) <= eps+1+red:
                    l -= [line]
                    i -= 1
            if i==0 :
                return select_color_image (pix, data, eps + 1)
            else :
                for line in l:
                    if not -eps+green <= int(line[D_GREEN]) <= eps+1+green:
                        l-= [line]
                        i-=1
                if i==0 :
                    return select_color_image (pix, data, eps + 1)
                elif n==1:
                    return l[0]
                else: # n>1 :
                    return rd.choice(l)   

