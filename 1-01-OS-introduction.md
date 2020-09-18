---
jupytext:
  cell_metadata_filter: all,-hidden,-heading_collapsed
  notebook_metadata_filter: all,-language_info,-toc,-jupytext.text_representation.jupytext_version,-jupytext.text_representation.format_version
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

<div class="licence">
<span>Licence CC BY-NC-ND</span>
<div style="display:grid">
    <span>Benoît Gschwind</span>
</div>
<div style="display:grid">
    <span><img src="ensmp-25-alpha.png" /></span>
</div>
</div>

+++

# Cours et mini-projet introductif sur les OS

*OS = Operating System = système d’exploitation*

+++ {"tags": []}

Le but de ce cours est de vous donner une petite idée de ce que sont les systèmes d'exploitation. Afin que ce soit plus ludique, nous allons le faire cette année à travers la simulation en Python d'un *scheduler*. Le *scheduler* est le code au coeur de votre OS qui choisi l'ordre d'éxécution des programmes sur votre ordinateur.

Ce mini-projet peut être réalisé à un premier niveau que nous espérons simple par les élèves qui ne sont pas très familiers avec ces notions, et les plus *geeks* d'entre vous pourront aller aussi loin qu'ils le veulent.

Mais commençons rapidement à contextualiser les systèmes d'exploitation et les ordinateurs. Attention, ces explications se veulent très simples, elles ne sont là que pour fixer les idées, elles peuvent parfois tomber dans la sur-simplification.

+++

## Pourquoi un système d'exploitation ?

+++

Un ordinateur est un système complexe, composé habituellement d'un ***processeur*** pour faire des calculs, de ***mémoires*** pour stocker les programmes qui s'exécutent et leurs données, de ***périphériques*** (clavier, souris, écran, disque...) et de ***bus*** pour faire communiquer tout cela.

Tous ces dispositifs ont des contraintes et des spécificités intrinsèques à leur composants éléctroniques sous-jacents et ne comprennent que des langages machine souvent abscons. De plus, pour un même dispositifs tels que le processeur ou le clavier, il existe de nombreuse variantes avec des fonctionnements différent. Etant données qu'il est difficile et long de maitriser le fonctionnement de chaque dispositif, les ordinateurs possèdent une couche logicielle, appelée le système d'exploitation qui propose plusieurs fonctionnalités comme :
1. l’OS gère les ressources matérielles de votre ordinateur tels que le processeurs, la memoire ou l'écran afin de partager ces resources aux différents programmes qui s'executent sur l'ordinateurs, par exemple l'ordinateur peut executer plusieurs programmes en "même temps" même si votre ordinateur ne possède qu'un seul processeur;
1. l’OS fournit aux programmeurs d’applications des couches *abstractions* pour gérer ces ressources matérielles de manière à caché le fonctionnement interne des différents composants et de permetre aux utilisateurs d'utilisé un même programme sur des ordinateurs différents; ainsi votre éditeur de texte préféré peut fonctionner sur un grand nombre d'ordinateur très différents.

Dit autrement: l’OS fonctionne **directement** sur le matériel et il est la base pour tous les autres logiciels: il permet de partager de *manière transparente* les différentes ressources physiques (processeurs, mémoires, périphériques); les programmeurs travaillent sur une **abstraction simple et de haut niveau de l'ordinateur**.

+++

## L’OS: une abstraction des ressources matérielles de l’ordinateur

+++

Pour illustrer les couches d'abstraction qu'un OS fournit, prenons l'exemple des disques durs. Les disque durs sont des composant informatique qui fournissent un stockage de données de masse. Sorti de sa boite, et selon les modèles, la doc technique va vous dire que l'objet a tant de disques, tant de secteurs, tant de blocs; ça peut être un disque mobile ou un SSD; on peut le brancher de plein de façons (scsi/sata/usb); bref, c'est d'une complexité infinie. 

Mais en tous cas ce qui est sûr, contrairement à ce que l'on pourrait penser: un disque dur n'offre pas de notion de dossier ou de fichier !

Ce sont des notions complètement artificielles qui sont **créés de toute pièces** par l'OS, pour vous permettre d'écrire du code qui puisse faire référence à du contenu organisé en hiérarchie, et cela quel(s) que soi(en)t le(s) disque(s) physiquement conecté(s) à votre ordi. Voilà donc un bel exemple d'abstraction.

Par ailleurs nous pouvons également prendre l'exemple des caméra vidéo. Chaque modèle de camera possède des caractéristiques différentes et fonctionne différemment, donc pour faciliter leurs utilisation, l'OS va exposer aux applications une ***Application Programming Interface*** (API) uniforme pour gérer n'importe quel caméra vidéo. En interne, ce sera le rôle du driver de faire le lien entre l'abstraction, i.e. l'API, et la réalité de cette caméra-là. C'est ce qui permet à une application comme Zoom de fonctionner sur n'importe quel ordinateur pourvu que l'OS fournis les drivers adéquat.

