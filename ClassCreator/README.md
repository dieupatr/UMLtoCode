# ClassCreator
In dieser Dokumentation werden aus **Drawio** Klassen-Diagrammen **Code** generiert. Um dies zu realisieren wird das Programm **ClassCreator** verwendet.
## Inhaltsverzeichniss
* [Quickstart](##Quickstart)
* [FuncDoc](Doc/FuncDoc.md)
* [AdvancExampel](Doc/AdvancExampel.md)
## Quickstart
Zu beginn legen wir das folgende Klassen Diagramm in **Drawio** an.


![Bild](Doc/Bilder/QuickClassDiagramm.png)


Wichtig ist, das nur die folgenden **Formen** verwendet werden.
* UML/Class
* Pfeil mit breiten weissen Kopf


Der folgende Konsolen aufruf generiert dann den entsprechenden **Quellcode**



	ClassCreator.py ClassDiagramm.drawio Quick.cs


**Output:**

[**Generierter Code in Quick.cs**](Doc/Quick.cs)
