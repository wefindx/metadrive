import io
import os
import bs4
import tqdm
import yaml
import json
import time
import urllib
import tarfile
import requests

from metadrive.config import KNOWN_DRIVERS


def auto_discover(refresh=True):
    '''
    Goes over all PyPI packages in existence, which end with "-driver" in their name
    and returns those which have __site_url__ in their package __init__.py file, as
    a mapping enabling the discovery of drivers for Internet sites.
    '''

    if os.path.exists(KNOWN_DRIVERS) and not refresh:
        site_drivers = yaml.load(open(KNOWN_DRIVERS).read(), Loader=yaml.Loader)
        return site_drivers

    print("Downloading PyPI ...")
    response = requests.get('https://pypi.org/simple/', stream=True)

    f = io.BytesIO()
    total_length = response.headers.get('content-length')
    if total_length is None:
        f.write(response.content)
    else:
        total_length = 10000000 #int(total_length)

        with tqdm.tqdm(total=total_length) as pbar:
            for data in response.iter_content(chunk_size=4096):
                pbar.update(len(data))
                f.write(data)

    bindata = f.getvalue()
    print("Done.")
    print("Reading package URLs ...")
    soup = bs4.BeautifulSoup(bindata, 'html.parser')
    links = soup.find_all('a')

    # packages known to be not a metadrive drivers
    ignore = [
        'https://pypi.org/simple/aquasystems-driver/',
        'https://pypi.org/simple/arun-cassandra-driver/',
        'https://pypi.org/simple/dlogg-driver/',
        'https://pypi.org/simple/dse-driver/',
        'https://pypi.org/simple/moxel-http-driver/',
        'https://pypi.org/simple/moxel-python-driver/',
        'https://pypi.org/simple/oceandb-elasticsearch-driver/',
        'https://pypi.org/simple/oceandb-mongodb-driver/',
        'https://pypi.org/simple/openstack-vim-driver/',
        'https://pypi.org/simple/osmosis-aws-driver/',
        'https://pypi.org/simple/osmosis-azure-driver/',
        'https://pypi.org/simple/osmosis-on-premise-driver/',
        'https://pypi.org/simple/pg-driver/',
        'https://pypi.org/simple/sensirion-shdlc-driver/',
        'https://pypi.org/simple/slipstream-libcloud-driver/',
        'https://pypi.org/simple/supy-driver/',
        'https://pypi.org/simple/wolphin-driver/',
        'https://pypi.org/simple/yb-cassandra-driver/',
    ]

    site_drivers = []

    # This is for retrieving setup.py details.
    from metadrive.utils import stdoutIO
    import setuptools
    def setup(**kwargs):
        print(json.dumps(kwargs))
    setuptools.setup = setup

    print("Looking for driver packages and reading __init__.py files ...")
    for link in tqdm.tqdm(links):
        if link.attrs['href'].endswith('-driver/'):

            name = link.text
            link = urllib.parse.urljoin('https://pypi.org', link.attrs['href'])

            if link in ignore:
                continue
            response = requests.get(link)
            if response.ok:

                if response.text:
                    soup = bs4.BeautifulSoup(response.content, 'html.parser')
                    versions = soup.find_all('a')

                    if versions:
                        last_version = versions[-1]
                        response = requests.get(last_version.attrs['href'])

                        try:
                            tar = tarfile.open(mode= "r:gz", fileobj = io.BytesIO(response.content))
                        except:
                            tar = None

                        if tar is not None:
                            # import pdb; pdb.set_trace()
                            for member in tar.getnames():

                                if member.endswith('driver/__init__.py'):
                                    content = tar.extractfile(member).read()
                                    if content:
                                        text = content.decode('utf-8')
                                        if text:
                                            for line in text.split('\n'):
                                                if '__site_url__' in line:
                                                    if '=' in line:
                                                        site = line.split('=',1)[-1].strip()[1:-1]
                                                        if site:
                                                            if site.startswith('http'):
                                                                domain = urllib.parse.urlparse(site).hostname
                                                            else:
                                                                domain = None

                                                            for member in tar.getnames():
                                                                if member.count('/') == 1:
                                                                    if member.endswith('/setup.py'):
                                                                        setup = tar.extractfile(member).read()
                                                                        if setup:
                                                                            info = setup.decode('utf-8')
                                                                            with stdoutIO() as s:
                                                                                exec(info)
                                                                            info = json.loads(s.getvalue())
                                                                        else:
                                                                            info = None

                                                            site_drivers.append(
                                                                {'site_url': site,
                                                                 'domain': domain,
                                                                 'package': name,
                                                                 'type': 'pypi',
                                                                 'info': info})
                                                    break
                                    break

    with open(KNOWN_DRIVERS, 'w') as f:
        f.write(yaml.dump(site_drivers, Dumper=yaml.Dumper))

    print("Saved to {}. Now you can use metadrive.drivers.all() to quickly access them.".format(KNOWN_DRIVERS))

    return site_drivers

def index():
    return auto_discover(refresh=False)
