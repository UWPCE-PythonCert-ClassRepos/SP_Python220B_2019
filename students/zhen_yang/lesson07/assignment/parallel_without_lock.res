         3146 function calls (3051 primitive calls) in 66.854 seconds

   Ordered by: cumulative time
   List reduced from 377 to 20 due to restriction <20>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000   66.853   66.853 parallel.py:51(import_thousand_data)
       61   66.841    1.096   66.841    1.096 {method 'acquire' of '_thread.lock' objects}
        3    0.000    0.000   66.833   22.278 threading.py:1012(join)
       16    0.000    0.000   66.833    4.177 threading.py:1050(_wait_for_tstate_lock)
        6    0.000    0.000    0.008    0.001 threading.py:264(wait)
        5    0.000    0.000    0.007    0.001 threading.py:834(start)
        5    0.000    0.000    0.007    0.001 threading.py:534(wait)
        6    0.000    0.000    0.006    0.001 collection.py:1315(count)
        8    0.000    0.000    0.005    0.001 __init__.py:1368(info)
        6    0.000    0.000    0.005    0.001 collection.py:1302(_count)
        8    0.000    0.000    0.005    0.001 __init__.py:1491(_log)
        8    0.000    0.000    0.005    0.001 __init__.py:1516(handle)
        8    0.000    0.000    0.005    0.001 __init__.py:1570(callHandlers)
        8    0.000    0.000    0.005    0.001 __init__.py:881(handle)
        8    0.000    0.000    0.005    0.001 __init__.py:1013(emit)
        8    0.004    0.001    0.004    0.001 {method 'write' of '_io.TextIOWrapper' objects}
    55/18    0.000    0.000    0.004    0.000 {built-in method builtins.next}
       12    0.000    0.000    0.004    0.000 mongo_client.py:848(_socket_for_reads)
     24/6    0.000    0.000    0.003    0.001 contextlib.py:107(__enter__)
       12    0.000    0.000    0.003    0.000 mongo_client.py:821(_get_socket)


