import sys
import os





#Global Variables








Var_dic={}
VarSize_dic={}




#####



def FromatSrcCode( SrcCode ):
    
    S=[]
    Code=""""""

    for line in open(SrcCode,encoding="utf-16"):
        Code=Code+line


    Code=Code.replace('\t',' ')
    #Format text
    Code=Code.split("\n")
    n=Code.count("")
    for k in range(n):
        Code.remove("")

#Splitt "  " in seperate expressions
    for line in Code:
        line=line.split("  ")
        for k in line:
            S.append(k)

#Replace " "
    for k in range(len(S)):
        S[k]=S[k].replace(" ","")

        
    return S




def PreCompile_TransGeek(ln,Greek_Dic):

    for k in Greek_Dic:
        if k in ln:
            ln=ln.replace(k,Greek_Dic[k])
            
    return ln
    





def PreCompile_lib(S):

    PreLoad="""
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <stdio.h>
#include <fstream>
#include <cmath>
#include <complex>
#include<chrono>

using namespace std;
    """
    
    S.append(PreLoad)



def SetPreload(Ptyp,Includes_set):

    PreLoad="""
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <stdio.h>
#include <fstream>
#include <cmath>
#include <complex>
#include<chrono>

using namespace std;
    """
    IncludeBlock=""
    VarBlock=""
    Functions=""

    for k in Includes_set:
        IncludeBlock+="#include\""+k+"\"\n"

    


#Preload for the gpu
    
    if "gpu" in Ptyp:
        VarBlock+="//For the Gpu\n int threads,blocks;\n"
        Functions+=""" //Functions for the gpu support
 static __global__ void reducePairAdd (double *g_idata, double *g_odata,  int n)
{
    // set thread ID
     int tid = threadIdx.x;
     int idx = blockIdx.x * blockDim.x + threadIdx.x;

    // boundary check
    if(idx >= n) return;

    // in-place reduction in global memory
    for (int stride = blockDim.x / 2; stride > 0; stride /= 2)
    {
        if (tid < stride)
        {
            g_idata[idx] += g_idata[idx + stride];
        }

        __syncthreads();
    }

    // write result for this block to global mem
    if (tid == 0) g_odata[blockIdx.x] = g_idata[idx];
}


static __global__ void reducePairMul (double *g_idata, double *g_odata,  int n)
{
    // set thread ID
     int tid = threadIdx.x;
     int idx = blockIdx.x * blockDim.x + threadIdx.x;

    // boundary check
    if(idx >= n) return;

    // in-place reduction in global memory
    for (int stride = blockDim.x / 2; stride > 0; stride /= 2)
    {
        if (tid < stride)
        {
            g_idata[idx] =g_idata[idx] * g_idata[idx + stride];
        }

        __syncthreads();
    }

    // write result for this block to global mem
    if (tid == 0) g_odata[blockIdx.x] = g_idata[idx];
}

//#########################


"""

###########

        
    if"mpi" in Ptyp:
        IncludeBlock+="#include<mpi.h> \n"
        #VarBlock+="//For  Mpi calculations \n  int procid, Nproc;\n double hproc;\n"


#Xml part

    if"xml" in Ptyp:
        IncludeBlock+="\n #include \"tinyxml/tinyxml.h\"  \n"
        Functions+="""
//Function for the xml io:system

template <class T>
  static  void ReadXml(TiXmlDocument doc, T& a, const char* id) {
        doc.LoadFile();
        string b;
        TiXmlElement* Data= doc.RootElement();
        TiXmlElement* S = Data->FirstChildElement(id);
        b = S->Attribute("value");
        if (typeid(a) == typeid(int)) {
            a = std::stoi(b);
        }
        else if (typeid(a) == typeid(double)){
            a = std::stod(b);
    }

    }


    template <class T>
    static void WriteXml(TiXmlDocument doc, T& a, const char* id) {

       doc.LoadFile();
        TiXmlElement* Data = doc.RootElement();

        TiXmlElement* S = Data->FirstChildElement(id);

        if (S == NULL) {


            TiXmlElement* ele = new TiXmlElement(id);

            if (typeid(a) == typeid(double)) {
                ele->SetDoubleAttribute("value", a);
            }
            else {
                ele->SetAttribute("value", a);
            }


            Data->LinkEndChild(ele);
            


        }
        else {

            
            if (typeid(a) == typeid(double)) {
                S->SetDoubleAttribute("value", a);
            }
            if (typeid(a) == typeid(int)) {
                S->SetAttribute("value", a);
            }
           


        }

        
        
        doc.SaveFile();
         
    }

//########################


"""
######################

    if"python" in Ptyp:
        PVarBlock=""
        IncludeBlock+="#include <Python.h>\n"
        PVarBlock+=""" //Link to python
static PyObject*  Pyresult,*PyModule,*PyArgs,*PyFunc;

"""
        IncludeBlock+=PVarBlock+"\n"
        

    VarBlock+="""//For time measurment
std::chrono::time_point<std::chrono::system_clock> start, stop;
double diff;



"""
    PreLoad+=IncludeBlock+"\n"
    PreLoad+="struct   "+sys.argv[1]+"Init {\n"+VarBlock+"\n};\n"+sys.argv[1]+"Init "+sys.argv[1]+"Vars;\n"
    PreLoad+=Functions

    return PreLoad

    
def PreCompile_head(S,Ptyp,Includes_set):
    begin=SetPreload(Ptyp,Includes_set)

    
    
    begin=begin+"""

//Variables

static int Nth;
static int Nbl;



static char Dchar[256];

//Standard things in math


static  double mod(double x, double y) {
double s;
s = (int)x % (int)y;
return s; }

static void seed(int sed){

srand(sed);

}


static int rint(int a,int b){

int r=(rand() % b) + a;
return r;

}

static double rdouble(int a,int b){


double r=a + (double)(rand()) / ((double)(RAND_MAX/(b - a)));


return r;



}

const double pi = 3.1415926535897932384626433832795028841971;

template <class T>
   static void SetArgv(T &a, int k, char** argv) {


        if (typeid(a) == typeid(double)) {
            a = stod(argv[k]);
            
        }
        if (typeid(a) == typeid(int)) {
            a = stoi(argv[k]);
        }
}

    """

    S.append(begin)





def PreCompile_SetMakros_ForArrays(S,ln,Mark):
    
    if ("€" in ln) and (not ("->" in ln) and not("C[" in ln) and not("#" in ln) and not("init" in ln)):
        if ("|R(" in ln) or ("|N(" in ln) or ("|C(" in ln) or ("(" in ln):

            ln=ln.split("€")
            var=ln[0]
            
            if var in Mark:
                return
            ln=ln[1]
            Mark[var]=ln
            
            for k in range(len(ln)):
                if "(" in ln[k]:
                    n=k
                    
            ln=ln[n:len(ln)-1 ]
            ln=ln.split(",")
            n=len(ln)
            

            k=0
            define=""
            define1=""
            CompiledLine=""
            while(k<n-1):
                define=define+"i"+str(k)+","
                define1=define1+"[(int)(i"+str(k)+")]"
                k+=1
            define=define+"i"+str(n-1)
            define1=define1+"[(int)(i"+str(n-1)+")]"

            if"," in var:
                var=var.split(",")
                for k in var:
                    if"*" in k:
                        k=k.split("*")
                        k=k[0]
                    CompiledLine=CompiledLine+"#define "+k+"("+define+")"+" "+k+define1+"\n"
            else:
                if"*" in var:
                    var=var.split("*")
                    var=var[0]
                CompiledLine="#define "+var+"("+define+")"+" "+var+define1+"\n"
                    
            S.append(CompiledLine)