De manière générale, les abstractions ont pour objet :

* de limiter la complexité pour l'écriture des applications; nos programmes, en ne dépendant pas de matériels spécifiques, sont plus faciles à écrire et plus portables
* de rendre possible la cohabitation de plusieurs programmes qui tournent en même temps
* d'être en mesure de faire du contrôle d'accès, i.e. qui a le droit de faire quoi
* et de partagé les resources disponibles.

Les clients du système d’exploitation sont les applications. Ce sont elles qui traitent directement avec le système d'exploitation et ses abstractions.

Naturellement l'utilisateur humain est lui aussi, indirectement, un client du système d'exploitation, à travers le `terminal shell` ou bien sûr une interface graphique (pour simplifier votre accès à l'OS).

En conclusion, disons qu'un OS:
* est un très gros programme, par example Linux est composé de plusieurs millions de lignes de code
* qui fait la jonction entre l’ordinateur et l’utilisateur
* grâce à sa parfaite connaissance des composants de l'ordinateur et leurs spécificités (grâce aux drivers).

Pour aller plus loin, vous trouverez une annexe avec une presentation très rapide sur les composants d'un ordinateur, et la notion d'espace utilisateur (user space) et d'espace noyaux (kernel space).

+++

# Le mini-projet: simulation de la gestion de processus

+++

Sur vos ordinateurs, vous avez l'habitude que plusieurs programmes s'exécutent en même temps (un gestionnaire de mails, un explorateur d'Internet, un éditeur de code, un terminal avec Python...).

Et lorsque plusieurs programmes sont lancés en même temps dans un ordinateur, l’OS doit partager l’utilisation du processeur (du CPU) entre les programmes. L’algorithme qui décide de la manière d'allouer le processeur aux programmes s'appelle un ***scheduler*** (ordonnanceur, planifieur). Dans ce contexte, on appelle un programme qui s'exécute un ***process*** (processus)

+++ {"tags": ["level_intermediate"]}

Pourquoi on appelle ça *process* et pas juste un programme ou une application ? parce que ces termes sont vagues, une application qui tourne peut en fait impliquer plusieurs (dizaines de) *process*; en fait la notion de *process* correspond à une abstraction dans l'OS, c'est l'unité atomique pour les programmes.

+++ {"tags": []}

Vous allez réaliser un mini-projet en Python pour simuler ce ***scheduler*** et coder un algorithme simpliste pour allouer les resources du processeur.

Donc tout d'abord, il faut comprendre comment travaille le processeur

+++ {"tags": []}

## Le processeur

+++

Le processeur exécute les instructions des programmes informatiques. Très schématiquement, pour faire cela, il doit récupérer *quelque part dans la mémoire* les instructions qui forment un programme (`fetch`), il va les décoder (`decode`) et il va les *exécuter* (`execute`).

Ainsi, son `cycle de base` consiste à:

1. récupérer la prochaine instruction du programme
1. la *décoder*
1. l'exécuter
1. ... et à recommencer jusqu'à la terminaison du programme.

Nous allons considérer que le temps dans votre simulateur sera cette succession de `cycle de base`, autrement dit, le simulateur ne s’exécute pas en temps réel mais suit le temps décrit par ses cycles.

Le rôle de votre simulateur est d'ordonnancer (de planifier) l'exécution des programmes. C'est pour cela qu'on l'appelle un `scheduler`. Il va contenir l'état de la planifications des processus et il sera chargé d'exécuter la simulation de ces processus.

+++

## Le  processus `init`

+++

Il y a quelque chose qu'il faut bien comprendre dans le fonctionnement de l'OS-linux, c'est la notion de `premier processus`.

Quand vous bootez un ordinateur l'OS commence par faire toutes sortes d'initialisation (le matériel, le filesystem, etc..), des trucs qui lui sont propres.

Ensuite du côté des utilisateurs, selon les cas, on voudrait par exemple: 

* soit lancer une interface graphique parce que c'est un ordi de bureau
* soit lancer un serveur web et une base de données parce que c'est un serveur de e-commerce 

Bref, il nous faut un moyen de configurer la liste des programmes qui doivent démarrer lorsque l'OS est prêt; et ça pour bien séparer les rôles, ça ne peut pas être defini dans le système d'exploitation, ce n'est pas son travail !

Donc le choix qui a été fait a été de dire qu'une fois que l'OS est prêt il démarre **un unique processus**. Pour la petite histoire, un processus est identifié par un numéro qu'on appelle son *pid* pour *process id*, et le process initial a toujours le *pid* numéro 1; pour des raisons historiques, on appelle cet unique processus `init` (quoique sur les systèmes modernes on devrait plutôt l'appeler `systemd`).

Ce processus initial ne fait pas partie du système d'exploitation, il tourne en *user space* (cf. annexe), et son travail c'est uniquement de lancer tous les process dont on a besoin; sachant que ces process peuvent eux-mêmes en lancer d'autres naturellement.

Et le travail du scheduler, c'est de gérer la liste des process qui sont encore actifs, et de leur attribuer le processeur à tour de rôle.

Donc pour redire à nouveau tout ça autrement: au démarrage, le système d'exploitation démarre son scheduler avec un unique processus à faire tourner, le processus `init`, dont le travail est principalement de lancer à son tour toutes les autres applications dont on a besoin sur cette machine, et qui vont au fur et à mesure rejoindre le processus initial dans la liste des process actifs que gère le scheduler. Dans la pratique, si le processus `init` vient à terminer, l'OS arrête la machine.

+++

## `fork` et `exec`

+++

Voilà, ce qu'il faut aussi comprendre c'est qu'en dehors du processus `init` les nouveaux processus ne se créent pas *à partir de rien*, mais sont tous créés par **une autre application**. Par exemple quand vous lancez `python` depuis votre terminal, vous créez un process; quand vous double-cliquez dans l'application 'Mail' à partir de votre Windows, vous créez un process.

Donc c'est toujours une application qui est à l'origine de la création d'un process, mais ça ne peut pas non plus se faire sans la complicité du système d'exploitation; les concepteurs de linux ont choisi qu'un nouveau processus soit créé par *division* (`fork`) d'un processus existant, dans le genre division cellulaire. Le processus obtenu par division, est donc le fils-identique de celui qui vient d'être `forké`.

Dans certains cas, les deux processus continuent d'exécuter le même programme, mais dans la grande majorité des cas, l'un des deux, généralement le fils, passe complètement à l'exécution d'un autre programme en utilisant l'appel système `exec`.

Voilà comment on obtient une arborescence de processus dont la racine est le processus initial `init`.

+++

La fonction `fork` est un `appel système` c'est-à-dire un `appel au système d'exploitation` via son API, en l'occurance ici une API de gestion de processus. C'est donc l'OS qui va accomplir cette division. Avec `fork` il va donner naissance à un nouveau processus qui est la copie conforme du processus `forké` a quelques différences près afin de pouvoir déterminer qui est le fils.

La fonction `exec` est aussi un `appel au système d'exploitation`. On demande à l'OS de lancer un nouveau programme dans le contexte d'un processus pré-existant. L'OS va remplacer tout simplement l'exécutable (le programme) pré-existant, en gros la seule chose qu'il garde c'est le numéro du processus qui a été obtenu lors de la division.

+++

Afin de vous faire comprendre tout cela.

Nous allons définir un tout petit langage de script dans lequel vous allez pouvoir programmer votre `init` (puisque vous allez faire comme linux) et par simplicité, vous allez aussi utiliser ce petit langage pour écrire d'autres programmes dont vous voulez simuler l'exécution par le scheduler.

+++

## Le mini-langage de script

+++

Afin de simuler l'exécution de programmes, définissons tout d'abord un miniscule langage de script avec lequel vous allez écrire plusieurs petits programmes, que vous stockerez *quelque part* afin que votre scheduler y accéde (lors d`exec`) et les fasse exécuter par votre simulateur de gestion de processus.

Nous choisissons de stocker chaque programme dans un fichier de la même manière que le système exploitation stocke les programmes.

+++

Notre mini-langage de script comporte donc une liste d’instructions. Ce sont les différentes actions que peut faire le processeur lors de l'exécution de votre programme.

Vos petits programmes seront écrits, à partir de cette liste d'instructions, dans un fichier texte donc `un fichier = un programme`.

Chaque ligne de ce fichier sera une instruction que le simulateur interprétera en un *cycle de base*  donc `une ligne d'un programme = une instruction` et `une instruction dure un cycle`.

+++ {"tags": []}

Voici la liste des instructions de base, vous pouvez naturellement ajouter des instructions qui vous semblent nécessaires ou intéressantes pour complexifier ce langage.

Mais disons que, pour l'instant, nous considérons:

* `fork` pour créer de nouveau processus

* `exec filename` pour remplacer un processus par l'exécutable stocké dans le fichier `filename`

* `busy n` cette instruction indique au simulateur qu'il va être occupé pendant `n` cycles, *comme si* il exécutait `n` instructions mais on ne spécifie pas ces instructions: on occupe juste le processeur (c'est là que se trouveraient les spécificités de votre langage de programmation)

