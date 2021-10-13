# Réseaux pour applications mobiles et de surveillance

Université Toulouse 3 - Paul Sabatier 

M2 SIAME - 2021/2022

Emulation d'un réseau sous protocole [WorldFIP](https://en.wikipedia.org/wiki/Factory_Instrumentation_Protocol) à travers la Wi-Fi

Emulate a [WorldFIP](https://en.wikipedia.org/wiki/Factory_Instrumentation_Protocol) protocol based network over Wi-Fi

# Documentation
### Objectif du projet
**Émulation du réseau WorldFIP à l'aide du WiFi**

Implanter le protocole de FIP sur au moins deux RPi pour émuler le fonctionnement de l'arbitre de bus, d'un producteur et d'un consommateur d'objets. Lorsqu'un producteur a une nouvelle valeur, il allume une **LED1** pendant un temps équivalent à **1/10** de son temps de production. Quand un consommateur reçoit une valeur dépassant de **20%** la valeur précédente, il allume une **LED rouge** pendant un temps équivalent à **20%** de sa période de consommation. Sinon, il laisse allumée une **LED verte**.

### Liens intéressants

- (FR) [Cours](https://www.irit.fr/~Zoubir.Mammeri/Cours/Introduction_WorldFIP.pdf) sur le WorldFIP
- (EN) [Document](http://people.cs.pitt.edu/~mhanna/Master/ch2.pdf) semblerait-il issu d'une thèse détaillant un peu plus le protocole, notamment pour l'arbitre de bus
