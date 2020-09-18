# this is to exercise fork 0

# 102 cycles
busy 102
# 1
print in dual 200 before forking
# 1 (in the parent only)
fork 0
# 96 = 2 x (47 + 1) 
busy 47
print dual 200 done

# total = 102 + 1 + 1 + 96 = 200
