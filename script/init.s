# on commence à travailler
busy 10

# on lance un exemplaire du programme test0.s
# qui va tourner tout seul en même temps que nous
# (enfin si le scheduler est "fair")
fork 1
exec script/test0.s

# un 2-ème test0.s
fork 1
exec script/test0.s

# à ce stade on a dépensé :
# 10 pour busy 10
# 2 pour 2 x fork
# 2 pour 2 x exec 
# ---
# 14

# où en est-on ?
print_status

# un 3-ème test0.s
fork 1
exec script/test0.s
# un 4-ème test0.s
fork 1
exec script/test0.s

# on finit par un temps de calcul de 1000 cycles en propre
busy 1000

# où en est-on ?
print_status