def PreCompile_SetFunctionHeads(S,FuncHeads,Ptyp,ln):
    
    if ("->" in ln) and not("send" in ln):
        #head
        ln=ln.split("->")
        if  "|R" in ln[1]:
            if("(" in ln[1]):
                prefix="double* "
            else:
                prefix="double "
                
        if  "|N" in ln[1]:
            if("(" in ln[1]):
                prefix="double* "
            else:
                prefix="double "
        if "|C" in ln[1]:
            prefix="complex<double>"
        if "()" in ln[1]:
            prefix="void "
        if"gpu" in ln[1]:
            prefix="__global__ void "


        
        ln=ln[0].split(":")
        if"gpu" in Ptyp:
            prehead="__host__ __device__  "
        else:
            prehead=""
        head=ln[0]
        #######
        
        ln=ln[1].split(",")
        Var_set=[]

        for k in ln:
            #k=k.split("€")
            #if "|R" in k[1]:
               # num="double "
            #elif"|N" in k[1]:
              #  num="int "
            #else:
              #  num=k[1]
            num="double "

            if"(" in k:
                var=k
                for j in range(len(var)):
                    if "(" in var[j]:
                        m=j
                        break
                defvar=var.split("(")[0]
                var=var[m+1:len(var)-1]
                var=var.split(";")
                count=len(var)

                if count==1:
                    stars="*"
                if count==2:
                    stars="**"
                if count==3:
                    stars="***"

                Var_set.append(num+stars+defvar)     
            else:
                Var_set.append(num+k)


        
        
        makros=""
        for k in range(len(ln)):
            #if"*" in ln[k]:
              #  var=ln[k].split("*")
                #var=var[1]
                #makros=makros+"#define "+var+"(i) "+var+"[i]\n"


 
            if "(" in ln[k]:
                var=ln[k]

                for j in range(len(var)):
                    if "(" in var[j]:
                        m=j
                        break
                var=var[m+1:len(var)-1]
                var=var.split(",")
                t=len(var)
                define=""
                define1=""
                p=0
                while(p<t-1):
                    define=define+"i"+str(p)+","
                    define1=define1+"[(int)(i"+str(p)+")]"
                    p+=1
                define=define+"i"+str(t-1)
                define1=define1+"[(int)(i"+str(t-1)+")]"
                if "&" in ln[k][0:m]:
                    start=1
                else:
                    start=0
                
                makros=makros+"#define "+ln[k][start:m]+"("+define+")"+" "+ln[k][start:m]+define1+"\n"

                          
        variables=""
        N=len(ln)

        for k in range(N):
            if"(" in ln[k]:
                ln[k]=ln[k].replace(';',',')
        
        for k in range(len(Var_set)-1):
            
            variables=variables+Var_set[k]+","
            
        variables=variables+Var_set[len(Var_set)-1]

        function=prehead+prefix+head+"("+variables+")"+";\n"

        if "libary" in Ptyp:
            FuncHeads.add(function)
            S.append("\n"+function)
        else:
            S.append("\n"+function)



def Compile_Functions(S,ln,H,F,mode):
    
    if (("->" in ln) or ("#" in ln) ) and  not("send" in ln) and not("recv" in ln)   :
        prehead=""

        if "->" in ln:
            ln=ln.split("->")
            if  ("|R" in ln[1]):
                
                if("(" in ln[1]):
                    prefix="double* "
                else:
                    prefix="double "
            if  "|N" in ln[1]:
                
                if("(" in ln[1]):
                    prefix="double* "
                else:
                    prefix="double "

            if "()" in ln[1]:
                prefix="void "
            if"gpu" in ln[1]:
                prefix="__global__ void "
            
            ln=ln[0].split(":")
            if"gpu" in mode:
                prehead="__host__ __device__  "
            else:
                prehead=""
            head=ln[0]
        
        else:
            ln=ln.split("#")
            prefix="void "
            ln=ln[1].split(":")
            head=ln[0]
            
            
        #######
        makros=""
        
        ln=ln[1].split(",")
        variables=""
        if  2>1 :
            
            Var_set=[]

            for k in ln:
                #k=k.split("€")
                makro1=""
                
                if not("C[" in k):
                    if "(" in k:
                        var=k
                        if"&" in var:
                            var=var.replace("&","")
                        makro1+="#define "+var+" "

                        var=var.split("(")
                        name=var[0]
                        makro1+=name

                        
                            
                    
                        var=var[1].replace(")","")
                        var=var.split(",")
                        for b in var:
                            makro1+="[(int)("+b+")]"
                        makro1+="\n"
                        makros+=makro1

                        

                    if ''==k:
                        num=""
                        temp=""
                    else:
                        num="double "
                        temp=""
                        
                    
                
                
                
                
                
                    #if "|R" in k[1]:
                      #  num="double "
                    #elif"|N" in k[1]:
                      #  num="int "
                    #else:
                       # num=k[1]+" "
                    
                    if"(" in k:
                        var=k
                        for j in range(len(var)):
                            if "(" in var[j]:
                                m=j
                                break
                        defvar=var.split("(")[0]
                        var=var[m+1:len(var)-1]
                        var=var.split(";")
                        count=len(var)

                        if count==1:
                            stars="*"
                        if count==2:
                            stars="**"
                        if count==3:
                            stars="***"

                        Var_set.append(num+stars+defvar)     
                    else:
                        Var_set.append(num+k)
                        
                else:
                    num="double "
                    if "(" in k[0]:
                        name=k[0].split("(")[0]
                        num+="*"
                    else:
                        name=k[0]
                        
                    varnum=k[1][2:len(k[1])-1]

                    varnum=varnum.split(",")
                    
                    
                    fvariables=""
                    
                    for j in range(len(varnum)):
                        star=""
                        numt="double "

                        #if "|R" in varnum[j]:
                          #  numt="double "
                        #elif"|N" in varnum[j]:
                          #  numt="int "

                          
                        
                        if "(" in varnum[j]:
                            star="*"

                        fvariables+=numt+star

                        if  j<len(varnum)-1:
                            fvariables+=","


                    Var_set.append(num+name+"("+fvariables+")")
                
                




                   




            variables=""
            N=len(ln)

            for k in range(N):
                if"(" in ln[k]:
                    ln[k]=ln[k].replace(';',',')
        
            for k in range(len(Var_set)-1):
            
                variables=variables+Var_set[k]+","
            
            variables=variables+Var_set[len(Var_set)-1]


        
        
        function=temp+prehead+prefix+head+"("+variables+")"+"\n"

        if variables=="":
            H.append(prehead+head+"("+variables+")")
        else:
            F.add(prehead+prefix+head+"("+variables+")"+";\n")

        S.append(function)




def Compile_Brackets(S,H,ln):
    
    
        
    
        

    if"*;" in ln:
        S.append("\n}}\n")

    #The brackets
    if "{" in ln:
        CompiledCode.append("{\n")

    if( "}" in ln)  :
        CompiledCode.append("\n}\n")
    if ";" in ln:
        if not("=" in ln) and not("->" in ln) and not("*" in ln) and not("#" in ln):
            n=ln.count(";")
            brack=""
            k=0
            while(k<n):
                brack+="}\n"
                k+=1
            S.append(brack)
               
            if "mpi" in ln:
                S.append("\n}\n MPI_Finalize();\n")
            


