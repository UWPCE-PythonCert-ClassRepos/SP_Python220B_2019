         98304108 function calls (92804013 primitive calls) in 136.187 seconds

   Ordered by: cumulative time
   List reduced from 399 to 20 due to restriction <20>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000  136.186  136.186 linear.py:132(import_thousand_data)
        3    1.070    0.357  136.172   45.391 linear.py:38(read_thousand_csv_file)
   300000    2.813    0.000  131.885    0.000 collection.py:619(insert_one)
   300000    0.666    0.000   96.834    0.000 collection.py:555(_insert)
   300000    2.583    0.000   95.641    0.000 collection.py:517(_insert_one)
   300006    0.771    0.000   87.567    0.000 pool.py:373(command)
   300007    2.855    0.000   86.797    0.000 network.py:48(command)
   300007    1.214    0.000   42.591    0.000 network.py:134(receive_message)
   600014    1.448    0.000   40.968    0.000 network.py:160(_receive_data_on_socket)
   600014   39.392    0.000   39.392    0.000 {method 'recv' of '_socket.socket' objects}
2700061/1500024    2.106    0.000   25.790    0.000 {built-in method builtins.next}
   600012    1.111    0.000   24.063    0.000 mongo_client.py:821(_get_socket)
   300007    1.371    0.000   23.931    0.000 message.py:435(query)
   300007    0.607    0.000   18.736    0.000 __init__.py:949(encode)
900024/300006    1.009    0.000   18.247    0.000 contextlib.py:107(__enter__)
   300007    1.582    0.000   18.093    0.000 __init__.py:746(_dict_to_bson)
2300017/900008    2.791    0.000   14.527    0.000 __init__.py:731(_element_to_bson)
2600017/900008    2.027    0.000   12.161    0.000 __init__.py:698(_name_value_to_bson)
   600012    0.898    0.000   10.682    0.000 server.py:166(get_socket)
   300000    0.837    0.000   10.227    0.000 __init__.py:505(_encode_list)