* `print` cette instruction demande au processeur d'afficher le texte qui va jusqu'à la fin de la ligne

* `print_status` cette instruction affiche l'état du simulateur

* les lignes qui commencent par `#` sont des commentaires
* et les ligne vides sont ignorées.


<div style="background-color: #fff0f0; padding: 20px;">
    
Il est important de souligner que dans ce modèle simplifié, on ne s'intéresse pas du tout à la partie purement calculatoire des programmes; nous n'avons pas d'addition, pas de test pour faire un `if`, rien de tout cela.
Tout ce qui correspond dans la vraie vie à un calcul apparaît dans notre modèle comme un `busy`, où on se contente d'indiquer le nombre de cycles que prendrait le calcul.

À quoi ça sert alors ? on veut juste mettre en évidence l'importance de l'algorithme de planification sur le comportement global du système, car c'est un élément important pour l'apprentissage de la programmation concurrante.

</div>

Voici un exemple de programme qui sera écrit dans un fichier texte `script1.s`:

```bash
# simulate the execution of 100 instructions
busy 100
# display hello world !
print "hello world !"
# execute 10000 instructions
busy 10000
# display the scheduler status
print_status

```

Ce programme commence par occuper (`busy`) le processeur pendant `100` cycles de base, ensuite il affiche (`print`) "hello world !", puis il occupe encore `10000` cycles du processeur et enfin, lors de son dernier cycle de base, il affiche l'état du simulateur.

