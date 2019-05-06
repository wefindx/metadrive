import metadrive

def test_read_table():
    drive = metadrive.drives.get('table-driver:default')
    from table_driver.api import Row

    expect = {'x': 1, 'y': 2, 'z': 3,
              '-': 'metadrive/tests/sample.csv#0',
              '@': 'PyPI::table-driver==0.0.3:default.api.Row'}

    result = Row._get('metadrive/tests/sample.csv#0', drive=drive)

    assert result['@'].startswith('PyPI::table-driver')
    assert result['@'].endswith('default.api.Row')

    del expect['@']
    del result['@']
    assert expect == result

