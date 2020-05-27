Testing:
The runtime test started with small databases (2-3 records) and increasing by a factor of 10 (to 10 million records). 

Conclusions:
The observed results were that the increases in the runtime were directly related to the increases in the size of the 
database and do not point to a bottleneck in the import_csv function.
