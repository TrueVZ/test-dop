import requests
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime
import os
from tika import parser
from collections import Counter
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt

cookies = {'MoodleSession': 'l1erceo61ovok6gfdqc8okc94t'} # Try to parse sdo

def dowload_file(download_url: str):
    now = datetime.now().strftime("%Y%m%d-%H%M%S")

    file_path = Path(f"pdfs/pdf_{now}.pdf")
    try:
        h = requests.head(download_url)
        content_type = h.headers.get('content-type')
        if content_type == "application/pdf":
            r = requests.get(url=download_url, cookies=cookies, allow_redirects=True, verify=False)
            file_path.write_bytes(r.content)
    except Exception:
        print(f"Get error when try to download file from {download_url}")


def download_files(url: str):
    path_string = ("resource", "image", "pluginfile")
    r = requests.get(url, verify=False, cookies=cookies)
    soup = BeautifulSoup(r.text, "html.parser")
    paths = soup.find_all(['a'])
    for path in paths:
        dowload_file(path['href'])

def get_metadata_from_pdf(file_name: str) -> dict:
    parsePDF = parser.from_file("pdfs/" + file_name)
    metadata = parsePDF['metadata']
    return metadata

def draw_plot(data: dict):
    fig, ax = plt.subplots()
    ax.barh(list(data.keys()), list(data.values()))
    ax.set_xlabel('Count')
    ax.set_title('Metadata keys')
    x_labels = ax.get_xticklabels()
    y_labels = ax.get_yticklabels()
    ax.set_ylabel('Metadata keys')
    plt.yticks(fontsize=6, rotation=45)
    fig.set_size_inches(20, 20, forward=True)
    # plt.setp(x_labels, rotation=45, horizontalalignment='right')
    # plt.setp(y_labels, rotation=45, horizontalalignment='right')
    plt.show()



if __name__ == '__main__':
    download_files("https://www.mirea.ru/about/documents/local-regulations/organizational-work/")
    stats_metadata = dict()
    pdfs = os.listdir("pdfs")
    for pdf_path in pdfs:
        meta_file = get_metadata_from_pdf(pdf_path)
        for k, v in meta_file.items():
            if k in stats_metadata:
                if type(v) is list:
                    continue
                else:
                    stats_metadata[k].add(v)
            else:
                if type(v) is list:
                    continue
                else:
                    stats_metadata[k] = {v}
    result = dict()
    for k, v in stats_metadata.items():
        count_data = len(stats_metadata[k])
        if count_data > 5:
            result[k] = count_data
    draw_plot(result)