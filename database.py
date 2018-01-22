from PIL import Image
import os
import numpy as np
import average
from variables import *


#data_base_writing_file

def update_data_base(name, database_path = DATABASE_PATH, ui = None):
    """
    :param database_path: path of the folder which contains all the files
    :write: text file of files list
    Autor :     Adrien
    Modifications:
    > Adel      2017-11-25
    > Adel      2017-11-26
    > Adel      2017-11-27
                            
    """
    
    list_files_database = os.listdir(database_path)
    
    #path of the database
    database_file_path = name 
    
    #writing on the file
    with open (database_file_path,'w') as f:
        
        n = len(list_files_database)
        i=0
        for file in list_files_database:
            
            i +=1
            path_file = database_path + '/' + file
            try : 
                #Open the image and get the pixels
                im = Image.open(path_file)
                aera = np.array(im)
                im.close()
                
                #Get the pixels value
                moy_pix_np = average.get_moy_pix(aera) 
                moy_pix = str(moy_pix_np[RED]) + ';' + str(moy_pix_np[GREEN]) + ';' + str(moy_pix_np[BLUE])
                gray = np.uint8(int(moy_pix_np[RED]*0.21 + moy_pix_np[GREEN]*0.72 + moy_pix_np[BLUE]*0.07))
                
                #Write in the file
                f.write(path_file + ';' + moy_pix + ';' + str(gray) + '\n')
                if ui != None : ui.pb_avance.setValue(i/n+1)
                
            except OSError:
                print("Erreur fichier : "+file+'\t'+str(i/n))
                #delete 
            
            
            
            
            

def get_image_base(name):
    """
    :return: The list of all images in the database
    Autor : Adel
    Modification :
    > Adel      2017-11-24  
    """
    
    database_file_path = name 
    
    #Read the file and save the data
    with open(database_file_path,'r') as file:
        images = [ line[:-1].split(';') for line in file]
        
    return images

    
if __name__ == "__main__":
   update_data_base("DATA.txt")
