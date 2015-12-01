Data Dictionary Operations Tool
===============================

Description
-----------
This tool can apply basic operations to data dictionaries: equality of keys, equality, intersection, difference,  merge, extract, and erase operations between two data dictionaries. Also, it can count the number of key-value pairs in a dictionary.

For more information, please have a look at some reference pages: 
- [Data dictionary](https://en.wikipedia.org/wiki/Associative_array)
- [Set operations](https://en.wikipedia.org/wiki/Set_(mathematics)#Basic_operations)

Usage
-----
### Count
Count the number of key-value pairs: the result will be a non-negative integer:
```
#> cat dict_A.json | python dict-ops-tool.py count
53
```

### Keys equality
'True' when all keys from dictionary A are in dictionary B and vice-versa, 'False' otherwise:
```
#> cat dict_A.json | python dict-ops-tool.py samekeys dict_B.json
True
```

### Dictionary equality
'True' when all key-value pairs from dictionary A are in dictionary B and vice-versa, 'False' otherwise:
```
#> cat dict_A.json | python dict-ops-tool.py same dict_B.json
False
```

### Intersection of dictionaries
Get the key-value pairs that are common to dictionary A and dictionary B:
```
#> cat dict_A.json | python dict-ops-tool.py inter dict_B.json > dict_C.json
```

### Difference of dictionaries
Remove key-value pairs from dictionary A that are in dictionary B:
```
#> cat dict_A.json | python dict-ops-tool.py diff dict_B.json > dict_C.json
```

### Merge dictionaries
Merge dictionaries: value in dictionary A have priority over value in dictionary B with the same key:
```
#> cat dict_A.json | python dict-ops-tool.py merge dict_B.json > dict_C.json
```
Note: merge(A, B) != merge(B, A)

### Extract key-value pairs
Extract key-value pairs from dictionary A for all keys that are in dictionary B:
```
#> cat dict_A.json | python dict-ops-tool.py extract dict_B.json > dict_C.json
```

### Erase key-value pairs
Erase key-value pairs from dictionary A for all keys that are in dictionary B:
```
#> cat dict_A.json | python dict-ops-tool.py erase dict_B.json > dict_C.json
```

License
-------
Please have a look at the LICENSE file for more info on what is permitted to do with this code.


