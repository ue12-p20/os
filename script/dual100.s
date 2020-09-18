# 1 cycle for the fork
fork 1
# 1 cycle for the exec (in the child, but still)
exec script/simple48.s
# 50
busy 50

# so if you simulate this as the entry point, you must end at cycle 100
# 1 + 1 + 48 (in the child) + 50 = 100