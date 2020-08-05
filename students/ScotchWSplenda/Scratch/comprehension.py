varvar = 3

for x in range(1, 101):
    if not x % varvar:
        print(x)

tt = [x for x in range(1, 101) if not x % varvar]
print(tt)
