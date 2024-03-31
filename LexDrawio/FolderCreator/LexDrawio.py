import xml.etree.ElementTree as ET
import html
import re


#Dokumentation erstellt mit der AI Tabine in Visual studio code




class Diagram:
    """
    A class to represent a UML Diagram.

    Attributes:
        blocks (list): A list of blocks in the diagram.
        arrows (list): A list of arrows in the diagram.
    """
    def __init__(self):
           
           
        self.blocks = []
        self.arrows = []
        
    def PrintArrows(self):

           for cell in self.arrows:

                  cell.PrintData()

    def PrintBlocks(self):

           for cell in self.blocks:

                  cell.PrintData()




class Cell:
    """
    A class to represent a UML Diagram cell.

    Attributes:
        Geometry (dict): A dictionary containing the geometry information of the cell.
        Attr (dict): A dictionary containing the attributes of the cell.

    """

    def __init__(self):
           self.Geometry={}
           self.Attr={}
           
    def PrintData(self):

           print(f"""
           id:                            {self.Attr['id']}
           parent:                {self.Attr['parent']}
           value:                   {self.Attr['value']}
           style:                     {self.Attr['style']}
           source:                 {self.Attr['source']}
           target:                  {self.Attr['target']}
           geometry:          {self.Geometry}
           
           ------------------------------------------------------
              """)



def SortBlocksByLevel(Diagram,attr):

    ####Bubble sort####

    N=len(Diagram.blocks)
     

    for j in range(N,2,-1):
        for k in range(j-1):
          
            if( float(   Diagram.blocks[k].Geometry[attr]   )>float(   Diagram.blocks[k+1].Geometry[attr]   )):
                
                #swapp
                dummy= Diagram.blocks[k+1]
                Diagram.blocks[k+1]=Diagram.blocks[k]
                Diagram.blocks[k]=dummy
                #####

    #################








def FormatHtmltoString(string):
    """
    This function takes a string that contains HTML escape sequences and converts it to a normal string by removing the HTML tags and replacing the HTML escape sequences with their original characters.

    Parameters:
    string (str): The input string that contains HTML escape sequences.

    Returns:
    str: The output string that contains no HTML tags and only the original characters.

    """
    # HTML-Escape-Sequenzen entschlüsseln
    decoded_string = html.unescape(string)
    #replace &nbsp and <br>
    clean_string = re.sub(r'&nbsp;', '  ', decoded_string)
    clean_string = re.sub(r'<br>', '\n', clean_string)
    # HTML-Tags entfernen
    clean_string = re.sub(r'<[^>]+>', '',  clean_string)
    
    return clean_string



def ReadXmlString(file_path):
       
       with open(file_path, 'r') as file:
              xml_string = file.read()

       return xml_string



def ExtractAtributes(Entry, ListAttributes ):
    
    ExtractedAtributes={   }

    for attr in ListAttributes:

        ExtractedAtributes[attr]=Entry.attrib.get(attr)

    return  ExtractedAtributes

        

def ExtractCellsFromDiagram( mxGraphModel ):
       """
    Extracts the cells from an mxGraphModel Element.

    Args:
        mxGraphModel (xml.etree.ElementTree.Element): The mxGraphModel Element.

    Returns:
        List[Cell]: A list of Cell objects."""
       
       
       CellSet = mxGraphModel.findall('.//mxCell')
       MxDiagram=[   ]

       ListAttributesGeometry=["x","y", "width", "height" , "as"]
       ListAttributesCell=["id","value",'style',  'parent', 'target', 'source']
       
       for cell in CellSet:

              Cell_curent=Cell()
              Cell_curent.Attr=ExtractAtributes(cell, ListAttributesCell )
              
        #Format style and  value
              try:
                  Cell_curent.Attr['value']=FormatHtmltoString( Cell_curent.Attr['value'] )
              except:
                  pass
                
              try:
                  Cell_curent.Attr['style']=Cell_curent.Attr['style'].split(";")        
              except:
                  
                  pass

              geometry=cell.find('.//mxGeometry')
              for attr in ListAttributesGeometry:
                  try:
                      Cell_curent.Geometry[attr]= geometry.  attrib.get(attr)
                  except:
                      pass
             
              MxDiagram.append(Cell_curent)

       return MxDiagram
              


def ClassifyCells(MxDiagram):
       """
    This function takes a list of mxCell objects and classifies them into blocks and arrows based on their style and geometry attributes.

    Parameters:
    MxDiagram (list): A list of mxCell objects.

    Returns:
    Diagram: A Diagram object containing the classified blocks and arrows.

    """

       Dia=Diagram()

       for cell in MxDiagram:

              if(cell.Attr['style']!=None):

                     if(cell.Geometry["x"]!=None or cell.Geometry["y"]!=None ):

                            Dia.blocks.append(cell)
                            
                     else:

                              Dia.arrows.append(cell)
                            
       return Dia

                     

def ParseDiagramsFromXmlFile(file_path):
       """
    Parse a UML XML file and extract the diagrams contained within it.

    Parameters:
        file_path (str): The path to the UML XML file.

    Returns:
        Dict[str, Diagram]: A dictionary where the key is the name of the diagram and the value is the Diagram object.
    """
       

       xml_string=ReadXmlString(file_path)

       Diagrams={    }
       
      
       mxFile = ET.fromstring(xml_string)

       MxDiagrams = mxFile.findall('.//diagram')

       for diagram in MxDiagrams:

              DiagramName= diagram.attrib.get('name')

              mxGraphModel = diagram.find('.//mxGraphModel')

              MxCells=ExtractCellsFromDiagram( mxGraphModel )

              Diagrams[DiagramName]=ClassifyCells(MxCells)

       return Diagrams

              

















