import requests
from bs4 import BeautifulSoup
from collections import OrderedDict

__author__ = 'ipsi'


def to_array(yieldable):
    a = []
    for o in yieldable:
        a.append(repr(o))
    return a


def update_key(dict, key):
    if key in dict:
        dict[key] += 1
    else:
        dict[key] = 1


def parse(base_url):
    data = {}
    target_url = base_url
    page_count = 1
    while True:
        print("Processing page [" + target_url + "]")
        r = requests.get(target_url)
        if r.status_code == 404:
            print("Received 404 attempting to hit URL [" + target_url + "] - assuming no more pages.")
            break
        soup = BeautifulSoup(r.text, 'html.parser')
        for postHeader in soup.find_all("div", "post_header"):
            strings = postHeader.stripped_strings
            strings = to_array(strings)
            if len(strings) < 2:
                print("PostHeader does not contain location: [" + strings + "]")
                continue
            location = strings[1].strip("'| ")
            location = location.split(",")
            if len(location) == 1:
                update_key(data, location[0].strip())
            elif len(location) == 2:
                update_key(data, location[0].strip() + ", " + location[1].strip())
            elif len(location) == 3:
                update_key(data, location[1].strip() + ", " + location[2].strip())
            else:
                print("Unknown location format [" + location + "]")

        page_count += 1
        target_url = base_url + "/page/" + str(page_count)
        if page_count > 100000:
            break

    print(OrderedDict(sorted(data.items(), key=lambda x: x[1])))
