# 1 (in parent)
fork 1
# 1 (in child)
exec script/simple96.s
# 1
fork 1
# 1
exec script/simple96.s
# 1
fork 1
# 1
exec script/simple96.s
# 1
fork 1
# 1
exec script/simple96.s
# 8
busy 8

# total = 4x2 + 4 * 96 + 8 = 400