<img src="http://www.math.univ-toulouse.fr/~besse/Wikistat/Images/Logo_INSAvilletoulouse-RVB.png" style="text-align:right; float:left; max-width: 40px;margin:0px auto 0px auto; display: inline" alt="INSA"/>

# Jobshop

Implémentation du projet
---

Pour utiliser ce projet, la première chose à faire ets de le cloner. Ensuite, une fois qu'Anaconda 3 est intallé, il vous 
faut créer un nouvel environnement virtuel Python 3.7 :
```
conda create -n jobshop_env python=3.7
```

Une fois que l'environnement est prêt, installez les librairies qui sont nécessaires pour le projet.
```
pip install -r requirements.txt
```


Introduction
---

La réalisation projet industriel d'un projet industriel nécessite souvent une succession de tâches auxquelles s'attachent 
trois types de contraintes :
- Des contraintes de temps relatives aux délais à respecter pour l’exécution des tâches.
- Des constraintes d’antériorité, c'est à dire que certaines opérations doivent s’exécuter avant d’autres.
- Des contraintes de production qui concernent le  temps  d’occupation  des machines.

Dans le cadre de notre TP,  le temps ne sera pas une contrainte mais plutôt l'objectif. L'objectif de ce projet
sera donc de minimiser le temps pour réaliser le projet.

Le projet en question est découpé en *tâches* et en *opérations*. Il existe plusieurs tâches dans un projet, une tâche comporte
une liste d'opérations dans laquelle chaque opérations est réalisée par une ressource (ou machine) différente. Une tâche
nécessite un nombre d'opérations égal au nombre de machines. Une tâche est une entité élémentaire caractérisée par une durée
et qui peut s'exécuter seulement sur une seule machine définie. Les opérations d'une doivent s'exécuter de manière
chronologique, c'est à dire que chaque opération doit être exécuter après l'opération qui la précède dans la tâche.


Dans ce TP, nous avons donc fait face à un problème d'ordonnancement lié à l'industrie. Pour représenter et comprendre ces 
problèmes d'ordonnancement, nous avons utilisé le *diagramme de Gantt* et la *méthode PERT* (Program Evaluation and Research 
Task).


D’une manière générale, les problèmes d’ordonnancement d’ateliers étant des problèmes combinatoires difficiles, il 
n’existe pas de méthodes universelles permettant de résoudre tous les cas. 
Plusieurs méthodes peuvent être utilisées pour résoudre un problème d’ordonnancement mais tous ne sont pas équivalentes :
- Les méthodes exactes permettent des approches correctes et complétes mais ont le désavantage de présenter une complexité
exponentielle sur des problème de grande taille.
- Les méthode approchées permettent de gagner du temps en n'explorant qu'une partie de l'espace de recherche mais le 
désavantage est que ce type de méthode ne retourne qu'un optimum local.

Puisque certaines instances de projet sont de taille très grande, nous avons préféré utiliser lors de ce TP des méthodes 
approchées guidées par des heuristiques, c'est à dire que ce sont des solutions correctes mais sans garantie de l'optimalité.
Nous avons essayé d'implémenter deux grands types de méthodes approchées qui sont :
- Les méthodes "constructives" dans lesquelles figurent les méthodes gloutonnes.
- Les méthodes de recherche locale dans lesquelles figurent les méthodes de descente.

