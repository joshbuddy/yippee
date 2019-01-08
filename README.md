# Yippee

## Manage requirements.txt files

Using `requirements.txt` files makes it hard to distinguish between top-level dependencies and transient dependencies. In addition, separating out different dependencies for multiple environments is challenging. *Yippee* attempts to ease the pain by specifying a DSL by which `requirements.txt` files can be generated.

For example, with the following `yippee.py` file:

```python
from yippee import group, pip

pip("django", ">=2.1.0")

with group("production"):
    pip("postgres", "2.2.2")

with group("development"):
    pip("black")
```

This would generate:

`requirements.txt`

```
Django==2.1.5
pytz==2018.7
```

`requirements-production.txt`
```
-r requirements.txt
postgres==2.2.2
psycopg2-binary==2.7.6.1
```

and

`requirements-development.txt`

```
-r requirements.txt
appdirs==1.4.3
attrs==18.2.0
black==18.9b0
Click==7.0
toml==0.10.0
```

## Usage

Install yippee via pypi. Then you can run `yippee` to generate your `requirements.txt` files.