def Precompile_DefineNumbers(S,ln,Variable_dic,mode):
    if ("€"  in ln) and not("(" in ln) and not("->" in ln)and not("#" in ln) and not("init" in ln):
        if("|R" in ln) or ("|N" in ln) or ("|C" in ln)or ("|B" in ln)or ("€" in ln):
            CompiledExp=""
            ln= ln.split("€")
            
            if  "|R" in ln[1]:
                num="double"
            elif  "|N" in ln[1]:
                num="double"
            elif "|C" in ln[1]:
                num="complex<double>"
            elif"|B" in ln[1]:
                num="bool"
            else:
                num=ln[1]
                

            if "," in ln[0]:
                var=ln[0].split(",")
                for k in var:
                    if("*" in k) and ("gpu" in mode):
                        k=k.split("*")
                        k=k[0]
                        CompiledExp=CompiledExp+num+" "+k+",*dev_"+k+";\n"
                        CompiledExp=CompiledExp+"int size_"+k+"=sizeof("+num+");\n"
                        CompiledExp=CompiledExp+"cudaMalloc( (void**)&dev_"+k+",size_"+k+");\n"
                        if "python" in mode:
                            CompiledExp=CompiledExp+"PyObject*"+" "+"py_"+k.split("*")[0]+";\n"
                    elif("*" in k):
                        k=k.split("*")[0]
                        CompiledExp=CompiledExp+num+" "+k+";\n"
                        CompiledExp=CompiledExp+"PyObject*"+" "+"py_"+k+";\n"
                    else:
                        CompiledExp=CompiledExp+num+" "+k+";\n"
                        
                        
                    Variable_dic[k]=num
                    VarSize_dic[k]="1"
                
            else:
                if("*" in ln[0]) and ("gpu" in mode):
                    var=ln[0].split("*")
                    var=var[0]
                    CompiledExp=num+" "+var+",*dev_"+var+";\n"
                    CompiledExp=CompiledExp+"int size_"+var+"=sizeof("+num+");\n"
                    CompiledExp=CompiledExp+"cudaMalloc( (void**)&dev_"+var+",size_"+var+");\n"
                    if "python" in mode:
                        CompiledExp+="PyObject*"+" "+"py_"+var.split("*")[0]+";\n"
                elif("*" in ln[0]):
                    var=ln[0].split("*")
                    var=var[0]
                    var=var.split("*")[0]
                    CompiledExp=num+" "+var+";\n"
                    CompiledExp+="PyObject*"+" "+"py_"+var+";\n"
                    
                    
                else:
                    CompiledExp=num+" "+ln[0]+";\n"
                    Variable_dic[ln[0]]=num
                    VarSize_dic[ln[0]]="1"
                
            S.append(CompiledExp)
            
            return

        
    




        
def Compile_DefineVariables(S,ln,mode):
    if ("€" in ln) and not("->" in ln) and not("#" in ln) and not("init" in ln):
        if ("|R(" in ln) or ("|N(" in ln) or ("|C(" in ln) or ("(" in ln):
            ln=ln.split("€")
            var=ln[0]
            ln=ln[1]
            CompiledLine=""
            
            
            
            if"|R" in ln[0:2]:
                num="double"
            elif"|N" in ln[0:2]:
                num="double"
            elif "|C" in ln[0:2]:
                num="complex<double>"
            else:
                num=ln[0:2]

            
            for k in range(len(ln)):
                if "(" in ln[k]:
                    n=k     
            ln=ln[n+1:len(ln)-1 ]
            lenght=ln
            ln=ln.split(",")
            
            n=len(ln)
            k=0
            define=""
            define0=""
            stars=""
            while(k<n-1):
                define=define+ln[k]+","
                stars=stars+"*"
                define0=define0+"*"
                k+=1
            define0=define0+"[(int)("+ln[n-1]+")]"
            define=define+ln[n-1]
            stars=stars+"*"

            Init=""
            if(n>1) and not ("," in var):

                if(n==2):
                    Init=Init+"for(int i=0;i<"+ln[0]+";i++){"+var+"[i]=new "+num+"[(int)("+ln[0]+")];}\n"
                if(n==3):
                    Init=Init+"for(int i=0;i<"+ln[0]+";i++){"+var+"[i]=new "+num+"*[(int)("+ln[0]+")];\n"
                    Init=Init+"for(int j=0;j<"+ln[0]+";j++){"+var+"[i][j]=new "+num+"[(int)("+ln[1]+")];}}\n"
            
                

            
            

            if"," in var:
                var=var.split(",")
                for k in var:
                    if("*" in k) and ("gpu" in mode):
                        k=k.split("*")
                        k=k[0]
                        define_gpu=define.split(",")
                        Nv=define_gpu[0]
                        for k in range(len(define_gpu)-1):
                            Nv=Nv+"*"+define_gpu[k+1]
                        CompiledLine=CompiledLine+num+"* "+k+";\n"
                        CompiledLine=CompiledLine+k+"=new "+num+" [(int)("+Nv+")];"
                        CompiledLine=CompiledLine+num+" *dev_"+k+";\n"
                        CompiledLine=CompiledLine+"int size_"+k+"="+Nv+"*sizeof("+num+");\n"
                        CompiledLine=CompiledLine+"cudaMalloc( (void**)&dev_"+k+",size_"+k+");\n"
                        if "python" in mode:
                            CompiledLine+="PyObject *"+" "+"py_"+k+"= PyList_New("+Nv+");\n"
                    
                    else:
                        Init=""
                        if(n>1) :
                            if(n==2):
                                Init=Init+"for(int i=0;i<"+ln[0]+";i++){"+k+"[i]=new "+num+"[(int)("+ln[0]+")];}\n"
                            if(n==3):
                                Init=Init+"for(int i=0;i<"+ln[0]+";i++){"+k+"[i]=new "+num+"*[(int)("+ln[0]+")];\n"
                                Init=Init+"for(int j=0;j<"+ln[0]+";j++){"+k+"[i][j]=new "+num+"[(int)("+ln[1]+")];}}\n"
            
                        if ("*" in k) and ("python" in mode):
                            k=k.split("*")[0]
                            CompiledLine=CompiledLine+num+stars+" "+k+"=new "+num+define0+";\n"+Init
                            CompiledLine+="PyObject *"+" "+"py_"+k+"= PyList_New("+lenght+");\n"
                        else:
                            CompiledLine+=num+stars+" "+k+"=new "+num+define0+";\n"+Init
                        
            else:
                if("*" in var) and ("gpu" in mode):
                    var=var.split("*")
                    var=var[0]
                    k=var
                    define_gpu=define.split(",")
                    Nv=define_gpu[0]
                    for k in range(len(define_gpu)-1):
                        Nv=Nv+"*"+define_gpu[k+1]
                    CompiledLine=CompiledLine+num+"* "+k+";\n"
                    CompiledLine=CompiledLine+k+"="+"new "+num+" [(int)("+Nv+")];\n"
                    CompiledLine=CompiledLine+num+" *dev_"+k+";\n"
                    CompiledLine=CompiledLine+"int size_"+var+"="+Nv+"*sizeof("+num+");\n"
                    CompiledLine=CompiledLine+"cudaMalloc( (void**)&dev_"+var+",size_"+var+");\n"
                    if "python" in mode:
                        CompiledLine+="PyObject *"+" "+"py_"+var+"= PyList_New("+Nv+");\n"
                    
                else:
                    if ("*" in var) and ("python" in mode):
                        var=var.split("*")[0]
                        CompiledLine=num+stars+" "+var+"=new "+num+define0+";\n"+Init
                        CompiledLine+="PyObject *"+" "+"py_"+var+"= PyList_New("+lenght+");\n"
                    else:
                        CompiledLine=num+stars+" "+var+"=new "+num+define0+";\n"+Init
                        
                    
                
            S.append(CompiledLine)
            
        