Ou encore:
```bash
# simulate the execution of 500 instructions
busy 500
# duplicate the current process the parent process will skip one instructions while child will do exec.
fork
# replace the current process by the execution of script1.s, only executed in child
exec script1.s
# display the scheduler status
print_status
```

Ce deuxième exemple, après une période de calcul de 500 cycles, crée un processus qui exécutera à son tour le programme `script1.s`, avant d'afficher l'état du simulateur, et de terminer.

+++

## Le rôle d'un scheduler

+++

Naturellement un seul processeur n'est capable de traiter qu'un seul processus à la fois. Mais alors lorsque plusieurs programmes sont exécutés en même temps dans un ordinateur, que se passe-t-il d'après vous ?

Plusieurs stratégies sont possibles :

1. la plus triviale : le scheduler exécute les programmes les uns après les autres, et il termine complètement l'exécution de l'un avant de commencer à exécuter l'autre

1. un peu mieux : le scheduler distribue l’utilisation du processeur entre les programmes en leur allouant aléatoirement de petits créneaux de temps d’exécution

1. ..

Et bien afin de se rendre compte des mérites respectifs de toutes les méthodes de scheduling auxquelles vous pouvez penser, on vous propose de les programmer; c'est le but de ce TP.

+++

## Nos exigences pour vos schedulers

+++

### Exigence sur la simulation

+++

Le but de ces exercices est de faire une `simulation statique`. Cela va consister à exécuter le `processus initial` qui décrit la session complète du `boot` au `shutdown` de l'ordinateur simulé.

Ce processus initial va donc démarrer tous les processus que vous désirez exécuter; ces processus sont libres naturellement de démarrer à leur tour d'autres processus.

Cette simulation est statique: tous les programmes impliqués sont fixés dès le départ. On ne s'est pas donné les moyens de modifier les programmes au fil de l'eau ni d'en rajouter ou d'en enlever dynamiquement. Ainsi, il y a une certaine dose de déterminisme dans le sens où, quelle que soit la stratégie implémentée, on doit s'attendre à ce que le nombre de cycles nécessaire pour finir une simulation soit constant et calculable à l'avance.

+++

### Exigence sur les statistiques

+++

Notons que, comme le but de ces exercices sera d'évaluer plusieurs algorithmes de planification des taches, il faudra maintenir différentes statistiques, comme:
* le temps d'exécution réel, i.e. le nombre de cycles de base écoulés entre la création du processus et sa terminaison
* le nombre d'instructions exécuté par un processus
* la durée moyenne de temps d’exécution par rapport à la longueur du processus
* le nombre de changement de context par processus, i.e. le nombre de fois ou un processus est retiré du CPU ou remis pour son l'execution.

+++

### Exigence sur le code

+++

Je vous propose d’implémenter le simulateur en Python en implémentant une classe `Process` dont le but est de maintenir l’état d’un processus donné, comme la liste des instructions en attente, ou le numéro d’identification du processus.

Donc ouvrez votre éditeur `vs-code` avec un terminal pour interpréter votre code `Python` ou bien écrivez directement votre code dans ce notebook, et allez-y : créez la classe `Python` `Process`:

```python
class Process:
    pass
```

Ensuite je vous propose d’implémenter une classe `Scheduler` qui contiendra l’état du planificateur de taches, et qui sera chargé d’exécuter la simulation. Il sera judicieux de pouvoir dériver cette classe pour implémenter d’autres algorithmes de planification de taches. Ceux qui ne savent pas dériver appellent un enseignant !

```python
class Scheduler:
    pass
```

Si vous choisissez d'écrire votre code dans un script, disons `simulation.py`, on s'attend à pouvoir lancer la simulation en tapant dans le terminal

```bash
python simulation.py le-programme-init.s
```

Si au contraire vous choisissez d'utiliser un notebook, on lancera la simulation en écrivant

```bash
s = Scheduler()
s.run("le-programme-init.s")
```

+++

## Simulation de la gestion de processus

+++ {"tags": []}

### Simulation de base

+++

Pour commencer le simulateur va simuler un système mono processeur, ce qui signifie qu’un unique processus sera en cours a chaque cycle simulé.

