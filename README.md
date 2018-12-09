# Metadrive

The package that introduces simple generic interfaces to the objects within web APIs, allowing for generation (searching), and management of items on the web systems.

The drivers shall define clients for [metaform](https://pypi.org/project/metaform/).

`$ harvest <resource>`
The first command allows to crawl custom source.

`$ provide`
The second command serves the API to the APIs and data.

Use `pip install --editable .` to preview changes to the commands.

# TODO

# Social information services

## Products
1. Taobao
2. 天猫
3. Alibaba
4. Amazon
5. EBay

## Business data
￼
1. Flights ( flightradar24.com )
2. Skyscanner ( skyscanner.com )
3. Weather ( windy.com )
4. Human ( biodigital.com )
5. Ships ( marinetraffic.com )
6. Deaths ( https://www.cdc.gov/nchs/data_access/vitalstatsonline.htm )
7. Companies ( opencorporates.com, etc.)
8. Oil Miners ( http://aleph.openoil.net/ )
￼
## Common services
1. Gmail API ( get all your mails )
2. LinkedIn
3. Google Plus
4. Twitter
5. Weibo
6. Telegram
7. WeChat
8. Kik
9. KakoTalk
10. Line
11. WhatsApp

## Common
1. Quora
2. Kr36
3. MeetUp
4. 知乎
5. Huodongxing

## Video
1. YouTube
2. YouKu
3. Vimeo

# Industrial and Medical Equipment

## Metal printers

- [https://www.aniwaa.com/best-of/3d-printers/best-metal-3d-printer/#The_best_metal_3D_printers_in_2018](https://www.aniwaa.com/best-of/3d-printers/best-metal-3d-printer/#The_best_metal_3D_printers_in_2018)

## CNC Machines

**Note:** [https://github.com/Nikolay-Kha/PyCNC#readme](https://github.com/Nikolay-Kha/PyCNC#readme)

- [https://mmi-direct.com/machines/search/?make_id=&page=brand](https://mmi-direct.com/machines/search/?make_id=&page=brand)

## Development
Add `~/.pypirc` file:

```
[distutils]
index-servers =
  pypi
  internal

[pypi]
username:<your_pypi_username>
password:<your_pypi_passwd>

[internal]
repository: https://pypi.wefindx.io
username: <wefindx_pypi_username>
password: <wefindx_pypi_passwd>
```

Then, use:
`python setup.py sdist upload -r internal`

Or also, use:
`pip install -i https://pypi.wefindx.io metadrive`


And then, `requirements.txt` may look like so:
`
metadir==0.0.1
--extra-index-url https://<wefindx_pypi_passwd>@ypi.wefindx.io/<wefindx_pypi_username>/
metadrive==0.4.0
`