Gpu_var=[ ]


def Compile_StandardTasks(S,Files_dic,Variable_dic,ln,mode):

    Pname=sys.argv[1]+"Vars."

    if("*:" in ln):
        ln=ln.split("*:")
        if"..." in ln[1]:
            var=ln[1].split("...")
            upper=var[0]
            upper=var[0].split("=")
            idx=upper[0]
            upper=upper[1]
            upper=upper.replace(",","")
            limit=var[1]
            limit=limit.replace(",","")
            CompiledLine="for(int "+idx+"="+upper+";"+idx+"<="+limit+";"+idx+"++){\n"
            CompiledLine+="if("+"id=="+idx+"){\n"
        else:
            nr=ln[1]
            CompiledLine="if("+"id=="+nr+"){\n"
            
        S.append(CompiledLine)
        
        
        

    
    
    
    if("::" in ln) and not (sys.argv[1]+"Vars" in ln):
        ln=ln.split("::")
        if "(" in ln[1]:
            CompiledExp=ln[1]+";\n"
        else:
            CompiledExp=ln[1]+":\n"
            
        S.append(CompiledExp)


    
            
    
    if (":" in ln) and not ("::" in ln) and not("#" in ln) and not("*:" in ln):
        
        ln=ln.split(":")

        if"goto" in ln[0]:
            
            CompiledExp="goto "+ln[1]+";\n"

            S.append(CompiledExp)
            

        if ln[0] in Files_dic:
            
            
            mode=Files_dic[ln[0]]
            if "in" in mode:
                expr=ln[0]+">>"+ln[1]+";\n"
            else:
                expr=ln[0]+"<<"+ln[1]+";\n"
                
            S.append(expr)

        if"clock" in ln:
            mod=ln[1]
            if"start" in mod:
                Compile="\n "+Pname+"start=std::chrono::high_resolution_clock::now();\n"
            if"stop" in mod:
                if "ms" in mod:
                    unit="milliseconds"
                elif "µs" in mod:
                    unit="microseconds"
                elif"ns" in mod:
                    unit="nanoseconds"
                else:
                    unit="seconds"
                
                #if"s" in mod:
                    #unit="seconds"
                    
                Compile= "\n "+Pname+"stop=std::chrono::high_resolution_clock::now();\n"
                Compile=Compile+"\n "+Pname+"diff=std::chrono::duration_cast<std::chrono::"+unit+">("+Pname+"stop"+ "-"+Pname+"start).count();\n"
            S.append(Compile)
            return
            
            
                

        if (("call" in ln[0])or ("py" in ln[0])) and not("gcall" in ln[0]) and not("=" in ln[0])and not("pyinit" in ln[0]) :
            var=ln[1]
            var=var.split("(")
            name=var[0]

            
            
            if name in Files_dic:

                if ".py" in Files_dic[name]:
                    exp=Files_dic[name]
                    exp=exp.split("/")
                    func=exp[1]
                    module=exp[0]
                    func=func.replace(".py","")
                    
                    CompiledExp="Py_Initialize();\n"+"PyModule=PyImport_Import(PyString_FromString((char*)\""+module+"\"));\n"
                    CompiledExp+="PyFunc=PyObject_GetAttrString("+"PyModule,(char*)\""+func+"\");\n"

                    pyvar=var[1]
                    pyvar=pyvar[0:len(pyvar)-1]
                    pyvar=pyvar.split(",")
                    nvar=len(pyvar)

                    for k in Var_dic:
                        if k in pyvar:
                            modi=Var_dic[k]
                            if "double" in modi:
                                num="PyFloat_FromDouble"
                            if"int" in modi:
                                num="PyInt_FromLong"
                            
                            if"*" in modi: 
                                CompiledExp+="for (int i = 0; i < PyList_Size("+"py_"+k+"); ++i) {"+"PyList_SetItem("+"py_"+k+",i,"+num+"("+k+"(i)"+"));}\n"
                            else:
                                CompiledExp+="py_"+k+"="+num+"("+k+");\n"
                            
                            

                    
                    variables=""
                    for a in range( len(pyvar)-1):
                        variables+="py_"+pyvar[a]+","
                    variables+="py_"+pyvar[len(pyvar)-1]
                        
                    CompiledExp+="PyArgs=PyTuple_Pack("+str(nvar)+","+variables+");\n"
                    CompiledExp+="Pyresult = PyObject_CallObject(  PyFunc ,PyArgs);\n Py_Finalize();\n"
                            
                    S.append(CompiledExp)
                    return
                    
                    
                    
                    
                    

            

                
                index=var[1]
                index=index[0:len(index)-1]
                var_index=index.split(",")
                
                prefix=""
                for k in var_index:
                    typ=Variable_dic[k]

                    if "int" in typ:
                        prefix=prefix+" %d"
                    else:
                        prefix=prefix+" %f"
                        

                    
                    

                if len(index)>0:
                    CompiledExp="\n sprintf(Dchar"+ ","+"\""+Files_dic[name]+prefix +"\""+","+index+");\n"
                    CompiledExp=CompiledExp+"system(Dchar);\n"
                    
                else:
                    CompiledExp="system("+"\""+Files_dic[name]+"\""+");\n"


                S.append(CompiledExp)
                
            else:
                
                CompiledExp=ln[1]+";\n"
                S.append(CompiledExp)
        
            

        if"save" in ln[0]:
            ln=ln[1].split("[")
            short=ln[1]
            short=short[0:len(short)-1]
            var=ln[0]
            name=ln[0]
            if "(" in var:
                var=var.split("(")
                name=var[0]

                index=var[1]
                index=index[0: len(index)-1]
                
                prefix=""
                for k in range(len(index.split(","))):
                    prefix=prefix+"%d"
                    
                expr="\n sprintf(Dchar"+ ","+"\""+name+prefix +"\""+","+index+");\n"
                expr=expr+"WriteXml("+"file_"+short+","+ln[0]+","+"Dchar"+");\n"
 
            else:
                expr=""
                expr="WriteXml("+"file_"+short+","+ln[0]+","+" \""+name+"\""+");\n"
                
            S.append(expr)


        if"open" in ln[0]:
        
            if"r" in ln[0]:
                mode="in"
            if"w" in ln[0]:
                mode="out"
            if"app" in ln[0]:
                mode="app"

            ln=ln[1].split("[")
            name=ln[0]
            short=ln[1][0:len(ln[1])-1]

            expr="fstream "+name+";\n"
            expr=expr+name+".open("+"\""+Files_dic[short]+"\""+","+"ios::"+mode+");\n"
            Files_dic[name]=mode
            S.append(expr)

        if"close" in ln[0]:
            if ln[1] in Files_dic:
                expr=ln[1]+".close();\n"
                S.append(expr)


