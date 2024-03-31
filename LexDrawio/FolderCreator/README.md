# FolderCreator

In diesem Teil wird eine einfache Anwendung der Implementierung von 
**LexDrawio** vorgestellt. 

Die Anwendung **FolderCreator** hat die folgende Aufgabe, sie generiert aus einem Diagram **Odner** und **Dateien** auf dem Computer.

![link](Bilder/Task.PNG)

*************************************************************


<br></br><br></br>

## Demonstration

Wir beginnen mit dem Folgenden Diagram. 

![link](Bilder/FolderDia.PNG)

Dieses wurde mit **Drawio** erstellt  und unter **FolderDiagramm.drawio** abgespreichert.


Hier sind einige **Ordner** und eine **Datei** zu sehen. Die **balue Markierung**  ist das **Stammverzeichniss** in welchem die Odner/Datein später erzeugt werden. 

Der nächste Schritt ist das Öfnnen einer **Konsole**, dort geben wir den 
folgenden Befehl ein


    .\FolderCreator.py FolderDiagramm.drawio

Dieser generiert die Ordner/Datein in dem entsprechenden Verzeichniss. 
<br></br><br></br>
Der **Output** ist :

![link](Bilder/Folder.PNG)

<br></br><br></br>
# Technische Details

Die folgenden **Formen** wurden in **Drawio** benutzt.


## Card

![link](Bilder/Card.PNG)


## UML2.5/Folder

![link](Bilder/Folder_Drawio.PNG)


************************************
<br></br><br></br>

## Konsolen aufruf

Das Skript **FolderCreator.py** kann über den folgeden Konsolenbfehl 
aufgerifen werden.


    .\FolderCreator.py    [Name des Drawio files]





