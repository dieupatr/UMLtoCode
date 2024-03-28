# Dokumentation des Programiercodes von LexDrawio



## Klasse:  **Cell**

**Beschreibung:** beschreibt ein Objekt in einem **Diagramm**   *

**params:**   

typ:  **Dictonary**

 **attr**= **{**
* Die **id** macht das Objekt im Diagramm einzigartig
* Der **value** gibt den **Text** in der Zelle an. Im obigen Diagramm ist es **Box 1**

* **style** beschreibt das Ausehen. Hier ist auch der Typ der **Zelle** enthalten.
* **source** und **target** gibt es nur bei **Pfeilen**. 
* **parent** Das ist die **id** der Zelle auf der diese liegt.
* **geometry** beinhaltet die **Position** und die **Abmessungen** der 
Zelle.

 **}**


**Methoden:**

**PrintData()**  :   Schreibt alle Daten auf die Konsole.



## Klasse:  Diagramm

**Beschreibung:** beschreibt eine Menge von **Cell** objekten die in 
**Blöcke** und **Pfeile** eingeteilt sind.

**param1:**  Blocks; Liste ;  Eine Liste von *Cell** objekten die als Blöcke Klazifiziert wurden.

**param2:** Arrows ; Liste ; ine Liste von *Cell** objekten die als Pfeile Klazifiziert wurden.







## Funktion **ParseDiagramsFromXmlFile**

**Beschreibung:**   Übersetzt ein **Xml** aus Drawio in in Datenobjekte
die im **Code** verwendet werden können. 


**param1:**  file_path ; string;   der Pfad, wo das **Drawio-Xml** liegt.

**return:**  Diagrams ; Dictonary;  ein Dictonary von Diagramen siehe Klasse Diagramm.