#Gpu part

        if"gcall" in ln[0]:
            
            if"_" in ln[0]:
                S.append(ln[1]+";\n")
                return

            ln=ln[1].split("(")
            var=ln[1]
            var=var.replace(")","")
            var=var.split(",")
            variables=""

            for k in range(len(var)):
                w=Var_dic[var[k]]
                
                
                if"*" in w:
                    variables+="dev_"+var[k]
                else:
                    variables+=var[k]
                    
                if k<(len(var)-1):
                    variables+=","

            CompileExp=ln[0]+"("+variables+");\n"
            S.append(CompileExp)

            

            
                
                
            
            

        if"gpu" in ln[0]:
            CompLine=""

            if("|R" in ln[0]) or ("|N" in ln[0]):
                var=ln[1]
                if"|R" in ln[0]:
                    num="double"
                if"|N" in ln[0]:
                    num="int"
                
                
            if "in" in ln[0]:
                var=ln[1].split(",")
                num="double "
                
                for k in var:

                    if "(" in k:
                        limit=k.split("(")[1]
                        k=k.split("(")[0]
                        limit=limit.split(")")[0]
                        CompLine+=num+"*dev_"+k+";\n"
                        CompLine+="int size_"+k+"=sizeof(double)*"+limit+";\n"
                        CompLine+="cudaMalloc( (void**)&dev_"+k+",size_"+k+");\n"
                    
                    CompLine=CompLine+"cudaMemcpy("+"dev_"+k+","+k+",size_"+k+",cudaMemcpyHostToDevice);\n"

                    Gpu_var.append(k)
                
                S.append(CompLine)
                    
            if"out" in ln[0]:
                var=ln[1].split(",")

                if not("()" in var):
                    for k in var:
                        CompLine=CompLine+"cudaMemcpy("+k+",dev_"+k+",size_"+k+",cudaMemcpyDeviceToHost);\n"
                    

                for k in Gpu_var:
                    CompLine=CompLine+"cudaFree(dev_"+k+");\n"

                del Gpu_var[:]
                S.append(CompLine)
                
            if"read" in ln[0]:
                var=ln[1].split(",")

                if not("()" in var):
                    for k in var:
                        CompLine=CompLine+"cudaMemcpy("+k+",dev_"+k+",size_"+k+",cudaMemcpyDeviceToHost);\n"
                        
                    S.append(CompLine)

                

        if"init" in ln[0]:
            #print(ln[1])
            var=ln[1]
            var=var.split("€")
            if "|R" in var[1]:
                num="double "
            elif "|N" in var[1]:
                num="int "
            else:
                num=var[1]
            
            
            if "(" in var[1]:
                varm=var[1]
                varm=varm.split("(")
                limit=varm[1][0:len(varm[1])-1]
                CompLine=var[0]+"=new "+num+"["+limit+"];\n"
                
            else:
                CompLine=var[0]+"=("+num+")"+"1;\n"


            S.append(CompLine)
                
                
            
            #ln[1]=ln[1].split("(")
            #var=ln[1][0]
            #size=ln[1][1]
            #size=size.replace(")","")
            #num=Var_dic[var]
            #Var_dic[var]=num+"*"
            #num1=num.replace("*","")
            #CompLine=num+" dev_"+var+";\n"
            #CompLine+="int size_"+var+"="+size+"*"+"sizeof("+num1+");\n"
            #CompLine+="cudaMalloc( (void**)"+"&dev_"+var+",size_"+var+");\n"
            #S.append(CompLine)
        if"pyinit" in ln[0]:
            CompLine="PyObject* py_"+ln[1]+";\n"
            S.append(CompLine)
            
            
                
        if("kernel" in ln[0]):

            if not("_" in ln[0]):
                modif="dev_"
                head=ln[0]
            else:
                modif=""
                head=ln[0].split("_")[1]
            
            var=ln[1].split(",")
            head=head.replace("(","")
            head=head.replace(")","")
            variables=""

            if mode:
                
                for k in range(len(var)-1):
                    variables+=Var_dic[var[k]]+" "+var[k]+","
                variables+=Var_dic[var[len(var)-1]]+" "+var[len(var)-1]

                CompLine="__global__ void "+head+"("+variables+"){{\n"
                CompLine+="int id= blockIdx.x * blockDim.x + threadIdx.x;\n"
                
                
            if not mode:
                
                for k in range(len(var)):
                    w=Var_dic[var[k]]
                    if"*" in w:
                        variables+=modif+var[k]
                    else:
                        variables+=var[k]
                    if k<(len(var)-1):
                        variables+=","
                        
                CompLine=head+"<<<Nbl,"+"Nth"+">>>("+variables+");\n"
                
            S.append(CompLine)

        if "block" in ln[0]:
            if"..." in ln[1]:
                var=ln[1].split("...")
                upper=var[0]
                upper=var[0].split("=")
                idx=upper[0]
                upper=upper[1]
                upper=upper.replace(",","")
                limit=var[1]
                limit=limit.replace(",","")
                CompiledLine="for(int "+idx+"="+upper+";"+idx+"<="+limit+";"+idx+"++){\n"
                CompiledLine+="if("+"threadIdx.x=="+idx+"){\n"
            else:
                nr=ln[1]
                CompiledLine="if("+"blockIdx.x=="+nr+"){\n"
            S.append(CompiledLine)
            
        if "thread" in ln[0]:
            if"..." in ln[1]:
                var=ln[1].split("...")
                upper=var[0]
                upper=var[0].split("=")
                idx=upper[0]
                upper=upper[1]
                upper=upper.replace(",","")
                limit=var[1]
                limit=limit.replace(",","")
                CompiledLine="for(int "+idx+"="+upper+";"+idx+"<="+limit+";"+idx+"++){\n"
                CompiledLine+="if("+"threadIdx.x=="+idx+"){\n"
            else:
                nr=ln[1]
                CompiledLine="if("+"threadIdx.x=="+nr+"){\n"
            S.append(CompiledLine)
        
                
            

        
            
            
            
                
            
            #for k in 
            

            
            
            #CompLine=head+"<<<"+Pname+"blocks,"+Pname+"threads"+">>>("+variables+");\n"
            #S.append(CompLine)

            
                
                    
            
            
            

            
##########           

    
            
             
        
        #For Mpi

        

        if("mpi" in ln[0]):

            if("open" in ln[1]):
                CompiledExp="MPI::Init();\n"
                CompiledExp+="int Np=MPI::COMM_WORLD.Get_size();\n"
                CompiledExp+="int id=MPI::COMM_WORLD.Get_rank();\n"
                S.append(CompiledExp)
            if("close" in ln[1]):
                CompiledExp="MPI::Finalize();\n"
                S.append(CompiledExp)
                
        if("node" in ln[0]):
            if"..." in ln[1]:
                var=ln[1].split("...")
                upper=var[0]
                upper=var[0].split("=")
                idx=upper[0]
                upper=upper[1]
                upper=upper.replace(",","")
                limit=var[1]
                limit=limit.replace(",","")
                CompiledExp="for(int "+idx+";"+idx+"<="+limit+";"+idx+"++){\n"
                CompiledExp+="if(id=="+idx+"){\n"
            else:
                num=ln[1]
                CompiledExp="if(id=="+num+"){\n"
            S.append(CompiledExp)
            
            
        if("send" in ln[0]) or ("recv" in ln[0]) :
            tag=ln[0].split("(")
            tag=tag[1]
            tag=tag.replace(")","")
            if "->" in ln[1]:
                ln=ln[1].split("->")
                prefix="MPI_Send"
            if "<-" in ln[1]:
                ln=ln[1].split("<-")
                prefix="MPI_Recv"
            
            var=ln[0]
            dest=ln[1]
            CompiledExp=""
            if"," in var:
                var=var.split(",")
                z=0
                for k in var:
                    leng=VarSize_dic[k]
                    num=Var_dic[k]
                    if "double" in num:
                        num="MPI_DOUBLE"
                    if"int" in num:
                        num="MPI_INT"
                        
                    CompiledExp+=prefix+"(&"+k+","+leng+","+num+","+dest+","+tag+str(z)+",MPI_COMM_WORLD"
                    z+=1
                    if "Recv" in prefix:
                        CompiledExp+=",MPI_STATUS_IGNORE);\n"
                    else:
                        CompiledExp+=");\n"
                        

                        
            else:
                leng=VarSize_dic[var]
                num=Var_dic[var]
                if "double" in num:
                    num="MPI_DOUBLE"
                if"int" in num:
                    num="MPI_INT"
                CompiledExp+=prefix+"(&"+var+","+leng+","+num+","+dest+","+tag+",MPI_COMM_WORLD"
                if "Recv" in prefix:
                    CompiledExp+=",MPI_STATUS_IGNORE);\n"
                else:
                    CompiledExp+=");\n"
                    
            S.append(CompiledExp)
                
                    
                
                
                
            
        

        if ("out" in ln[0]) and not ("gpu" in ln[0]):
            CompiledExp="cout<<"+ln[1]+";"+"\n"
            S.append(CompiledExp)

        if "return" in ln[0]:
            CompiledExp="return "+ln[1]+";\n"
            S.append(CompiledExp)