Pour cette première version ultra simplifiée du simulateur, on ignore les instructions `fork` et `exec`, et donc sans ces instructions on sait qu'on n'aura qu'un seul processus à gérer. 
Il s'agit principalement de mettre en place une première version simpliste, mais qui fonctionne.

Le simulateur commence par charger et créer le processus principal, qu'on appelle `init`.

Une fois ce programme chargé il va commencer à simuler les cycles, à chaque cycle le simulateur peut lire et interpréter une instruction, ou ne rien faire (le simulateur ne fait rien si une instruction `busy n`, du processus en cours a été lancée, c’est-à-dire que la simulation attend que les n cycles necessaire pour le `busy` soient effectivement réalisées).

Le simulateur, après $x$ cycles, lance une heuristique dont le but sera de choisir le prochain processus à exécuter : naturellement dans cette simulation de base, puisqu'on n'a au maximum qu'un seul processus en cours, cette heuristique est simple à écrire.

Le but de la simulation sera d’évaluer plusieurs algorithmes de planification des taches. N'oubliez pas de conserver les différentes statistiques dont nous avons parlé dans les exigences.

+++

### Simulation avec création de sous-process `fork`  et `exec`

+++

On vous rappelle qu'il s’agira de faire une simulation *statique* consistant à lancer un unique programme qui se chargera de lancer d’autres sous-programmes grâce aux appels système `fork` et `exec`.

Notre simulateur est vraiment simple actuellement (il simule un unique programme) nous allons donc complexifier le simulateur en lui ajoutant la capacité de créer de nouvelles taches. Pour ce faire nous allons ajouter les deux instructions qui sont `fork` et `exec`.

Mais il faut bien comprendre quelque chose qui ressemble à la poule et l'oeuf. Suivez moi:
   - pour que le process fils réalise un programme différent de celui de son père, il doit faire un `exec`, qui apparaît donc après le `fork`
   - comme le code du process fils est exactement le même que le code du process père, cet `exec` apparaît donc dans le code du process père
   - ... vous commencez à comprendre
   - si vous ne voulez pas que le père se mette aussi à exécuter l'`exec` il faut lui donner la possibilité de sauter un certain nombre de lignes de code lors du `fork`

Donc:
* `fork n` copie le processus actuel, incluant l’état du processus actuel, et le programme parent ignore `n` instructions, le processus crée continue, lui à l’instruction suivante.
* `exec filename` remplace le processus par le processus `filename`. Cette instruction lit les instructions du fichier de nom *filename*, et remplace les instructions en cours par ces dernières. Le flux d’exécution est réinitialisé pour commencer à la première instruction du ficher chargé.

Voila vous devez maintenant réaliser une scheduler qui prenne en compte `fork+exec` mais dans une première version, lorsque l'exécution d'un programme est commencée, le programme s'exécute jusqu'au bout. Attention lors de l'ecriture de `fork n` de ne pas compté les lignes vides et les commentaires. n fait il n'y a pas de scheduling. Allez-y !

Maintenant que votre scheduler super-basique fonctionne, vous vous posez et vous réfléchissez. Quels sont les défauts de cette stratégie ? Oui le $n^{ème}$ process lancé va attendre que les $n-1$ premiers process aient terminé avant d'accéder pour la première fois au processeur et oui il trouve ca super injuste ! Le scheduler ne pourrait-il pas offrir une stratégie plus juste aux process qu'il doit exécuter ? L'idée est là de partager une ressource (le processeur) de manière plus juste, donc de ne pas laisser le process en cours d'exécution terminer complètement tout son programme, mais de l'interrompre. Voila, vous pouvez laisser libre à votre imagination ! et implémenter et comparer toutes les stratégies que vous voulez.

Nous vous rappelons de calculer les statistique utiles :
- le temps réel d’exécution: la différence de temps entre le moment ou le programme se termine et le moment ou le programme a été créé. Note : c'est le moment du fork ou l'instant 0 pour le premier processus.
- le temps d’exécution réel moyen: la moyenne de l'indicateur précédent pour tous les processus
- le taux d’usage du CPU, i.e. le temps où le CPU a effectivement réalisé l’instruction busy d’un programme, par rapport au temps total.
- le nombre de changement de context par processus, i.e. le nombre de fois ou un processus est retiré du CPU ou remis pour son l'execution.

+++

Vous devez arriver à cette précédente étape pour que le mini-projet vous ait appris les bases que nous souhaitions.

+++ {"tags": ["level_intermediate"]}

Note: Le choix d’utiliser `fork` et `exec` plutôt qu’une seule instruction est assez arbitraire, mais elle est plus flexible qu’une instruction unique `exec` qui ferait `fork+exec` car dans certains contextes, un simple `fork` est beaucoup plus efficace que de recharger le programme complet.

Par exemple un programme comme `apache`, qui est un serveur `HTTP/HTTPS`, va démarrer, puis charger sa configuration et ensuite réaliser un `fork` afin de pouvoir servir des requêtes en parallèle. Cette méthode est bien plus efficace que de devoir recharger le programme depuis zéro. Le `fork` utilisé de cette manière est un intermédiaire aux threads que nous décrirons au second semestre.

