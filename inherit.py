# pendant le cours d'introduction on n'a pas eu le temps de couvrir
# l'héritage et la dérivation des classes
#
# dans le contexte de cet exercice pourtant, c'est une technique
# qui peut s'avérer très utile
#
# voyons un exemple simplissime
#

class Scheduler:

    # dans la classe principale j'implémente un certaine logique
    # qui pour rester simple consiste à imprimer 3 fois de suite
    # 'quelque chose'
    def loop(self):
        # je simule une dizaine de pas
        for i in range(3):
            print(i, '->', self.something())

    def something(self):
        return None

# du coup, ceci écrit 3 fois 'None'
print(10*'=', "Scheduler") 
s = Scheduler()
s.loop()


# la dérivation ça consiste à définir une sous-classe de Scheduler
# et à redéfinir la méthode 'something'

import random

# pour dire que SchedulerNumbers est-une sous-classe
# de Scheduler, ça se passe ici
#
#                     ↓↓↓↓↓↓↓↓↓↓↓
class SchedulerNumbers(Scheduler):
    def something(self):
        return random.randint(0, 10)

# cette fois, je vais tirer trois fois au hasard un entier

print(10*'=', "SchedulerNumbers")
sn = SchedulerNumbers()
sn.loop()


# et je peux comme ça modifier à volonté un comportement spécifique
# tout en gardant (on dit en héritant) de la logique générale

class SchedulerFruits(Scheduler):
    def something(self):
        return random.choice(['apple', 'banana', 'pear'])
print(10*'=', "SchedulerFruits")
sn = SchedulerFruits()
sn.loop()
