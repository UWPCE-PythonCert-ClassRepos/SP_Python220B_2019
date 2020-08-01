import itertools


with open('foo.csv', 'w') as f:
    listy = ['OBL', 'GJL', 'ZBL', 'SKS', 'CAT']
    f.write('\n'.join((str(seq)) for seq in itertools.permutations(listy)))


# use yield to iterate over
def nextSquare():
    i = 1
    while True:
        yield i*i
        i += 1


for num in nextSquare():
    if num > 100:
        break
    print(num)