def Precompile_Import(S,Files_dic,ln):

    if (":" in ln) and not ("->" in ln):
        
        ln=ln.split(":")

        if "]" in ln[0]:
            file=ln[1]
            short=ln[0]
            short=short[1:len(short)-1]
            
            if ".xml" in file:
                CompileImport="TiXmlDocument "+"file_"+short+"("+"\""+file+"\""+");\n"
                S.append(CompileImport)

            if ".exe" in file:
                Files_dic[short]=file
            if".txt" in file:
                Files_dic[short]=file
            if".linux" in file:
                file=file.split(".")
                file=file[0]
                Files_dic[short]="./"+file
            if".py" in file:
                Files_dic[short]=file
                

            if".h" in file:
                return
                
                
                
                
            

        

def Compile_Import(S,ln):

    if "[" in ln and not (":" in ln):
        
        ln=ln.split("[")
        short=ln[1]
        short=short[0:len(short)-1]
        
        var=ln[0]
        name=ln[0]

        if"arg" in short:
            number=short[len(short)-1]
            expr="SetArgv("+var+","+number+","+"_argv"+");\n"
            S.append(expr)
            return


        
        if "(" in var:
            
    
            var=var.split("(")
            name=var[0]

            index=var[1]
            index=index[0: len(index)-1]

            

            prefix=""
            for k in range(len(index.split(","))):
                prefix=prefix+"%d"
                
            
            expr="\n sprintf(Dchar"+ ","+"\""+name+prefix +"\""+","+index+");\n"
            expr=expr+"ReadXml("+"file_"+short+","+ln[0]+","+"Dchar"+");\n"
            
        else:
            expr="ReadXml("+"file_"+short+","+ln[0]+","+"\""+name+"\""+");\n"
            
        S.append(expr)
          
        





def Compile_expressions(S,ln,mode):
            
    if ("="  in ln) or ("<" in ln) or (">" in ln) or ("||" in ln) or ("&&" in ln) or ("!=" in ln) or ("Σ" in ln) or ("Π" in ln):
        
    

#Sum
        if("<<" in ln) or (">>" in ln) or ("<<<" in ln) or (">>>" in ln) :
            return

        if("send" in ln) or ("recv" in ln)or ("thread" in ln) or ("block" in ln)or ("*:" in ln):
            return
        

    #Gpu operator
        if ("Σ*" in ln) or ("Π*" in ln):
            
            if "Π*" in ln:
                sym="Π*"
                head="reducePairMul"
                ope="*"
                start="=1.0;\n"
            if "Σ*" in ln:
                sym="Σ*"
                head="reducePairAdd"
                ope="+"
                start="=0.0;\n"

            ln=ln.split("="+sym)
            var=ln[1]
            runvar=ln[0]
            var=var[1:len(var)-1]
            var=var.split(",")
            limit=var[2]
            var=var[0:2]
            define=""
            for k in var:
                define=define+"dev_"+k+","
            Pname=sys.argv[1]+"Vars."
            CompileExp=head+"<<<"+"Nbl,"+"Nth>>>"+"("+define+limit+");\n"
            CompileExp+="cudaMemcpy("+var[1]+",dev_"+var[1]+",size_"+var[1]+",cudaMemcpyDeviceToHost);\n"
            CompileExp+=runvar+start
            CompileExp+="for(int i=0;i<"+"Nbl;i++){\n"+runvar+"="+runvar+ope+var[1]+"[i]"+";"+"\n}\n"
            S.append(CompileExp)
            return
################################


            
        if ("Σ" in ln) or ("Π" in ln):
            

            if "Π" in ln:
                sym="Π"
                oper="*"
                start="1.0"
            if "Σ" in ln:
                sym="Σ"
                oper="+"
                start="0.0"
            
            
            ln=ln.split(sym)
            var=ln[0]
            var=var.split("=")
            var=var[0]
            ln=ln[1:]
            
            n=len(ln)

            CompiledLine=var+"="+start+";\n"

            Brackets=[]
            for k in range(n-1):
                
                
                s=ln[k]
                s=s[1:len(s)-1]
                s=s.split(",")
                loopvar=s[0]
                init=s[1]
                limit=s[2]
                
                CompiledLine=CompiledLine+"\n for( int "+loopvar+"="+init+";"+loopvar+"<="+limit+";"+loopvar+"++){\n"
                if len(s)>3:
                    logic=s[3]
                    CompiledLine=CompiledLine+"if("+logic+"){\n"
                    Brackets.append("}\n}\n")
                else:
                    Brackets.append("}\n")
                    
                
            
            ln=ln[n-1]
            for k in range(len(ln)):
                if ")" in ln[k]:
                    m=k
                    break
                    
            s=ln[1:m]
            s=s.split(",")
            
            loopvar=s[0]
            init=s[1]
            limit=s[2]
                
            expr=ln[m+1:]
            
            CompiledLine=CompiledLine+"\n for( int "+loopvar+"="+init+";"+loopvar+"<="+limit+";"+loopvar+"++){\n\n"
            if len(s)>3:
                logic=s[3]
                CompiledLine=CompiledLine+"if("+logic+"){\n"
                Brackets.append("}\n}\n")
            else:
                Brackets.append("}\n")
            CompiledLine=CompiledLine+var+"="+var+oper+expr+";\n\n"
            
            for k in Brackets:
                CompiledLine=CompiledLine+k
                
            S.append(CompiledLine)
            return
            
            
#############      
            
            
            
            

### Für den FOR loop
        if ("..." in ln) and not("mpi" in ln) and not("*=" in ln) and not("node" in ln) and not("thread" in ln) and not("block" in ln):
            ln=ln.split("=")
            CompiledExp=""
            
            var=ln[0]

            ln=ln[1].split(",")
            init=ln[0]
            limit=ln[2]

            if "," in var:
                var=var.split(",")
                for k in var:
                    CompiledExp=CompiledExp+"\n for( int "+k+"="+init+";"+k+"<="+limit+";"+k+"++){\n"
            else:
                CompiledExp="\n for( int "+var+"="+init+";"+var+"<="+limit+";"+var+"++){\n"
                
            S.append(CompiledExp)
            return

        elif ("..." in ln) and ("mpi" in ln):
            ln=ln.split(":")
            ln=ln[1]
            CompiledExp=""
            ln=ln.split("=")
            
            #Mpi init
            CompiledExp=CompiledExp+"MPI_Init(&argc,&argv);\n"
            CompiledExp=CompiledExp+"MPI_Comm_size(MPI_COMM_WORLD, &Nproc);\n"+"MPI_Comm_rank(MPI_COMM_WORLD, &procid);\n"
            ########

            var=ln[0]
            ln=ln[1].split(",")
            init=ln[0]
            limit=ln[2]

            CompiledExp=CompiledExp+"hproc="+"("+limit+"-"+init+"+1)"+"/Nproc;\n"

            
            
            CompiledExp=CompiledExp+"\n for( int "+var+"=procid*hproc"+";"+var+"<=(procid+1)*hproc-1"+";"+var+"++){\n"
            S.append(CompiledExp)
            return
            

        

