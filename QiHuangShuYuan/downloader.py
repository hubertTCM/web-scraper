# -*- coding: utf-8 -*-
import os
import urllib.request
import collections

from bs4 import BeautifulSoup

Entry = collections.namedtuple('Entry', 'name url')

def query_data(url):
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            try:
                return data.decode('utf8')
            except:
                return data
    except Exception as e:
        print('exception in url ****', e, url)
        return ""

# 医案链接
def parse_summary(entry, parent_directory):
    entry_directory = os.path.join(parent_directory, entry.name)
    if not os.path.exists(entry_directory):
        os.makedirs(entry_directory)
    raw_text = query_data(entry.url)
    with open(os.path.join(entry_directory, "content.html"), "w+") as content_file:
        content_file.write(raw_text)

    bs = BeautifulSoup(raw_text, 'html.parser')
    nameList = bs.find_all('div', {'class':'margin_a8'})

    details = []
    for name in nameList:
        links = name.find_all('a')
        for link in links:
            if not next((x for x in details if x.url == link['href']), None):
                details.append(Entry(name= link.get_text(), url=link['href']))
    
    for item in details:
        download_detail_pdf(item, entry_directory)


# 医案pdf
def download_detail_pdf(entry, parent_directory):
    entry_directory = os.path.join(parent_directory, entry.name)
    if not os.path.exists(entry_directory):
        os.makedirs(entry_directory)
    raw_text = query_data('http://www.xlgyyjs.com' + entry.url)
    with open(os.path.join(entry_directory, "content.html"), "w+") as content_file:
        content_file.write(raw_text)
    
    bs = BeautifulSoup(raw_text, 'html.parser')
    nameList = bs.find_all('div', {'class':'margin_a8'})

    downloaded = []
    for name in nameList:
        links = name.find_all('a')
        for link in links:
            url = link['href'].strip()
            if not url.startswith("http"):
                url = 'http://www.xlgyyjs.com' + url
            print(url)

            text = link.get_text().strip()
            if text.lower().endswith('pdf') or url.lower().endswith('pdf'):
                with open(os.path.join(entry_directory, text), "w+") as content_file:
                    data = query_data(url)
                    if data:
                        content_file.write(data)
                    else:
                        print(text, url)
            else:
                pass



if __name__ == "__main__":
    entries = [
        Entry(name='急危重症病例', url='http://www.xlgyyjs.com/keyan/Index_174.html')]
    for entry in entries:
        parse_summary(entry, os.path.join(os.path.dirname(__file__), "resource"))

    print(os.path.dirname(__file__))
    print("***done***")
pass
