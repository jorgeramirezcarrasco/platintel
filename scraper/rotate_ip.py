import requests
from re import findall
from itertools import cycle


def get_proxies():
    r = requests.get('https://www.sslproxies.org/')
    matches = findall(r"<td>\d+.\d+.\d+.\d+</td><td>\d+</td>", r.text)
    revised = [m.replace('<td>', '') for m in matches]
    proxies = [s[:-5].replace('</td>', ':') for s in revised]
    return proxies


def make_request(proxy_active, proxy_active_value, url, headers, params):
    proxies = get_proxies()
    proxy_pool = cycle(proxies)
    for i in range(100):
        if proxy_active != 1:
            proxy_active_value = next(proxy_pool)
        try:
            response = requests.get('https://httpbin.org/ip', timeout=3.0, proxies={
                                    "http": 'http://' + proxy_active_value, "https": 'https://' + proxy_active_value})
            page = requests.get(url, headers=headers, params=params, proxies={
                                "http": 'http://' + proxy_active_value, "https": 'https://' + proxy_active_value})
            proxy_active = 1
            if page.status_code == 200:
                return proxy_active, proxy_active_value, page
        except Exception as e:
            proxy_active = 0
            continue
    return proxy_active, proxy_active_value, "Error"
