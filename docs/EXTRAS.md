# Extras

As a plugin, data normalization package is available, to use it, install:

```
pip install -U --extra-index-url https://pypi.wefindx.io/ metaform --no-cache
```

then, pass `?normalize=true` as URL parameter as part of `POST` requests. The data `results` key will be normalized.
