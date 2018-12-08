# Go over each country in https://www.kompass.com/selectcountry/
from boltons.iterutils import remap
import copy
import requests
import bs4
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
OPTIONS = Options()
OPTIONS.add_argument("--window-size=1600,900")
OPTIONS.add_argument("--disable-infobars")
OPTIONS.add_argument('--no-sandbox')
OPTIONS.add_argument('--disable-dev-shm-usage')
OPTIONS.add_argument('--headless')

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def get_domains():
    response = requests.get('https://www.kompass.com/selectcountry/', headers=headers, verify=False)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')

    L = soup.find('div', {'class': 'container countries-liste'})
    country_domains = [{'country': item.text, 'url': item.attrs['href'][:-2]}
                       for item in L.find_all('a')]

    return country_domains

# Go over each category at the bottom
def get_categories(domain):
    response = requests.get(domain, headers=headers, verify=False)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')

    C = soup.find('div', {'class': 'footerCol1-1'})
    categories = [{'category': item.text, 'url': item.attrs['href'], 'id': item.attrs['id']}
                  for item in C.find_all('a')[:-1]]

    return categories

# Go over each page in category
# response = requests.get('https://gb.kompass.com/s/transport-logistics/10/', headers=headers, verify=False)
# soup = bs4.BeautifulSoup(response.content, 'html.parser')

def get_pages_and_count(soup):
    pages = soup.find('ul', {'id': 'paginatorDivId'})
    if pages:
        max_page = max([int(pg.text.strip()) if pg.text.strip().isdigit() else -1
                        for pg in pages.find_all('li')
                        if pg.text.strip()])
    else:
        max_page = 1

    count = soup.find('span', {'class': 'numberSociety'})
    if count:
        s = count.text.strip().replace(',','')
        r = ''
        for l in s:
            if not l.isdigit():
                break
            else:
                r += l
        results_count = int(r)
    else:
        results_count = None

    return {'pages': max_page, 'total': results_count}

def get_subcategories(category_url):
    driver = webdriver.Chrome(chrome_options=OPTIONS)
    driver.get(category_url)
    soupx = bs4.BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()

    cats = soupx.find('div', {'class': 'activ1'})

    if cats:
        sub_categories = [
            {'name': item.text.split('\xa0\n')[0].strip(),
             'url': item.attrs['href'],
             'total': int(item.text.split('\xa0\n')[-1].strip()[1:-1])}
             for item in cats.find_all('a')]
    else:
        sub_categories = []

    return sub_categories

def paginate(category_url):
    response = requests.get(category_url, headers=headers, verify=False)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    info = get_pages_and_count(soup)

    records = []

    for page_id in range(1, info['pages']+1):
        if page_id == 1:
            url = category_url
        else:
            url = category_url + 'page-{}/'.format(page_id)
        print(url)

        item_response = requests.get(url, headers=headers, verify=False)
        item_soup = bs4.BeautifulSoup(item_response.content, 'html.parser')

        companies = item_soup.find_all('div', {'class': 'prod_list'})#[1:]

        for i, company in enumerate(companies):
            record = {
                'page_url': url,
                'url': company.find('a', {'class': 'productMainLink'}).attrs['href'],
                'raw': company
            }
            records.append(record)

    return records


def get_all_subcategories(category_url):
    '''
    Given a category url, returns subcategories, where each
    has total of <=1600 of results.
    '''
    response = requests.get(category_url, headers=headers, verify=False)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    info = get_pages_and_count(soup)
    info['url'] = category_url

    base = {'children': [info]}

    def visit(path, key, value):
        if isinstance(key, int):
            if value['total'] > 1600 and not 'children' in value:
                result = get_subcategories(value['url'])
                print('Getting...', value['url'])
                value['children'] = result
        return key, value

    while True:
        temp = copy.deepcopy(base)
        base = remap(base, visit)
        if base == temp:
            break

    def get_childless(category_tree):

        records = []

        def visit(path, key, value):
            if isinstance(key, int):
                if not value.get('children'):
                    records.append(value)
            return key, value

        result = remap(category_tree, visit)

        return records

    return get_childless(base)


# subcats = get_all_subcategories('https://gb.kompass.com/s/transport-logistics/10/')

#sum([cat['total'] for cat in subcats])

#tree = {}
# json.load(open('/home/mindey/Projects/Research/kompass.com/tree.json'))

# for domain in get_domains()[:-1]:
#     if domain['country'] in tree.keys():
#         continue
#     if domain['country']:
#         continue
#     print(domain['url'], domain['country'])
#
#     tree.update({
#         domain['country']: {'domain': domain['url'],
#                             'categories': get_categories(domain['url'])}})
#
#     for i, category in enumerate(tree[domain['country']]['categories']):
#         tree[domain['country']]['categories'][i]['subcategories'] = get_all_subcategories(category['url'])


#
# records = []
# for i, category in enumerate(categories):
#     data = paginate(category_url)
#     records.extend(data)


#
# tot = 0
# for t in tree:
#     for cat in tree[t]['categories']:
#         for sub in cat['subcategories']:
#             tot += sub['total']


# [Later] Visit each detail page
