# Time stats for small, medium and large database

Initial runs were made on an empty database and all subsequent runs of the same job 
were ran on a populated database. 
Reads from the database seem to take around the same amount of time no matter the size of the database, as well as generating the data to enter into the database. 

The slowest component appears to be the importing of data ontop of a populated database. This seems to increase by 0.10 every 5000 entries. 


## Small inventory 1000 entries
Empty database first pass
```
INFO:csv_handler: Running csv reader
INFO:function_timer:Total time to run csv_reader  took: 0.012390
INFO:function_timer:Total time to run product_format  took: 0.000001
INFO:function_timer:Total time to run generate_document_list  took: 0.014549
INFO:csv_handler: Running csv reader
INFO:function_timer:Total time to run csv_reader  took: 0.009779
INFO:function_timer:Total time to run customer_format  took: 0.000001
INFO:function_timer:Total time to run generate_document_list  took: 0.012506
INFO:csv_handler: Running csv reader
INFO:function_timer:Total time to run csv_reader  took: 0.009009
INFO:function_timer:Total time to run rentals_format  took: 0.000001
INFO:function_timer:Total time to run generate_document_list  took: 0.010627

INFO:function_timer:Total time to run import_data  took: 0.130851

INFO:function_timer:Total time to run show_available_products  took: 0.007111
INFO:function_timer:Total time to run show_rentals  took: 0.016399

total time to finish 0.156106
```

secondary run adding 1000 more entries
```
INFO:csv_handler: Running csv reader
INFO:function_timer:Total time to run csv_reader  took: 0.008088
INFO:function_timer:Total time to run product_format  took: 0.000001
INFO:function_timer:Total time to run generate_document_list  took: 0.010214
INFO:csv_handler: Running csv reader
INFO:function_timer:Total time to run csv_reader  took: 0.000721
INFO:function_timer:Total time to run customer_format  took: 0.000001
INFO:function_timer:Total time to run generate_document_list  took: 0.003403
INFO:csv_handler: Running csv reader
INFO:function_timer:Total time to run csv_reader  took: 0.000696
INFO:function_timer:Total time to run rentals_format  took: 0.000001
INFO:function_timer:Total time to run generate_document_list  took: 0.002094

INFO:function_timer:Total time to run import_data  took: 0.094426

INFO:function_timer:Total time to run show_available_products  took: 0.010909
INFO:function_timer:Total time to run show_rentals  took: 0.008337

total time to finish 0.11
```
## Medium sized dataset 5000 entries
Empty database
```
INFO:csv_handler: Running csv reader
INFO:function_timer:Total time to run csv_reader  took: 0.006018
INFO:function_timer:Total time to run product_format  took: 0.000001
INFO:function_timer:Total time to run generate_document_list  took: 0.011982
INFO:csv_handler: Running csv reader
INFO:function_timer:Total time to run csv_reader  took: 0.000777
INFO:function_timer:Total time to run customer_format  took: 0.000001
INFO:function_timer:Total time to run generate_document_list  took: 0.012425
INFO:csv_handler: Running csv reader
INFO:function_timer:Total time to run csv_reader  took: 0.000727
INFO:function_timer:Total time to run rentals_format  took: 0.000001
INFO:function_timer:Total time to run generate_document_list  took: 0.006041

INFO:function_timer:Total time to run import_data  took: 0.315034

INFO:function_timer:Total time to run show_available_products  took: 0.033317
INFO:function_timer:Total time to run show_rentals  took: 0.015258

total time to finish 0.36453089999999994
```
added 10000 more
```
INFO:csv_handler: Running csv reader
INFO:function_timer:Total time to run csv_reader  took: 0.008033
INFO:function_timer:Total time to run product_format  took: 0.000001
INFO:function_timer:Total time to run generate_document_list  took: 0.017648
INFO:csv_handler: Running csv reader
INFO:function_timer:Total time to run csv_reader  took: 0.000821
INFO:function_timer:Total time to run customer_format  took: 0.000001
INFO:function_timer:Total time to run generate_document_list  took: 0.012138
INFO:csv_handler: Running csv reader
INFO:function_timer:Total time to run csv_reader  took: 0.000830
INFO:function_timer:Total time to run rentals_format  took: 0.000001
INFO:function_timer:Total time to run generate_document_list  took: 0.006340

INFO:function_timer:Total time to run import_data  took: 0.406607

INFO:function_timer:Total time to run show_available_products  took: 0.059238
INFO:function_timer:Total time to run show_rentals  took: 0.041465

total time to finish 0.5082187
```

## Large sized dataset 10000 entries at a time
```
INFO:csv_handler: Running csv reader
INFO:function_timer:Total time to run csv_reader  took: 0.014557
INFO:function_timer:Total time to run product_format  took: 0.000001
INFO:function_timer:Total time to run generate_document_list  took: 0.027934
INFO:csv_handler: Running csv reader
INFO:function_timer:Total time to run csv_reader  took: 0.008129
INFO:function_timer:Total time to run customer_format  took: 0.000001
INFO:function_timer:Total time to run generate_document_list  took: 0.034463
INFO:csv_handler: Running csv reader
INFO:function_timer:Total time to run csv_reader  took: 0.096377
INFO:function_timer:Total time to run rentals_format  took: 0.000001
INFO:function_timer:Total time to run generate_document_list  took: 0.110561

INFO:function_timer:Total time to run import_data  took: 0.682761

INFO:function_timer:Total time to run show_available_products  took: 0.040845
INFO:function_timer:Total time to run show_rentals  took: 0.026080

total time to finish 0.7505569000000001
```
At around 40,000 entries it takes around 1.2 seconds to complete
```
INFO:csv_handler: Running csv reader
INFO:function_timer:Total time to run csv_reader  took: 0.016012
INFO:function_timer:Total time to run product_format  took: 0.000001
INFO:function_timer:Total time to run generate_document_list  took: 0.029217
INFO:csv_handler: Running csv reader
INFO:function_timer:Total time to run csv_reader  took: 0.008649
INFO:function_timer:Total time to run customer_format  took: 0.000001
INFO:function_timer:Total time to run generate_document_list  took: 0.034975
INFO:csv_handler: Running csv reader
INFO:function_timer:Total time to run csv_reader  took: 0.096751
INFO:function_timer:Total time to run rentals_format  took: 0.000001
INFO:function_timer:Total time to run generate_document_list  took: 0.111263

INFO:function_timer:Total time to run import_data  took: 1.024713

INFO:function_timer:Total time to run show_available_products  took: 0.160533
INFO:function_timer:Total time to run show_rentals  took: 0.096308

total time to finish 1.2824631
```
