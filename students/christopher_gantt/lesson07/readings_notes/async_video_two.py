from types import coroutine

@coroutine
def nothing():
    yield 'yeilding nothing'
    return 'returned from nothing'

@coroutine
def count(num):
    for i in range(num):
        # print(f'{i} in count')
        yield f'count: {i}' #4
    return 'returned from count'

async def do_a_few_things(num=3, name='no_name'):
    for i in range(num):
        print(f'in the "{name}" loop for the {i}th time') #2
        from_await = await nothing() #3, calls count function
        print('value returned from await:', from_await)


daft = do_a_few_things(3, 'first one')
daft.send(None) #1
print('daft send None')


i = 0
while True:
    i+=1
    print(f"\n{i} time in the outer while loop") #5
    try:
        res = daft.send(i) #6, new loop 
        print('result of send:', res) 
    except StopIteration:
        print('the awaitable is complete')
        break
