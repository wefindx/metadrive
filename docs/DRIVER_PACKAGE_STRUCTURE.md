# Driver package structure

```
.
├── driver_name
│   ├── __init__.py   # _login(), and an items generator function _harvest()
│   └── api.py        # classes, that define methods _get() and _filter() generators.
├── README.md
└── setup.py
```

## Defualt files structure

```
__init__.py file:
=====================
 _login(): authentication function

 _harvest(): default downloading function

api.py file:
============
 Classes represent data types available in data source of driver package.
 Methods represent way to query for objects in the data source.

 @classmethod
 _filter(): Returns a generator of the objects of the class.

 @classmethod
 _get(): Returns a method to retrieve a single object.

 @classmethod
 _update(): A method to update or delete the object in source by ID.
```

1. Publish drivers on `PyPI`.

2. Reference them on `-` wikis on GitHub (example: [https://github.com/mindey/-/wiki/topic#halfbakery](https://github.com/mindey/-/wiki/topic#halfbakery).

3. Use, like `harvest https://github.com/mindey/-/wiki/topic#halfbakery -o my_data`.

Alternatively, to database:
`harvest https://github.com/user/-/wiki/concept\#source --db mongodb://username:password@hostname:27017/db_name/collection`

More advanced usage will be covered in the future.
