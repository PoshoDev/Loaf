# 🍞 Loaf
### *So bland yet so good!™*

Effortlessly access your SQL servers and procedures, plus some other utilities.



## Install

```
$ pip install loaf
```



## Examples

### Importing Into Your Project

```python
from loaf import Loaf
```



### Setting Up Credentials

```python
# Setup your credentials with a single line.
loaf = Loaf(port=6969, db="pizzeria")
# Or load your credentials from a file.
loaf = Loaf(file="creds.ini")
# Or use a local SQLite file instead.
loaf = Loaf(file="pizzeria.db")
```



### Executing Queries

```python
# Make queries easily.
toppings = loaf.query("SELECT * from toppings")
# Load your quieries directly from files.
clients = loaf.query(file="getHappyClients.sql")
# Prevent disasters by executing multiple queries.
pepperoni_id, client_name = loaf.multi([
    "SELECT id FROM toppings WHERE name='Pepperoni'",
    "SELECT name FROM clients WHERE id=6"
])
```



### Printing

```python
# Display info using built-in tables!
loaf.print(pepperoni_id)
loaf.print(client_name)
loaf.print(toppings)
```

```powershell
┏━━━━┓
┃ id ┃
┡━━━━┩
│ 1  │
└────┘
┏━━━━━━━━━━━┓
┃ name      ┃
┡━━━━━━━━━━━┩
│ 'Alfonso' │
└───────────┘
┏━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ id ┃ name        ┃ price ┃
┡━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1  │ 'Pepperoni' │ 1.49  │
│ 2  │ 'Mushrooms' │ 1.99  │
│ 3  │ 'Onions'    │ 0.99  │
└────┴─────────────┴───────┘
```



### Data Manipulation

```python
# Manipulate your data with dictionaries, as God intended.
for topping in toppings:
    print(topping['name'])
```

````powershell
Pepperoni
Mushrooms
Onions
````



### Utilities

```python
# Not lazy enough? Try some of the pre-built queires.
# Equivalent of: SELECT name FROM client WHERE name='Marco' LIMIT 1
result = loaf.select("name", "clients", "name='Marco'", limit=1)
# Get all values from a table.
result = loaf.all("toppings")
# Got stored procedures? No problemo!
result = loaf.call("ProcedureFindClient", 1)
```



![](https://github.com/PoshoDev/Loaf/blob/main/loaf.png?raw=true)



```
⚠️ Syntax for the package has changed heavily since version 0.2.0, if your project depends on Loaf and is using an inferior version, I heavily suggest that you use the previous stable version:
```

```
$ pip install loaf==0.1.30
```

