from LexDrawio import *

import os
import sys


#Create folder
# Generate by ChatGpt
# Valid +
def create_folder(folder_name):
    try:
        os.mkdir(folder_name)
        print(f"Folder '{folder_name}' created successfully.")
    except FileExistsError:
        print(f"Folder '{folder_name}' already exists.")


#Create file
# Generate by ChatGpt
# Valid +
def create_file(file_name):
    try:
        with open(file_name, 'w') as file:
            file.write("")
        print(f"File '{file_name}' created successfully.")
    except Exception as e:
        print(f"Error occurred: {e}")






#Build folders from a drawio diagram
        
def BuildFolders(FilePathXml):

    MxDiagrams=ParseDiagramsFromXmlFile(FilePathXml)


    for   key    in MxDiagrams:

        RootName=key+"\\"
        diagram=MxDiagrams[key]
        Blocks= diagram.blocks
        
        for block in Blocks:

            FileName=RootName+block.Attr['value']
            
            if(   block.Attr['style'][0]=="shape=folder" ):
                
                
                create_folder( FileName)

            if(block.Attr['style'][0]=="shape=card"):

                create_file(FileName)

                

BuildFolders(sys.argv[1])



        
        
    






















    
    

    



