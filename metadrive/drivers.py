#import git
#git.Git("/your/directory/to/clone").clone("git://gitorious.org/git-python/mainline.git")

# Known drivers
# Github API

# GET https://api.github.com/repos/:owner/:repo/contents/:path

import io
import bs4
import tqdm
import urllib
import tarfile
import requests

def discover_drivers():
    '''
    Goes over all PyPI packages in existence, which end with "-driver" in their name
    and returns those which have __site_url__ in their package __init__.py file, as
    a mapping enabling the discovery of drivers for Internet sites.
    '''
    response = requests.get('https://pypi.org/simple/')
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
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
                                                            site_drivers.append(
                                                                {'domain': domain,
                                                                 'package': name,
                                                                 'site_url': site})
                                                    break
                                    break
    return site_drivers



index = [
    'https://gitlab.com/wefindx/infinity.git',
    'https://gitlab.com/wefindx/metaculus.git',
    'https://gitlab.com/wefindx/hthworldwide.git',
    'https://gitlab.com/wefindx/kompass.git',
    'https://gitlab.com/wefindx/linkedin.git',
    'https://gitlab.com/wefindx/halfbakery.git',
    'https://gitlab.com/wefindx/metaculus.git',
    # 'https://gitlab.com/wefindx/3d-systems-prox-dmp-300.git',
    # 'https://gitlab.com/wefindx/biodigitalapp.git',
    # 'https://gitlab.com/wefindx/cdcvitals.git',
    # 'https://gitlab.com/wefindx/flightradar24.git',
    # 'https://gitlab.com/wefindx/google.git',
    # 'https://gitlab.com/wefindx/hp-metal-jet.git',
    # 'https://gitlab.com/wefindx/hscodeseu.git',
    # 'https://gitlab.com/wefindx/huodongxing.git',
    # 'https://gitlab.com/wefindx/infinity.git',
    # 'https://gitlab.com/wefindx/jianshu.git',
    # 'https://gitlab.com/wefindx/kakotalk.git',
    # 'https://gitlab.com/wefindx/kik.git',
    # 'https://gitlab.com/wefindx/kr36.git',
    # 'https://gitlab.com/wefindx/lietuvai.git',
    # 'https://gitlab.com/wefindx/lineapp.git',
    # 'https://gitlab.com/wefindx/marinetraffic.git',
    # 'https://gitlab.com/wefindx/meetupapp.git',
    # 'https://gitlab.com/wefindx/opencorporates.git',
    # 'https://gitlab.com/wefindx/quora.git',
    # 'https://gitlab.com/wefindx/reddit.git',
    # 'https://gitlab.com/wefindx/skyscanner.git',
    # 'https://gitlab.com/wefindx/telegram.git',
    # 'https://gitlab.com/wefindx/treebase.git',
    # 'https://gitlab.com/wefindx/twitter.git',
    # 'https://gitlab.com/wefindx/ubio.git',
    # 'https://gitlab.com/wefindx/vimeo.git',
    # 'https://gitlab.com/wefindx/wechat.git',
    # 'https://gitlab.com/wefindx/weibo.git',
    # 'https://gitlab.com/wefindx/whatsapp.git',
    # 'https://gitlab.com/wefindx/windy.git',
    # 'https://gitlab.com/wefindx/youku.git',
    # 'https://gitlab.com/wefindx/youtube.git',
    # 'https://gitlab.com/wefindx/zhihu.git',
]