+++ {"tags": ["level_advanced"]}

# Pour aller plus loin dans le mini-projet

+++ {"tags": ["level_advanced"]}

Le simulateur a pour but d’analyser différents planificateurs de taches, nous vous avons invités à implémenter plusieurs algorithmes de planification, et à en inventer. Par exemple le premier trivial consiste a exécuter la tache courante jusqu’à sa terminaison, une fois terminé on prend le suivant dans la liste...

Mais d'autres scenarii peuvent être testés, en particulier la plupart des programmes peuvent être classés en deux catégories, les programmes limités par les entrées/sorties, et les programmes limités par la capacité de calcul. Les programmes de la première catégorie ont un ratio de wait/busy élevé, et ceux du second ont un ratio de busy/wait élevé. Donc il est judicieux de tester le comportement des différents algorithmes dans les deux cas extrêmes, l’un avec une grosse majorité de processus limités par les I/O, et un autre avec une grosse majorité de processus limités par la capacité de calcul.

+++ {"tags": ["level_advanced"]}

## Simulation des I/O

+++ {"tags": ["level_advanced"]}

Les I/O dans l’ordinateur sont les instructions d’entrées-sorties, qui consistent:
* à attendre que des données d’entrées soit reçues, comme par exemple, des données en provenance d’une clef USB;
* à attendre que des données soit envoyées vers des périphériques, comme par exemple le réseau.

Durant ces périodes d’I/O le programme est bloqué et ne peut plus faire de calcul. Pour simuler ces I/O nous allons ajouter une instruction `wait n` qui consistera à attendre `n` cycles.

Contrairement à l’instruction `busy`, cette instruction ne consomme **pas de cycle de calcul** et donc les processus qui sont en train d'exécuter l’instruction `wait` sont juste bloqués pour `n` cycles, il peut donc y avoir plusieurs processus bloqués en même temps.

+++ {"tags": ["level_advanced"]}

## Simulation des processus coopératifs

+++ {"tags": ["level_advanced"]}

Le système de planification peut proposer un système de coopération afin de permettre au programme de se partager les ressources du CPU. Pour se faire on peut ajouter une instruction pause, dont le but est d’informer le planificateur de taches que c’est un bon moment pour exécuter une autre tache.
__Note:__ ce système était le système utilisé pour les programmes DOS.

+++ {"tags": ["level_advanced"]}

## Simulation d’un planificateur préemptif

+++ {"tags": ["level_advanced"]}

Implémenter une simulation telle que le planificateur peut interrompre un processus à tout moment pour le remplacer par un autre.

+++ {"tags": ["level_advanced"]}

## Gestion de priorité

+++ {"tags": ["level_advanced"]}

Dans la vraie vie tous les programmes ne sont pas égaux, par exemple le programme qui fait la lecture d’un film ou d’une musique doit avoir accés à assez de ressources pour afficher une video fluide ou un son continu. De même, le programme qui effectue les sauvegardes est probablement plus prioritaire que le programme qui charge les e-mails. Pour prendre en compte ces différences on va ajouter un système de priorité avec l’instruction renice n, n étant un nombre représentant la priorité d’un processus. Historiquement les valeurs les plus basses représente les priorités les plus élevées.

+++ {"tags": ["level_advanced"]}

## Simulation de plusieurs processeurs

+++ {"tags": ["level_advanced"]}

Jusqu’à maintenant notre simulateur ne simule qu’une file d’exécution, mais dans les ordinateurs modernes, plusieurs files d’exécution sont disponibles, i.e. plusieurs unités de calcul.

+++ {"tags": ["level_advanced"]}

## Simulation de la mémoire

+++ {"tags": ["level_advanced"]}

Le système d’exploitation est également chargé d’attribuer de la mémoire aux différents programmes. Le but de cette section est d’inventer un algorithme de gestion de la mémoire, et d’attribuer la mémoire aux différents processus. On suppose pour le moment que le système d’exploitation dispose de N cases mémoires, chaque case mémoire contenant un espace mémoire fixé, habituellement 8 bits, 1 octet. Tout les programmes partagent le même espace mémoire, et se voient attribuer un sous ensemble de cet espace. Chaque case mémoire est numérotée de 0 a N-1, et une même case ne peut être attribuée à plusieurs processus, afin d’assurer le bon fonctionnement de chaque programme. À noter que dans cette configuration un programme mal intentionné peut accéder et modifier la mémoire des autres programmes. Pour le faire, il faudra ajouter les instructions suivantes au simulateur :

* Alloc n, alloue de la mémoire continue X to X+n
* Dealloc n, désalloue le n ème block mémoire alloué (xxx n-ième dans quel sens ?)

+++ {"tags": ["level_advanced"]}

### Simulation de la mémoire virtuelle

+++ {"tags": ["level_advanced"]}

