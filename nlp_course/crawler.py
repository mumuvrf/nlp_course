import queue
from typing import List

import requests
from bs4 import BeautifulSoup

import re

re_handle = '@[A-Za-z0-9_.-]+'
re_hashtag = '#[A-Za-z0-9]+'
re_zipcode = '\d{5}-\d{3}'

def get_data(url: str) -> List[str]:
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.Timeout:
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    page_text = soup.get_text()
    
    handles = re.findall(re_handle, page_text)
    print("Handles: ", handles)

    hashtags = re.findall(re_hashtag, page_text)
    print("Hashtags: ", hashtags)

    zipcodes = re.findall(re_zipcode, page_text)
    print("Zip Codes: ", zipcodes)

    title = soup.title.string if soup.title else 'No title found'

    links = []
    for link in soup.find_all('a'):
        target_url = link.get('href')
        if target_url is None:
            continue
        if target_url.startswith('http'):
            links.append(target_url)
    return links, title


def crawl(
    start_url: str,
    max_documents: int,
) -> List[str]:

    q = queue.Queue()
    q.put(start_url)
    visited = set()

    saved_info = []

    while (not q.empty()) and (len(visited) < max_documents):
        url = q.get()
        if url in visited:
            continue
        visited.add(url)

        print(f'Now visiting: {url}')
        links, title = get_data(url)
        saved_info.append((title, url))
        for link in links:
            if link not in visited:
                q.put(link)
    return visited, saved_info

crawl("https://ww2.trt2.jus.br/contato/telefones-e-enderecos/unidade-rio-branco", 5)