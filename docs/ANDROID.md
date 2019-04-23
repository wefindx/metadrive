# Android

If installed on Termux (Android), needs:

```
pkg i clang
pkg i make
pkg i python-dev
pkg i libcrypt-dev
pkg i libffi-dev
pkg i openssl
pkg i openssl-dev
pkg i openssl-tool
pkg i libjpeg-turbo-dev
LDFLAGS="-L/system/lib/" CFLAGS="-I/data/data/com.termux/files/usr/include/" pip install Pillow
OR LIBRARY_PATH="/system/lib" CPATH="$PREFIX/include" pip install pillow
```
