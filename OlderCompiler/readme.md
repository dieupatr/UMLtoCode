
# Erste Schritte


Zu Beginn, legen wir eine "HalloWelt.txt" Datei an.

![Unbenanntes Diagramm](https://github.com/dieupatr/CNote/assets/93820975/37fa67a7-8c31-4e1d-beee-ec5c61994a59)



In diese schreiben wir den folgenden Inhalt:

```
				Main

programtype:cpu


#MainAlg:       {


out:"hallo"


}


```


<br><b>"#Main"</b> definiert ein Kapitel und "out:" gibt einen String auf der Konsole.<br><br><br><br>  


Als nächstes, öffnen wir eine Konsole in dem aktuellen Verzeichniss. 

![Konsole](https://github.com/dieupatr/CNote/assets/93820975/91f70a7b-0ba7-49b4-9d10-b141b1fbe63b)




In diesem Kompilieren wir unsere text datei mit dem Befehl.

```
.\note.py HalloWelt

```


Das Resultat ist, die Datei "Hallowelt.cpp".

![HalloWeltCpp](https://github.com/dieupatr/CNote/assets/93820975/7c83c8bf-f14f-48c7-b270-1099c4824c7e)



Zum Schluss, braucht die generiert Datei, nur noch in C++ Kompiliert werden.

```
g++    HalloWelt.cpp   -o run

```


Die Ausgabe ist.

![Halloweresult](https://github.com/dieupatr/CNote/assets/93820975/a88a26b6-7829-43f4-9382-9e527657444b)








