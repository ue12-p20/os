# un exemple de code pour montrer comment passer un paramètre
# à un script Python sur la ligne de commandes
#
# typiquement ici on vous demande d'écrire un script qui s'utilise en tapant
# $ simulateur.py le-programme.s
# dans la console
#
# et la question est, comment récupérer ce paramètre 'le-programme.s' dans mon programme Python
#

# deux approches pour ça

# première approche - simple, basique, un peu limitée

import sys
print(sys.argv[1])

# lancez
# $ args.py turlututu
# pour voir le résultat
#
# attention toutefois, si maintenant vous tapez seulement
# $ args.py
# cette fois ça se passe mal, il faudrait vérifier que sys.argv contient assez d'éléments...

# deuxième approche
#
# pour les élèves plus avancés, sachez que personne n'utilise sys.argv dans la vraie vie
# on utilise plutôt le module argparse (cherchez dans la doc)
#
# mais pour cet exercice la première méthode suffit bien
