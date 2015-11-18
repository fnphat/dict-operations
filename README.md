Data Dictionary Operations Tool
===============================

Description
-----------
This tool can apply set operations to data dictionaries. It can do basic set operations: union, intersection, difference and symmetric difference between two data dictionaries. Since a dictionary contains key-value pairs, only the keys will be used to do the set operations, with one dictionary's values having priority over the values of the other dictionary involved, when using the union and the intersection operations.

For more information, please have a look at some reference pages: 
- [Data dictionary](https://en.wikipedia.org/wiki/Associative_array)
- [Set operations](https://en.wikipedia.org/wiki/Set_(mathematics)#Basic_operations)

Usage
-----
### Union
To do a union operation between dictionary A and dictionary B, noted A | B, values of A having priority over B:
```
#> cat dict_A.json | python dict-ops-tool.py union dict_B.json > dict_C.json
```
Note: A | B != B | A

### Intersection
To do an intersection operation between dictionary A and dictionary B, noted A & B, values of A having priority over B:
```
#> cat dict_A.json | python dict-ops-tool.py inter dict_B.json > dict_C.json
```
Note: A & B != B & A

### Difference
To do a difference operation between dictionary A and dictionary B, noted A - B:
```
#> cat dict_A.json | python dict-ops-tool.py diff dict_B.json > dict_C.json
```

### Symmetric difference
To do a symmetric difference operation between dictionary A and dictionary B, noted A ^ B:
```
#> cat dict_A.json | python dict-ops-tool.py symdiff dict_B.json > dict_C.json
```

License
-------
Please have a look at the LICENSE file for more info on what is permitted to do with this code.


