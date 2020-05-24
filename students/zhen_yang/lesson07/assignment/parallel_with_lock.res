         3146 function calls (3051 primitive calls) in 67.730 seconds

   Ordered by: cumulative time
   List reduced from 380 to 20 due to restriction <20>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000   67.730   67.730 parallel_with_lock.py:51(import_thousand_data)
       61   67.713    1.110   67.713    1.110 {method 'acquire' of '_thread.lock' objects}
        3    0.000    0.000   67.709   22.570 threading.py:1012(join)
       16    0.000    0.000   67.709    4.232 threading.py:1050(_wait_for_tstate_lock)
        8    0.000    0.000    0.009    0.001 __init__.py:1368(info)
        8    0.000    0.000    0.009    0.001 __init__.py:1491(_log)
        8    0.000    0.000    0.008    0.001 __init__.py:1516(handle)
        8    0.000    0.000    0.008    0.001 __init__.py:1570(callHandlers)
        8    0.000    0.000    0.008    0.001 __init__.py:881(handle)
        8    0.000    0.000    0.008    0.001 __init__.py:1013(emit)
        8    0.008    0.001    0.008    0.001 {method 'write' of '_io.TextIOWrapper' objects}
        6    0.000    0.000    0.006    0.001 collection.py:1315(count)
        6    0.000    0.000    0.006    0.001 collection.py:1302(_count)
        6    0.000    0.000    0.004    0.001 threading.py:264(wait)
    55/18    0.000    0.000    0.004    0.000 {built-in method builtins.next}
       12    0.000    0.000    0.004    0.000 mongo_client.py:848(_socket_for_reads)
     24/6    0.000    0.000    0.004    0.001 contextlib.py:107(__enter__)
        5    0.000    0.000    0.004    0.001 threading.py:834(start)
       12    0.000    0.000    0.004    0.000 mongo_client.py:821(_get_socket)
        7    0.000    0.000    0.003    0.000 network.py:48(command)


