import apiage
import random

def generate(
        point,
        kind='doctors',
        d=80,
        test=True,
        pause=lambda: random.randint(1,2),
        proxies={'http': 'socks5://127.0.0.1:9999', 'https': 'socks5://127.0.0.1:9999'},
        servers={'test': {'url': 'https://ghsapi-staging.betahth.com',
                          'key': '#---get one---#'},
                 'prod': {'url': 'https://ghsapi.hthworldwide.com',
                          'key': '#---get one---#'}},
        gen=True): # return generator
    '''
    point: dict that has keys 'latitude', 'longitude' (e.g., -34.61315, -58.37723).
    gen: if gen, then returns generator, else, returns responses combined
    kind: can be ['doctors', 'pharmacies', 'hospitals']
    '''
    url_template = '{url}/{kind}/search/geolocation/?latitude={latitude}&longitude={longitude}&distance={distance}&distance_type=k&page={page}&page_size=100&includeLaungages=true&user_key={key}'

    if test:
        server = servers['test']
    else:
        server = servers['prod']

    first_url = url_template.format(
        url=server['url'],
        latitude=point['latitude'],
        longitude=point['longitude'],
        distance=d,
        key=server['key'],
        kind=kind,
        page=1
    )

    def next_url(r):
        if r['PagingData']['PageCurrent'] < r['PagingData']['PageTotalCount']:
            p = r['PagingData']['PageCurrent']+1
        else:
            p = None

        if p:
            url = url_template.format(
                url=server['url'],
                latitude=point['latitude'],
                longitude=point['longitude'],
                distance=d,
                key=server['key'],
                page=p
            )
            return url

    def count_results(r):
        try:
            return r['PagingData']['ItemsTotalCount']
        except:
            return None

    if gen:
        api = getattr(apiage, 'gen')
    else:
        api = getattr(apiage, 'get')

    data = api(
        first_url,
        next_key=next_url,
        count_key=count_results,
        results_key=kind.title(),
        proxies=proxies,
        pause=pause,
        remove_keys_in_url=['user_key'],
        debug=True
    )

    return data