Cette partie va consister à améliorer l’allocation précédente, et de simuler en supposant maintenant que l’on est capable d’isoler les processus dans leurs espace mémoire distinct. Le principe maintenant est de maintenir pour chaque processus la correspondance entre l’adresse physique et l’adresse virtuel du processus.

+++ {"tags": ["level_advanced"]}

### Simulation de l’accès Mémoire

+++ {"tags": ["level_advanced"]}

Ajout des instructions Read n, Write n.

+++ {"tags": ["level_advanced"]}

### Simulation des accès aux disques

+++ {"tags": ["level_advanced"]}

Ajout des instruction OpenFile, ReadFile n, WriteFile n, CloseFile :

* OpenFile filename, ouvre un fichier de manière anonyme, les fichiers sont numérotés par ordre d’ouverture,
* ReadFile n, lit n éléments d’un fichier ouvert
* WriteFile n, écrit n élément d’un fichier ouvert
* CloseFile n, ferme le n-ème fichier ouvert.

+++ {"tags": ["level_advanced"]}

### Disable WriteFile concurency

+++ {"tags": ["level_advanced"]}

Remplace WriteFile par :

WriteFile n m, qui écrit m octets dans le n-eme fichier.

L’écriture concurrente est désactivée, si un processus écrit dans un fichier les autre programmes ne peuvent pas lire dans ce fichier.

+++ {"tags": ["level_advanced"]}

### Simulation du SWAP

+++ {"tags": ["level_advanced"]}

Permettre à l’allocation de mémoire de mettre les données d’un processus sur le disque. Attribuer un coût pour l’écriture des données sur le disque, et la lecture des données depuis le disque.

+++ {"tags": ["level_advanced"]}

## Simulation des signaux

+++ {"tags": ["level_advanced"]}

...


```python

```

+++ {"tags": ["level_basic"]}

# Annexe

+++ {"tags": ["level_basic"]}

## Les composants d’un ordinateur

+++ {"tags": ["level_basic"]}

Vous avez tout d'abord le **`CPU`** (Central Processing Unit). Puis les mémoires en enfin les périphériques.

+++ {"tags": ["level_basic"]}

### Le processeur ou `CPU` (Central Processing Unit) -

+++ {"tags": ["level_basic"]}

Le processeur (encore appelé CPU) exécute les instructions des programmes informatiques. Très schématiquement, pour faire cela, il doit récupérer *quelque part dans la mémoire* (les unes après les autres) les instructions qui forment un programme (`fetch`), il va les décoder (`decode`) et il va les *exécuter* (`execute`).

Ainsi, son `cycle de base` consiste à:

1. récupérer la prochaine instruction du programme `fetch`
1. la *décoder* `decode`
1. l'exécuter `execute`
1. ... et à recommencer jusqu'à la terminaison du programme.

+++ {"tags": ["level_basic"]}

Il va contenir:
* l'`unité de commande` qui s'occupe d'aller chercher les instructions à exécuter
* l'`unité arithmétique et Logique` qui s'occupe de réaliser les instructions trouvées par l'unité de commande
* des `registres`, des mémoires qui servent à stocker (des variables, résultats intermédiaires et autres informations de contrôle du processeur).

Notons que les registres, comme ils sont super proches des calculs, leur accès est très très rapide et donc les calculs aussi ! si on doit aller chercher une valeur dans une mémoire très très loin, c'est sûr que c'est beaucoup moins rapide...
<!img src="shrek-far-far-away.jpg" width=400>

+++ {"tags": ["level_basic"]}

Bien sûr, il faut bien que les informations arrivent et ressortent du `CPU`, il doit donc communiquer avec ses périphériques et il va le faire en utilisant des **`bus`**.

+++ {"tags": ["level_basic"]}

### les `bus`

+++ {"tags": ["level_basic"]}

Afin que les informations arrivent et repartent du `CPU`, il va communiquer avec ses périphériques (comme les mémoires, les entrées/sorties) en utilisant un système de **`bus`**.

* l'`address bus` qui transporte les informations concernant le device (l'appareil, le dispositif) avec lequel il veut communiquer
* le `data bus` qui transporte les données en cours de traitement
* le `command bus` qui transporte les commandes et renvoie les signaux indiquant l'état des devices

+++ {"tags": ["level_basic"]}

Et puis pour faire des calculs, il va bien falloir stocker les programmes et les données quelque part. C'est le rôle des différentes mémoires.

+++ {"tags": ["level_basic"]}

### les mémoires

+++ {"tags": ["level_basic"]}

Donc un autre composant très important d'un ordinateur est la **mémoire** et souvent, ce qui est lent dans un ordi, ce ne sont pas calculs mais les accès à la mémoire.

Idéalement:
1. l’accès à la mémoire  devrait être extrêmement rapide (pour que le processeur ne soit jamais bloqué en attente des données sur lesquelles il calcule)
1. la mémoire devrait être abondante
1. elle devrait être bon marché ...  
mais malheureusement aucune technologie actuelle ne satisfait ces trois objectifs (ce serait trop simple).

