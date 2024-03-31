
from LexDrawio import *



file_path = 'TestRunDia.drawio'  

Dia=ParseDiagramsFromXmlFile(file_path)


SortBlocksByLevel(Dia["Test1"],"y")



Blocks= Dia["Test1"].blocks
Arrows=Dia["Test1"].arrows


for block  in Blocks:

    #block.PrintData()

    print(block.Geometry)

for arrow in Arrows:

    print(arrow.Geometry)
