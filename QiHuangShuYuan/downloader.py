# -*- coding: utf-8 -*-
import os
import urllib.request
import collections

Entry = collections.namedtuple('Entry', 'name url')

def query_data(url):
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf8')
    except:
        return ""

# 医案链接
def parse_summary(entry, parent_directory):
    entry_directory = os.path.join(parent_directory, entry.name)
    if not os.path.exists(entry_directory):
        os.makedirs(entry_directory)
    raw_text = query_data(entry.url)
    with open(os.path.join(entry_directory, "content.html"), "w+") as content_file:
        content_file.write(raw_text)
    pass


if __name__ == "__main__":
    entries = [
        Entry(name='急危重症病例', url='http://www.xlgyyjs.com/keyan/Index_174.html')]
    for entry in entries:
        parse_summary(entry, os.path.join(os.path.dirname(__file__), "resource"))

    print(os.path.dirname(__file__))
    print("***done***")
pass
