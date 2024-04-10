
from LexDrawio import *
import re
import sys




def DectectError(value,pattern):

       match=re.findall(pattern, value)
       
       

       if len(match)>0:
              print(f"Error in : {value} ")
              sys.exit(0)

       else:
              pass




def CheckSyntax( value,pattern):

    pattern = re.compile(pattern)
    if pattern.match(value):
        pass
       
    else:
           
           print(f"Syntax in : {value} '")
           sys.exit(0)
           
  #ToDo build better Syntax controll         
        
#r'^+?-[A-Za-z]:\s?b(?:\s?\[\d+\])?(?:=\d+)?(?:\{\d+(?:,\d+)?\})?$'
       

#############


def BuildClass_Cs(Methoden, Variables,Name, Parent):


       Name= re.sub(r'[^\x00-\x7F]+', '', Name)


       if Parent!="":
              Parent=":"+Parent+"_UML"

       Parent=re.sub(r'[^\x00-\x7F]+', '', Parent)


       #Variables

       Class_Atributes=""

       for var in Variables:

              attribute=var["mod"]+var["type"]

              try:
                     var["array"]
                     attribute=attribute+" "+" [ ]"
              except:
                     pass

              attribute=attribute+var["name"]

              try:
                     attribute=attribute+" "+"="+ var["value"]+";\n"
              except:
                      attribute=attribute+"{ get; set; }\n"

             

              Class_Atributes=Class_Atributes+attribute

       

       Class_Methods=""

       for var in Methoden:

              method=var["mod"]+" abstract  "+var["return"]+" "+var["name"]+" "

              method=re.sub(r'[^\x00-\x7F]+', '',method)

              parameter=var["var"]
             
            

              StringParam=""

              if len(parameter)>1:

                     StringParam="("+','.join(parameter)+" );"
                     StringParam=re.sub(r'[^\x00-\x7F]+', '',StringParam )
              else:
                     try:
                            value=parameter[0]
                            value=value[0]+""+value[1]
                            value=re.sub(r'[^\x00-\x7F]+', '', value)
                            
                     except:
                            value=""
                            
                     
                     StringParam="("+value+");"
                     

              method=method+StringParam



              Class_Methods=Class_Methods+method
                     


       Code= f"""

public abstract class {Name}_UML {Parent}  $


{Class_Atributes}
    
{Class_Methods}
      
?
              """
       Code=Code.replace("$","{")
       Code=Code.replace("?","}")

       return Code



def TokenizeValue(value):

       value=value.replace("\n","")

       DectectError(value,r'[^a-zA-Z0-9\s_+:=\{\},;\[\]]')

      
       CheckSyntax( value, r'^[+-]\s*[A-Za-z0-9]*:\s?[A-Za-z0-9]*\s*?(?:=\s*?\d+)?(?:\s*?\[\s*?\d*?\s*?\])?' )


       value=re.sub(r'[^\x00-\x7F]+', '',value)

       

       TokValue=value.split(":")

       Variable={}

       modifier={"+" :"public "             ,"-": "private " }

       for mod in modifier:

              if mod in TokValue[0]:

                     TokValue[0]=TokValue[0].replace(mod , "" )

                     Variable["mod"]=modifier[mod]
                     Variable["name"]=TokValue[0]   
                     break

       
       TokValue=TokValue[1]

       if "=" in TokValue:

               TokValue=TokValue.split("=")
               Variable["value"]=TokValue[1]

               TokValue=TokValue[0]


       if "[" in TokValue:

              TokValue=TokValue.split("[")
              Variable["array"]="["+TokValue[1]

              TokValue=TokValue[0]


       Variable["type"]=TokValue


       return Variable


       

              
def TokenizeMethod(method):

       DectectError(method,r'[^a-zA-Z0-9\s_+:=\{\}\(\),;\[\]]')

       method=method.replace("\n","")


       TokMethod=method.split(")")

       Method={ }

       #Extract return
       Method["return"]= TokMethod[1].replace(":","")

       TokMethod=TokMethod[0].split("(")

       modifier={"+" :"public "    ,"-": "private "}

       for mod in modifier:

              if mod in TokMethod[0]:

                     TokMethod[0]=TokMethod[0].replace(mod , "" )

                     Method["mod"]=modifier[mod]
                     Method["name"]=TokMethod[0]   
                     break


       TokMethod=TokMethod[1]

       Variables=[ ]

       if "," in TokMethod:

              TokMethod=TokMethod.split(",")

              for var in TokMethod:

                     var=var.split(":")

                     Variables.append(var[1]+" "+var[0]   )

       else:
              try:
                     var=TokMethod.split(":")
                     Variables.append(  (var[1],var[0] )  )
              except:
                     pass


       Method["var"]=Variables

       

       return Method


       
def ParseClassesFromDiagramm( Diagramm ):

       Blocks=Diagramm.blocks
       Arrows=Diagramm.arrows


       Classes={   }
       ErbArrow={ }
       Atributes= { }
       Methoden= { }
       

       #Sort blocks to methods and attributes
       for block in Blocks:

              Id=block.Attr["id"]
              value=block.Attr["value"]
              parent=block.Attr["parent"]
              Type=block.Attr["style"][0]

              if  Type=="swimlane":

                     DectectError(value,r'[^a-zA-Z0-9\s_]')

                     Classes[Id]=value
               
                     continue

              
              pattern = r'\b\w+\s*\([^()]*\s*\)\s*:\s*\w+'
              matches = re.findall(pattern, value)
              
              if  len(matches)>0 :

                     Methoden[Id]=(parent,     TokenizeMethod(value)   )
                     continue

              if Type=="text":

                     Atributes[Id]=(parent,   TokenizeValue(value)    )
                     continue
       #Sort arrows
       for arrow in Arrows:

              
              source=arrow.Attr["source"]
              target=arrow.Attr["target"]

              style=arrow.Attr["style"]
            
              if  "endArrow=block" in  style:
                     
                     ErbArrow[source]=target

                    

                            


       CodeClasses=""
       for key in Classes:

              Atributes_current=[]
              Methoden_current=[]
              
              
              Name_Class=Classes[key]
              Parent_Class=""
              

              for source in  ErbArrow:

                     if source==key:
                            Parent_Class=Classes[ ErbArrow[source]  ]
                            break




              for idx in Atributes:

                     parent=Atributes[idx][0]
                     value=Atributes[idx][1]

                     if parent==key:

                            Atributes_current.append(  value   )

              for idx in Methoden:

                     parent=Methoden[idx][0]
                     value=Methoden[idx][1]

                     if parent==key:

                            Methoden_current.append(  value   )


              CodeClasses=CodeClasses+BuildClass_Cs( Methoden_current , Atributes_current, Name_Class, Parent_Class )+"\n"

       return CodeClasses

              

       
def GenerateCode(Code,DiagrammName):

       File=open(DiagrammName,"w")

       Code="namespace "+DiagrammName.split(".")[0]+"{\n"+Code+"\n}"
       
       File.write(Code)
       File.close()
                


def GenerateCodeFromClassDiagramm(file_path,DiagrammName):

       Dia=ParseDiagramsFromXmlFile(file_path)
       Dia=Dia[DiagrammName]

       Code=ParseClassesFromDiagramm( Dia)

       GenerateCode(Code,DiagrammName)
       

       
                     
########Main############
                     
file_path =sys.argv[1]
DiagrammName=sys.argv[2]


GenerateCodeFromClassDiagramm(file_path,DiagrammName)