+++ {"tags": ["level_basic"]}

L'approche alternative qui a été adoptée est de doter les ordis d'une *hiérarchie* de mémoires. Les mémoires dans les couches supérieures ont une vitesse d'accès supérieure, une capacité inférieure et un coût (au bit) supérieur à ceux des couches inférieures et puis ca se dégrade (et nous parlons là de facteurs de dégradation qui peuvent dépasser le milliard i.e. le Giga).) jusqu'à arriver au disque dur (avec donc une vitesse d'accès très inférieure mais de très grosses capacités et très peu chers).

Dans la hiérarchie de mémoire, il y a les `registres`, les `mémoire cache`, la `mémoire principale` et des disques durs.

+++ {"tags": ["level_basic"]}

#### les registres

+++ {"tags": ["level_basic"]}

Les `registres` sont à l'intérieur du CPU, ils sont aussi rapides que le processeur, n'ont pas de délai d’accès mais des capacité inférieures à 1Ko. Ils vont contenir les données en cours de traitement par le CPU.

+++ {"tags": ["level_basic"]}

#### la mémoire cache

+++ {"tags": ["level_basic"]}

La `mémoire cache` et une mémoire très proche du CPU donc très rapide mais moins rapide que les registres. Elle permet de stocker des copies des données que vous accéder souvent afin de diminuer le temps des accès ultérieurs du CPU à ces données.

+++ {"tags": ["level_basic"]}

En gros, quand un programme doit lire une donnée en mémoire, il vérifie d'abord si elle ne serait pas dans le cache avant d'utiliser un bus pour aller la chercher plus loin.
 
Les techniques de cache jouent un grand rôle en informatique: à chaque fois qu'une ressource peut être divisée en morceaux dont certains sont beaucoup plus utilisé que d’autres, la mise en cache permet d’améliorer fortement les performances. Ceux qui rangent chez eux les objets les plus utilisés dans les endroit les plus difficiles d'accès ont sûrement des problèmes de cache !

+++ {"tags": ["level_basic"]}

#### la mémoire principale

+++ {"tags": ["level_basic"]}

La mémoire principale `RAM` (Random Access Memory) on l'appelle `la mémoire` (tout court). Et bien en gros, lors des calculs, toutes les demandes de stockage de données qui n’ont pas pu être satisfaites par le cache vont en mémoire RAM.

+++ {"tags": ["level_basic"]}

#### le disque dur (magnétique)

+++ {"tags": ["level_basic"]}

Les `disques durs` sont des appareils mécaniques où les informations sont inscrites sur des cercles concentriques, on parle de bras, de têtes, de cylindres, de secteurs, de variateurs de vitesse... que nous ne détaillerons surtout pas ici.

+++ {"tags": ["level_basic"]}

#### exercice à faire à-la-maison et pas pendant les cours

+++ {"tags": ["level_basic"]}

Voici des temps d'accès à ces différents types de mémoires. Ce ne sont que des ordres de grandeur très grossiers peut être complètement dépassés (vous corrigerez par vous-même mais pas pendant le cours SVP).

+++ {"tags": ["level_basic"]}

| Types | Temps d’accès | Capacité | Prix | 
|-------|---------------|----------|------|
|Registre | 1 nano-seconde | < 1 Ko (kilo-octet) | super chers |
| Cache | 2 nano-secondes | 4 Mo (Méga-octet) | très cher |
| RAM | 10 nano-secondes |  1-8 Go (Giga-octet) | cher |
| Disque dur | 10 milli-secondes | 1-4 To (Tera-octet) | peu cher |
| Internet | plusieurs secondes | *infinie* | *gratuit* |

+++ {"tags": ["level_basic"]}

1. Dans les temps d'accès donnés ci-dessus, remplacer la nano seconde par une seconde et dites, avec l'unité qui s'applique (seconde, heure, jour, mois, année), combien de temps il faut pour aller chercher une donnée dans chacun de ces stockage de données. Je vous donne le premier, il faut une seconde pour aller chercher une donnée dans un registre.

1. Remplacer les qualitatifs super chers, très cher, cher, peu cher par les prix au jour d'aujourd'hui

+++ {"tags": ["level_basic"]}

## *kernel space* et *user space*

+++ {"tags": ["level_basic"]}

Petit point de vocabulaire à nouveau : pour pouvoir assurer la différence de privilèges entre l'OS et les processus, Linux partitionne la mémoire en deux espaces, qu'on appelle 

1. *kernel space*, où réside le code du ***noyau*** de l'OS,
1. et *user space*, souvent appelé aussi *user-land*

Depuis le *kernel space*, on peut tout faire !

Le *code* utilisateur (y compris celui du super-utilisateur/administrateur/root), qu'on appelle aussi parfois les ***applications***, est lui logé dans le *user-land*, il est limité dans ses privilèges, et doit du coup demander certains services au noyau, au travers de ce qu'on appelle les *appels système*
