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


Exécution
---

Pour lancer notre code, il faut *** :
```
main ...***
```

Un fichier excel sera créé avec un recapitulatif des résulats obtenus.
Vous pouvez obtenir des informations sur les arguments grace au help ***

Si vous souhaiter obtenir des graphes sur l'évolution de la descnete ou un diagramme de Gantt d'une solution, vous pouvez ...***


