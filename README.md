# 🍞 Loaf
### *So bland yet so good!™*

Effortlessly access your SQL servers and procedures, plus some other utilities.



## Install

```
$ pip install loaf
```



## Sample Demo

```python
import loaf

# Setup your credentials with a single line.
loaf.bake(port=6969, db="pizzeria")

# Make a query easily.
result = loaf.query("SELECT * from toppings")
print(result)

# Not lazy enough? Try some of the pre-built queires.
result = loaf.all("toppings")
print(result)

# Got stored procedures? No problemo!
result = loaf.call("ProcedureFindClient", 1)
print(result)
```



![](https://github.com/PoshoDev/Loaf/blob/main/loaf.png?raw=true)

