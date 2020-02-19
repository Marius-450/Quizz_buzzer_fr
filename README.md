# Quizz_buzzer_fr
Système d'arbitrage pour Quizz avec Circuit Playground. jusqu'à 4 joueurs.

## Pré-requis

### Materiel
* Une carte Circuit Playground d'Adafruit
* 5 cables a pinces crocodile
* 5 "Pads" : pièces de monaies, bricolages en aluminium, fruits ...

### Logiciel

* CircuitPython 5.x beta 5

#### Bibliothèques
* adafruit_circuitplayground
* neopixel
* adafruit_thermistor

## Mise en place et configuration

Le code est configuré pour 4 "équipes" ou joueurs, et un arbitre <br>
* Equipe 1 = Vert, connecté sur A1
* Equipe 2 = Jaune, connecté sur A2
* Equipe 3 = Rouge, connecté sur A5
* Equipe 4 = Blanc, connecté sur A6 (RX)
* Arbitre = Noir/bleu, connecté sur A4

/!\ Connectez les pads avant de brancher la batterie ou le cable usb. sinon, il faudra presser le bouton *reset* pour recalibrer la fonction tactile.

les variables `TEMPS_MAXIMUM` et `INACTIVITE` peuvent être modifiées au début du fichier code.py pour l'adapter aux besoins.


## Jeu

Lorsque l'arbitre lâche son touchpad, un son est joué, les LED deviennent bleues.<br>
Les joueurs ont ensuite 30 secondes pour toucher leur pad. Le gagnant est le plus rapide. Il est annoncé avec un nombre de sons correspondant au numéro de l'équipe. Ensuite les 3 LED les plus proches du cable du gagnant s'allument de la couleur correspondante a l'équipe.<br>
Si un ou plusieurs autres joueurs ont touché leur pad dans la même seconde, le second meilleur temps est indiqué par une seule LED allumée moins fort, proche du cable correspondant, de la couleur de l'équipe.<br>
Les données brutes sont indiquées par la liaison série (REPL), mais aussi l'écart de temps en milliseconde entre le meilleur et le second, par exemple.<br>
Si personne ne répond avant 30 secondes, un son est joué, puis toutes les LED sont allumées en rouge.
L'interrupteur permet de couper le son. Dans ce cas, la LED D13 est allumée.<br>
Au bout de 20 secondes d'inactivité, une animation se déclenche. La couleur principale correspond au dernier gagnant.<br>

## Informations techniques 

* La boucle qui enregistre les temps de réponse dure entre 1.6 et 1.8 millisecondes avec un Circuit Playground Bluefruit. c'est donc la précision maximale que l'on peut attendre de cet appareil.
* Il est possible d'ajouter 2 joueurs supplémentaires, les emplacements A3 et A7 (TX) étant libres. (les pixels, moins...)

### Documentation (en)

* https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express/circuit-playground-express-library
* https://learn.adafruit.com/circuit-playground-express-piano-in-the-key-of-lime



# Todo et Idées en Vrac

* Une communication bluetooth est envisageable pour annoncer le vainqueur, donner le Go, et pourquoi pas exporter le son (CP Bluefruit seulement)