###################
        
#Expression
          
        elif ("=" in ln) and not("node" in ln):

            if "py:" in ln:
                
                ln=ln.split("=")
                outvar=ln[0]
                ln=ln[1].split(":")
                var=ln[1]
                var=var.split("(")
                name=var[0]

                exp=Files_dic[name]
                exp=exp.split("/")
                func=exp[1]
                module=exp[0]
                func=func.replace(".py","")
                CompiledExp="Py_Initialize();\n"+"PyModule=PyImport_Import(PyString_FromString((char*)\""+module+"\"));\n"
                CompiledExp+="PyFunc=PyObject_GetAttrString("+"PyModule,(char*)\""+func+"\");\n"
                pyvar=var[1]
                pyvar=pyvar[0:len(pyvar)-1]
                pyvar=pyvar.split(",")
                nvar=len(pyvar)
                for k in Var_dic:
                    if k in pyvar:
                        modi=Var_dic[k]
                        if "double" in modi:
                            num="PyFloat_FromDouble"
                        if"int" in modi:
                            num="PyInt_FromLong"
                        if"*" in modi:
                            CompiledExp+="for (int i = 0; i < PyList_Size("+"py_"+k+"); ++i) {"+"PyList_SetItem("+"py_"+k+",i,"+num+"("+k+"(i)"+"));}\n"
                        else:
                            CompiledExp+="py_"+k+"="+num+"("+k+");\n"
                pyvar=var[1]
                pyvar=pyvar[0:len(pyvar)-1]
                pyvar=pyvar.split(",")
                nvar=len(pyvar)
                variables=""
                for a in range( len(pyvar)-1):
                    variables+="py_"+pyvar[a]+","
                variables+="py_"+pyvar[len(pyvar)-1]
                        
                CompiledExp+="PyArgs=PyTuple_Pack("+str(nvar)+","+variables+");\n"
                CompiledExp+="Pyresult = PyObject_CallObject(  PyFunc ,PyArgs);\n"

                modi=Var_dic[outvar]
                if "double" in modi:
                    num="PyFloat_AsDouble"
                if"int" in modi:
                    num="PyInt_AsLong" 
                    

                if "*" in Var_dic[outvar]:
                        
                    CompiledExp+="for (int i = 0; i < PyList_Size(Pyresult); ++i){\n"+outvar+"(i)="+num+"(PyList_GetItem(Pyresult, i));\n"
                else:
                    CompiledExp+=outvar+"="+num+"(Pyresult);\n"
                        
                            
                S.append(CompiledExp+"Py_Finalize();\n")
                return

                
                
                
                

            if("*=" in ln) and not mode:
                ln=ln.split("*=")
                if not("_" in ln[0]):
                    modif="dev_"
                else:
                    modif=""
                    ln[0]=ln[0].split("_")[1]
                head="f_"+ln[0]

                ln=ln[1].split(";")
                var=ln[0]
                var=var[1:len(var)-1]
                var=var.split(",")
                
                variables=""
                for k in range(len(var)):
                    w=Var_dic[var[k]]
                    if "*" in w:
                        variables=variables+modif+var[k]
                    else:
                        variables=variables+" "+var[k]
                    if(k<len(var)-1):
                        variables=variables+","
                CompileExp=head+"<<<"+"Nbl,"+"Nth"+">>>("+variables+");\n"
                S.append(CompileExp)
                
                return

            if("*=" in ln) and  mode:
                ln=ln.split("*=")

                if"_" in ln[0]:
                    ln[0]=ln[0].split("_")[1]
                runvar=ln[0]
                head="f_"+ln[0]

                ln=ln[1].split(";")
                
                limitvar=ln[1].split(",")
                limitvar=limitvar[1]
                
                var=ln[0]
                var=var[1:len(var)-1]
                var=var.split(",")
                
                variables=""
                define=""
                for k in range(len(var)):
                    w=Var_dic[var[k]]
                    if "*" in w:
                        variables=variables+w+" "+var[k]
                        #define=define+"#define "+var[k]+"(i) "+var[k]+"[i] \n"
                    else:
                        variables=variables+w+" "+var[k]
                    if(k<len(var)-1):
                        variables=variables+","
                CompileExp=define+"__global__ void "+head+"("+variables+"){\n"

                preload=""
                preload=preload+"int "+runvar+"=blockIdx.x * blockDim.x + threadIdx.x;\n"
                preload+="if("+runvar+"<="+limitvar+"){\n"
                CompileExp+=preload
                S.append(CompileExp)
                return


                
            
                

            if ";" in ln:
                ln=ln.split(";")
                
                S.append("\n if("+ln[1]+"){\n"+ln[0]+";"+"\n}\n" )
                return
                

            
            if( not (">" in ln) or not("<" in ln) or not("||" in ln) or not("&&" in ln) or not("!=" in ln) ):
                if("if" in ln) or ("while" in ln):
                    return
                if not ("Σ" in ln) or not("Π" in ln):
                    S.append(ln+";\n")
                    return
                
        elif ("<" in ln) or (">" in ln) or ("||" in ln) or ("&&" in ln) or ("!=" in ln):
            if not ("Σ" in ln) or  not("Π" in ln) :
                if not( "->" in ln ) and not("while" in ln) and not("if" in ln):
                    
                    S.append(ln)
                    return


def Compile_IfWhileExpressions(S,ln):
    
    
    if ( ("if" in ln) and ("(" in ln) ) or (("while" in ln) and ("(" in ln)) :
        Compilexp=ln+"{\n"
        S.append( Compilexp )
        return
    if ("*else" in ln):
        ln=ln.split("*")
        Compilexp="\n}\n"+ln[1]+"{"
        S.append( Compilexp )
        
    
            
    ##########################         




def Post_Compile(S,H,Files_dic):
    main="""        
    int main(int argc, char **argv){

    """
    S.append(main)

        

    for head in H:
        S.append(head+";\n")


    
    end="""

    return 0;
    }
    """

    S.append(end)





######################
    
####################


#Alphabet
Greek_Dic = {
    u'\u0391': 'Alpha',
    u'\u0392': 'Beta',
    u'\u0393': 'Gamma',
    u'\u0394': 'Delta',
    u'\u0395': 'Epsilon',
    u'\u0396': 'Zeta',
    u'\u0397': 'Eta',
    u'\u0398': 'Theta',
    u'\u0399': 'Iota',
    u'\u039A': 'Kappa',
    u'\u039B': 'Lamda',
    u'\u039C': 'Mu',
    u'\u039D': 'Nu',
    u'\u039E': 'Xi',
    u'\u039F': 'Omicron',
    u'\u03A1': 'Rho',
    u'\u03A4': 'Tau',
    u'\u03A5': 'Upsilon',
    u'\u03A6': 'Phi',
    u'\u03A7': 'Chi',
    u'\u03A8': 'Psi',
    u'\u03A9': 'Omega',
    u'\u03B1': 'alpha',
    u'\u03B2': 'beta',
    u'\u03B3': 'gamma',
    u'\u03B4': 'delta',
    u'\u03B5': 'epsilon',
    u'\u03B6': 'zeta',
    u'\u03B7': 'eta',
    u'\u03B8': 'theta',
    u'\u03B9': 'iota',
    u'\u03BA': 'kappa',
    u'\u03BB': 'lamda',
    u'\u03BC': 'mu',
    u'\u03BD': 'nu',
    u'\u03BE': 'xi',
    u'\u03BF': 'omicron',
    u'\u03C0': 'pi',
    u'\u03C1': 'rho',
    u'\u03C3': 'sigma',
    u'\u03C4': 'tau',
    u'\u03C5': 'upsilon',
    u'\u03C6': 'phi',
    u'\u03C7': 'chi',
    u'\u03C8': 'psi',
    u'\u03C9': 'omega',
    "diff": sys.argv[1]+"Vars."+"diff",
    "threads": sys.argv[1]+"Vars."+"threads",
    "blocks": sys.argv[1]+"Vars."+"blocks",
    "procid": sys.argv[1]+"Vars."+"procid",
    "Nproc": sys.argv[1]+"Vars."+"Nproc",
    "hproc": sys.argv[1]+"Vars."+"hproc"
}

    

