# 🍞 Loaf
### *So bland yet so good!™*

Effortlessly access your MySQL server and procedures, plus some other utilities.



## Install

```
$ pip install Loaf
```



## Sample Demo

```python
import Loaf # Don't forget the uppercase 'L'!

# Setup your credentials with a single line.
Loaf.bake(port=6969, db="pizzeria")

# Make a query easily.
result = Loaf.query("SELECT * from toppings")
print(result)

# Not lazy enough? Try some of the pre-built queires.
result = Loaf.all("toppings")
print(result)

# Got stored procedures? No problemo!
result = Loaf.call("ProcedureFindClient", 1)
print(result)
```



![]()

