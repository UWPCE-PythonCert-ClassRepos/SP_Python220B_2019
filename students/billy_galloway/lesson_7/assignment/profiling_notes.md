## Case study on adding threads
The current application takes a linear approach with no threading. As the database grows 
the application may become slower while reading and writing to the database. 

## Linear speed of 10 cycles
```
1.2 secs
1.2 secs
```
## Linear speed of 100 cycles
```
74 secs
65 secs
60 secs
```
## Linear 200 cycles
227 secs

## Linear 300 cycles
499 secs

## Threaded 10 cycles
```
0.8 secs
0.9 secs
```
## Threaded 100 cycles
```
59 secs
68 secs
56 secs
```
## Threaded 200 cycles
218 secs

## Threaded 300 cycles
483 secs

So far the improvements are faster, but not fast enough to warrant refactoring and threading the read and write operations. 
