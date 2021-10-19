# 🍞 Loaf
### *So bland yet so good!™*

Effortlessly access your MySQL server and procedures, plus some other utilities.



## Install

This isn't a Python package yet so you'd need to do this very archaically for now, lmao.

You need to install the following:

```
$ pip install pymysql
$ pip install datetime
```

 Then simply download *LazyDB.py* and put it in your project's directory, then use the good ol' *import*:

```python
import Loaf
```



## Sample Demo

```python
import Loaf

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

