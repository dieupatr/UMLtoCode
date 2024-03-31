
from LexDrawio import *



file_path = 'TestRunDia.drawio'  

Dia=ParseDiagramsFromXmlFile(file_path)





Blocks= Dia["Test1"].blocks
Arrows=Dia["Test1"].arrows


for block  in Blocks:

    block.PrintData()

    

for arrow in Arrows:

    arrow.PrintData()
