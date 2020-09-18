# 1 (in parent)
fork 1
# 1 (in child)
exec script/dual200.s
fork 1
# 1
exec script/dual200.s
# 96
busy 96

# total = 2x2 + 4 * 200 + 96 = 500