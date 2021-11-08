
# WorldFIP Protocol emulation

## Tools used

- 3x Raspberry Pi
- Python3
- Sockets over a Wi-Fi network

M2 SIAME - 2021/2022 - Université Toulouse 3 - Paul Sabatier

## Overview

- Emulation d'un réseau sous protocole [WorldFIP](https://en.wikipedia.org/wiki/Factory_Instrumentation_Protocol) à travers la Wi-Fi

- Emulate a [WorldFIP](https://en.wikipedia.org/wiki/Factory_Instrumentation_Protocol) protocol based network over Wi-Fi

## Documentation

### Project's objectives

**Émulation du réseau WorldFIP à l'aide du WiFi**
Implanter le protocole sur au moins deux RPi pour émuler le fonctionnement de l'arbitre de bus, d'un producteur et d'un consommateur d'objets. Lorsqu'un producteur a une nouvelle valeur, il allume une **LED1** pendant un temps équivalent à **1/10** de son temps de production. Quand un consommateur reçoit une valeur dépassant de **20%** la valeur précédente, il allume une **LED rouge** pendant un temps équivalent à **20%** de sa période de consommation. Sinon, il laisse allumée une **LED verte**.

### Usefull links

- (FR) [Cours](https://www.irit.fr/~Zoubir.Mammeri/Cours/Introduction_WorldFIP.pdf) WorldFIP Introduction - M2SIAME Course UNIV-TLSE3
