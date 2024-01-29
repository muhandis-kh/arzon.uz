import os
import requests


token_url = "https://id.uzum.uz/api/auth/token"
token_headers = {'Accept': '*/*',
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9,uz-UZ;q=0.8,uz;q=0.7,ru-RU;q=0.6,ru;q=0.5,tr;q=0.4",
                'Access-Control-Request-Headers': 'content-type',
                'Access-Control-Request-Method': 'POST',
                'Connection': 'keep-alive',
                'Host': 'id.uzum.uz',
                'Origin': 'https://uzum.uz',
                'Referer': 'https://uzum.uz/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
token_response = requests.post(token_url, headers=token_headers)
if token_response:
    data = token_response.cookies
    
    access_token = data.get('access_token', None)
    if access_token:
        # print(access_token)
        pass
    else:
        print("noting")
# Запросы для магазина
list_headers = {
    'authority': 'graphql.uzum.uz',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,uz-UZ;q=0.8,uz;q=0.7,ru-RU;q=0.6,ru;q=0.5,tr;q=0.4',
    'apollographql-client-name': 'web-customers',
    'apollographql-client-version': '1.29.9',
    'authorization': f'Bearer {access_token}',
    # Already added when you pass json=
    # 'content-type': 'application/json',
    'origin': 'https://uzum.uz',
    'referer': 'https://uzum.uz/',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'x-iid': '0a2bf1a1-1581-47f8-8b4a-6d0c3cbe0c9d',
}

products_headers = {
    'authority': 'api.uzum.uz',
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9,uz-UZ;q=0.8,uz;q=0.7,ru-RU;q=0.6,ru;q=0.5,tr;q=0.4',
    'access-content-allow-origin': '*',
    'authorization': f'Bearer {access_token}',
    'content-type': 'application/json',
    'origin': 'https://uzum.uz',
    'referer': 'https://uzum.uz/',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'x-iid': '0a2bf1a1-1581-47f8-8b4a-6d0c3cbe0c9d',
}


def json_data(query, offset):
    return {
        'operationName': 'getMakeSearch',
        'variables': {
            'queryInput': {
                'text': query,
                'showAdultContent': 'TRUE',
                'filters': [],
                'sort': 'BY_RELEVANCE_DESC',
                'pagination': {
                    'offset': offset,
                    'limit': 48,
                },
            },
        },
        'query': 'query getMakeSearch($queryInput: MakeSearchQueryInput!) {\n  makeSearch(query: $queryInput) {\n    id\n    queryId\n    queryText\n    category {\n      ...CategoryShortFragment\n      __typename\n    }\n    categoryTree {\n      category {\n        ...CategoryFragment\n        __typename\n      }\n      total\n      __typename\n    }\n    items {\n      catalogCard {\n        __typename\n        ...SkuGroupCardFragment\n      }\n      __typename\n    }\n    facets {\n      ...FacetFragment\n      __typename\n    }\n    total\n    mayHaveAdultContent\n    __typename\n  }\n}\n\nfragment FacetFragment on Facet {\n  filter {\n    id\n    title\n    type\n    measurementUnit\n    description\n    __typename\n  }\n  buckets {\n    filterValue {\n      id\n      description\n      image\n      name\n      __typename\n    }\n    total\n    __typename\n  }\n  range {\n    min\n    max\n    __typename\n  }\n  __typename\n}\n\nfragment CategoryFragment on Category {\n  id\n  icon\n  parent {\n    id\n    __typename\n  }\n  seo {\n    header\n    metaTag\n    __typename\n  }\n  title\n  adult\n  __typename\n}\n\nfragment CategoryShortFragment on Category {\n  id\n  parent {\n    id\n    title\n    __typename\n  }\n  title\n  __typename\n}\n\nfragment SkuGroupCardFragment on SkuGroupCard {\n  ...DefaultCardFragment\n  photos {\n    key\n    link(trans: PRODUCT_540) {\n      high\n      low\n      __typename\n    }\n    previewLink: link(trans: PRODUCT_240) {\n      high\n      low\n      __typename\n    }\n    __typename\n  }\n  badges {\n    ... on BottomTextBadge {\n      backgroundColor\n      description\n      id\n      link\n      text\n      textColor\n      __typename\n    }\n    __typename\n  }\n  characteristicValues {\n    id\n    value\n    title\n    characteristic {\n      values {\n        id\n        title\n        value\n        __typename\n      }\n      title\n      id\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment DefaultCardFragment on CatalogCard {\n  adult\n  favorite\n  feedbackQuantity\n  id\n  minFullPrice\n  minSellPrice\n  offer {\n    due\n    icon\n    text\n    textColor\n    __typename\n  }\n  badges {\n    backgroundColor\n    text\n    textColor\n    __typename\n  }\n  ordersQuantity\n  productId\n  rating\n  title\n  __typename\n}',
    }