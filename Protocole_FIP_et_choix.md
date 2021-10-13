# World-FIP

## Description générale

Le protocole FIP est un protocole de gestion de bus basé sur le modèle *producteur/consommateur*.  
Différents objets et messages peuvent être échangés, des producteurs vers les consommateurs.  
Les échanges sont gérées par un ***arbitre de bus*** qui est chargé d'initier les échanges.
Les objets transférés peuvent être périodiques ou pas. Étant donné notre sujet, nous ne
traiterons **que des objets périodiques**.

Les objets sont diffusés en *broadcast*, tandis que les messages sont envoyés en *pair-à-pair*.
Vu le cours et le sujet de TP, **nous n'allons utiliser uniquement que la transmission d'objets**.  
Les objets sont identifiés grâce à un *ID*. Chaque *producteur/consommateur* est lié à un plusieurs
objets identifiés. L'*arbitre de bus* est chargé de déterminer en fonction de tous les objets
périodiques, un ordonnancement des tâches --- c'est à dire quels objets sont envoyés à quelle
période. Il construit pour cela une table.

Pour résumer on a :
- un arbitre de bus
- un seul type d'objet (en plus d'être périodique)
- un consommateur
- un producteur

## Détails techniques

Dans le cas des objets périodiques, la configuration du réseau est connue au lancement du
programme --- il n'y pas une sorte de fetch sur le réseau. Cette configuration peut donc ête
stockée à priori en dehors du réseau FIP (via un fichier texte ou par exemple) ; l'arbitre,
les producteurs et les consommateur charge cette configuration lorsqu'ils rejoigne le réseau.

Ensuite suit l'échange de message (texte issus du cours de ***M. Zoubir***):

> Le déroulement d’un échange de données s’effectue selon les étapes suivantes :
>
> 1. En utilisant sa table, l’arbitre de bus diffuse une trame (appelée ID-Dat) contenant
> l’identificateur d’un objet (il s’agit de l’objet que la table d’arbitre de bus indique comme
> étant l’objet à échanger à l’instant courant).
> 2. En “lisant” l’identificateur diffusé, le producteur et le(s) consommateur(s) de l’objet diffusé
> se reconnaissent.
> 3. Après un temps dit temps de retournement (fixé à quelques dizaines de μs pour un débit de 1 Mb/s),
> le producteur diffuse une trame (dite RP-Dat) contenant la valeur du tampon de production associé à
> l’objet dont l’identificateur a été diffusé par la dernière trame ID-Dat.
> 4. Le(s) consommateur(s) de l’objet met(tent) à jour la valeur de son (leur) tampon de réception à
> partir de la valeur contenue dans la trame RP-Dat.
> 5. Après un intervalle de temps égal au temps de retournement, l’arbitre de bus passe à
> l’identificateur suivant dans la sa table (quand le dernier identificateur de la table a été diffusé,
> l’arbitre de bus repart à partir du premier identificateur de la table).

Pour l'étape 3, le temps de retournement est fixé à une valeur permettant d'obtenir les débits souhaités.  
De plus, le protocol n'assure aucune forme d'acquittement (*ack*).

Comme nous émulons le FIP au dessus d'un protocole existantm il convient de choisir ledit protocol.
Puisque que la transmission d'objets est basé sur du ***broadcast*** et ***ne nécessite pas d'ack***,
l'UDP semble tout indiqué.

Pour la forme des différentes trames (qu'on voit dans le cours de Zoubir. D'ailleurs, c'est pas exactement
les mêmes que dans l'autre document, génial non ?). J'ai utilisé celles données par Zoubir vu que c'est lui
qui nous note, en soit la seul différence est la fin de trame qui est sur 1 ou 2 bits selon la source. J'ai
modifié le fichier `frame.py` pour inclure le format adéquat ainsi que le support pour créer les frames.

Dernier point (que je n'ai pas encore oublié) : je comprends pas l'histoire des LEDs.  
À aucun moment dans le cours il y a une idée de "temps de production", surtout que je vois pas à quoi ça correspond IRL, un capteur il met pas 200ans à recueillir sa donnée et l'envoyer non ? Il y a bien
l'histoire du temps de transmission mais ça n'a pas l'air d'être ça dont il parle.  
> Je ne pense pas que ce soit ća en effet.
Pareil pour le consommateur et son "temps de consommation". Bein il lit la valeur, la stocke et voilà ? Ça prend 1μs (et encore).
> Je donne ma langue au Zoubir.
> Je pense qu'il veux qu'on simule une espèce de *temps de traitement* ? Dans tout les cas on peut ajout un
> délais arbitraire qui représente ledit temps de traitement. La seule contrainte étant qu'un producteur doit pourvoir répondre au message dans les temps pour communiquer le suivant. De même, l'ensemble des messages envoyés
> à une prériode `p` doit pouvoir être effectivement envoyé avant `p + 1`.

Ou alors il veut dire, que ce soit pour le conso ou le prod, que le temps de conso/prod correspond à la
période de prod/conso (tous les coombiens c'est produit/consommé). Sauf que ça n'a pas vraiment de sens
pour le conso vu que lui il sait juste qu'il doit consommer quand l'arbitre le lui dit (donc à priori pas
de notion de période directement). De toutes façons les deux périodes doivent être synchro puisque l'arbitre
a dans sa table une période unique pour un type d'objet donné.

Bref je comprends pas trop, help me plzz.
> J'ai pu faire des trucs sauf la dernière partie (sur les LEDs), déso pas déso.

Autre point, pour le code il manque grossièrement que la partie *conso/prod* qui peut être assez basique pour
l'instant. Les deux peuvent partager la partie réception d'un message. Le producteur recevant l'***ID-Dat*** et
le consomateur recevant le ***RP-Dat***.
Pour l'envoie du ***RP-Dat***, le code sera propre au producteur, tout comme la partir traitement de l'***ID-Dat**
pour savoir s'il est concerné.

Au niveau du code, oublie tout ce qui est gestion des sockets en python, je m'en chargerais (sauf si ća t'amuse).
En revanche tu peux faire l'ago qui décrit tout ća (en pseudo-python) comme ća j'ai plus qu'à beautify le code et
en avant guingamp.
