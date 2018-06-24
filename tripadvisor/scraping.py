from __future__ import unicode_literals

# from urllib import urlencode
from urlparse import parse_qsl, urlparse # parse_qs, urlunparse
from bs4 import BeautifulSoup
from requests import requests
from tripadvisor.models import Listing


class AnalyzeScrape(object):
    host = 'https://www.tripadvisor.com'

    def index_page(self, obj, url, count):
        print("analyze index page %s" % (url))
        page = requests.get(url)
        bs = BeautifulSoup(page.text, 'html.parser')

        items = []
        i = 0
        for item in bs.select('.listItem .listing_title a'):
            if i < count:
                items.append(self.host + item.get('href'))
                i += 1
            else:
                break
        
        for link in items:
            self.listing_page(obj, link)
    
    def listing_page(self, obj, url):
        page = requests.get(url)
        bs = BeautifulSoup(page.text, 'html.parser')

        title = bs.select('h1#HEADING')[0].get_text()
        about = bs.select('.location_btf_wrap .description .text')[0].get_text()
        address = bs.select('.headerBL .blEntry.address')[0].get_text()
        img_map = bs.select('.staticMap img')[0]
        phone = bs.select('.blEntry.phone span:last-child')[0].get_text()
        
        img_src = img_map.get('src')
        query_pairs = dict(parse_qsl(urlparse(img_src).query))
        center_loc = query_pairs['center'].split(',')

        # price_from = 
        # price_to = 
        lat = center_loc[0]
        lng = center_loc[1]

        listing = Listing(
            url=url,
            title=title,
            about=about,
            link=obj,
            address=address,
            phone=phone,
            # website=website,
            # features=features,
            # email=email,
            # price_from=price_from,
            # price_to=price_to,
            lat=lat,
            lng=lng
        )
        listing.save()