#Init variables
CompiledCode=[]
Headers=[]

include_set=[]

Mark={}

FuncHeads=set()


Files_dic={}

Variable_dic={}

titel="run"

#Load source file
Filen_Name=sys.argv[1]
file=Filen_Name+".txt"

#Pepare source file
try:
    SrcFile=FromatSrcCode( file)
except:
    print("wrong format")



for k in range( len(SrcFile)):
    w=SrcFile[k]
    w=PreCompile_TransGeek(w,Greek_Dic)
    SrcFile[k]=w




 
     



#Collect all variables and includes

for w in SrcFile:
    if".h" in w:
        w=w.split(":")
        include_set.append(w[1])
    
    if(("€" in w)or ("#" in w) or ("->" in w)):

        if(("#" in w) or ("->" in w)):

            if("->" in w):
                w=w.split("->")
                w=w[0]
            w=w.split(":")[1]
            w=w.split(",")
            if "" in w:
                continue
            
            for k in w:
                if "&" in k:
                        k=k.replace("&","")
                if not("(" in k):
                    
                    Var_dic[k]="double "
                    

                else:
                    
                    k=k.split("(")[0]
                    
                    Var_dic[k]="double * "
  
            continue
        #########
        
        w=w.split("€")
        
        if "|R" in w[1]:
            num="double"
        elif"|N" in w[1]:
            num="int"
        else:
            num=w[1]
        

        if "," in w[0]:
            vec=0
            w[0]=w[0].split(",")
            
            if"(" in w[1]:
                vec=1
                leng=w[1].split("(")[1]
                leng=leng.replace(")","")
            else:
                leng="1"

            for k in w[0]:
                VarSize_dic[k]=leng
                
                if "*" in k:
                    k=k.split("*")
                    k=k[0]
                    Var_dic[k]=num+" *"
                else:
                    if vec==1:
                        Var_dic[k]=num+" *"
                    else:
                        Var_dic[k]=num
                        
                        
               
        else:
            if("*" in w[0]) and ("(" in w[1]):
                k=w[0].split("*")
                k=k[0]
                Var_dic[k]=num+"*"
                w[1]=w[1].split("(")[1]
                w[1]=w[1].replace(")","")
                VarSize_dic[w[0]]=w[1]
                

                
            elif("*" in w[0]):
                k=w[0].split("*")
                k=k[0]
                Var_dic[k]=num
                VarSize_dic[k]="1"
            else:
                Var_dic[w[0]]=num
                if"(" in w[1]:
                    Var_dic[w[0]]=num+" *"
                    w[1]=w[1].split("(")[1]
                    w[1]=w[1].replace(")","")
                    VarSize_dic[w[0]]=w[1]
                else:
                    VarSize_dic[w[0]]="1"
                    
                
        




SrcGpuFile=[]


for w in SrcFile:

    if("kernel(" in w) or ("*=" in w):
        m=SrcFile.index(w)
        for j in range(m, len(SrcFile)):
            h=SrcFile[j]
            if "*;" in h:
                n=SrcFile.index(h)
                break
        SrcGpuFile.extend(SrcFile[m:n+1])
        del SrcFile[m+1:n+1]
    


##################

for w in SrcFile:
    if "programtype:" in w:
        w=w.split(":")
        w=w[1].split("/")
        Ptyp=w


        

#Compile Gpu part of the programm



CompiledGpuCode=[]

mode=True

for w in SrcGpuFile:

    w=PreCompile_TransGeek(w,Greek_Dic)

    Compile_Brackets(CompiledGpuCode,[],w)

    Compile_expressions(CompiledGpuCode,w,mode)

    Compile_DefineVariables(CompiledGpuCode,w,Ptyp)

    Precompile_DefineNumbers(CompiledGpuCode,w,Variable_dic,Ptyp)

    

    Compile_StandardTasks(CompiledGpuCode,Files_dic,Variable_dic,w,mode)


    Compile_IfWhileExpressions(CompiledGpuCode,w)

    





###################


#Precompile process


#set programmtype



        

#change

PreCompile_head(CompiledCode,Ptyp,include_set)

#Makkros

makro=""
for k in Var_dic:
    makro="#define "+k+"(i) "+k+"[(int)(i)]\n"
    CompiledCode.append(makro)
        
    



   
for  w in SrcFile:
    if "$" in w:
        continue

    w=PreCompile_TransGeek(w,Greek_Dic)
    

    #PreCompile_SetMakros_ForArrays( CompiledCode , w,Mark)

    PreCompile_SetFunctionHeads(CompiledCode,FuncHeads,Ptyp,w)

    Precompile_Import(CompiledCode,Files_dic,w)


CompiledCode.extend(CompiledGpuCode)    

   

#########
                
            
##################################



#Constrtuct code

mode=False    

for  w in SrcFile:

    if"titel" in w:
        w=w.split(":")
        titel=w[1]

    if"$" in w:
        continue

    w=PreCompile_TransGeek(w,Greek_Dic)
    
    Compile_Functions(CompiledCode,w,Headers,FuncHeads,Ptyp)

    Compile_Brackets(CompiledCode,Headers,w)

    Compile_DefineVariables(CompiledCode,w,Ptyp)

    Precompile_DefineNumbers(CompiledCode,w,Variable_dic,Ptyp)

    

    Compile_StandardTasks(CompiledCode,Files_dic,Variable_dic,w,mode)

    Compile_expressions(CompiledCode,w,mode)

    Compile_IfWhileExpressions(CompiledCode,w)

    Compile_Import(CompiledCode,w)

    

#####################

#Post Compile

if not("libary" in Ptyp):
    Post_Compile(CompiledCode,Headers,Files_dic)

####################




#Save in C-File

if ("gpu" in Ptyp) or ("cu" in Ptyp):
    CompiledFile=Filen_Name+".cu"
else:
    CompiledFile=Filen_Name+".cpp"
    

if"libary" in Ptyp:
    HeaderFile=Filen_Name+".h"
    f = open(os.getcwd()+"\\"+HeaderFile, "w",encoding="utf-8")
    for k in FuncHeads:
        f.write(k)
    f.close()    



f = open(os.getcwd()+"\\"+CompiledFile, "w",encoding="utf-8")
       
for k in CompiledCode:
    f.write(k)

f.close()    



#Run compiled file


#os.system("g++ "+os.getcwd()+"\\"+"tinyxml\*.cpp "+os.getcwd()+"\\"+CompiledFile+ " -o "+ titel)















    
