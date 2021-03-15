<img src="http://www.math.univ-toulouse.fr/~besse/Wikistat/Images/Logo_INSAvilletoulouse-RVB.png" style="text-align:right; float:left; max-width: 40px;margin:0px auto 0px auto; display: inline" alt="INSA"/>

# Jobshop

Introduction
---

Le problème de job shop est un problème d'optimisation combinatoire complexe. La taille de l’arbre de recherche “explose” lorsque la taille du problème augmente.
Lors des cours de PLNE et PPC, nous avons étudié les méthodes exactes; ou comment limiter l’explosion combinatoire en structurant et en élaguant l' arbre recherche. La solution trouvée était la solution optimale.

Ici, on va s'intéresser aux méthodes approchées, qui font des impasses sur l’arbre de recherche et ne garantissent pas l’optimalité de la solution trouvée.
Nous trouverons une solution réalisable, mais pas forcément optimale.
L’objectif avec ces méthodes est de garder une complexité raisonnable tout en trouvant une “bonne” solution.
On utilise des heuristiques pour se guider vers les zones de l’espace de recherche qui semblent les plus prometteuses.

La qualité d’une méthode approchée est évaluée en comparant la qualité des solutions obtenues pour un temps de calcul donné.

Lors de ce projet nous avons implémenté et évalué différentes méthodes approchées, nous les avons comparées entre elles et avec une méthode exacte (celle réalisée en TP de PPC).



Implémentation du projet
---

Pour utiliser ce projet, la première chose à faire est de le cloner. Ensuite, une fois qu'Anaconda 3 est intallé, il vous 
faut créer un nouvel environnement virtuel Python 3.7 :
```
conda create -n jobshop_env python=3.7
```

Une fois que l'environnement est prêt, installez les librairies qui sont nécessaires pour le projet. Dans le cas où vous
n'utiliserez que les méta-heuristiques, n'installez pas la librairie DOCPLEX.
```
pip install -r requirements.txt
```
Dans le cas où vous voulez aussi utiliser les méthodes exactes, installez-la, puis installez toutes les librairies qui 
vont avec dans votre nouvel environnement virtuel Python :
```
pip install -r requirements_cplex.txt
```


Exécution du code
---

Pour lancer notre code, lancer le script à partir d'un ide ou d'une commande Python :
```
cd scripts
.../scripts> python main.py
```

Plusieurs arguments sont disponibles pour lancer le script :
- Possibilité de trouver une méthode exacte à l'aide de DOCPLEX (vous ne pourrez l'utiliser que si vous avez DOCPLEX et
que votre environnement Python contient `requirements_cplex.txt`)
- Possibilité d'utiliser plusieurs instances à la fois.
- Possibilité de créer un Excel qui récapitule les résultats obtenus.

Dans ce projet, il existe de nombreuses possibilités (plus que ce que nous avons déjà citées) que vous pourrez obtenir 
en utilisant les arguments parser, tel que :
```
python main.py --exact True --instance ft06 ft20 --descent True
```
Vous pouvez obtenir des informations sur les arguments grace au help en tappant :
```
python main.py -h
```

Documentation argument parser
---
La documentation permet de voir l'étendue des possibilité à travers les arguments parser
```
optional arguments:
  -h, --help            show this help message and exit
  --instance INSTANCE [INSTANCE ...]
                        Instances list
  --gantt GANTT         Draw Gantt chart
  --descent DESCENT     Add descent solver after 'gloutonne' methods
  --taboo TABOO         Add taboo solver after 'gloutonne' methods
  --timeout TIMEOUT     Parametrize the timeout for descent and taboo methods
  --iter ITER           Parametrize the maximum number of iteration for the
                        taboo method
  --time_taboo TIME_TABOO
                        Parametrize the number of iteration during the inverse
                        permutation is forbidden for the taboo method
  --excel EXCEL         Specify the name of the Excel filename (and False if
                        you don't want the file generation
  --exact EXACT         Specify if you want the exacte solution from DOCPLEX
```


