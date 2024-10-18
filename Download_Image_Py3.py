from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import requests
import sys
import os
import time
import urllib3
import shutil
from bs4 import BeautifulSoup

# Add path to geckodriver to the OS environment variable
os.environ["Path"] += os.pathsep + os.getcwd()
# Syntax of Search
search_syntax_head = "https://www.google.co.in/search?q="
search_syntax_end = "%0D%0A&sca_esv=339a018dea4bc811&udm=2&ei=aecRZ4ehF-rg2roPzcHnkQQ&ved=0ahUKEwjH-b6Kj5eJAxVqsFYBHc3gOUIQ4dUDCBA&uact=5&oq=BAC%0D%0A&gs_lp=Egxnd3Mtd2l6LXNlcnAiBEJBQwoyDRAAGIAEGLEDGEMYigUyCBAAGIAEGLEDMgQQABgDMgoQABiABBhDGIoFMg4QABiABBixAxiDARiKBTIIEAAYgAQYsQMyBBAAGAMyCBAAGIAEGLEDMgsQABiABBixAxiDATIFEAAYgARIvxNQAFi1CXAAeACQAQCYAUmgAcsBqgEBM7gBA8gBAPgBAZgCA6AC1AGYAwCSBwEzoAelDw&sclient=gws-wiz-serp"


def main():
    text_search = sys.argv[1]
    num_imgs = sys.argv[2]
    name_dir = sys.argv[3]
    # Chose Webdriver
    wd = webdriver.Chrome()
    if not os.path.exists(name_dir):
        os.makedirs(name_dir)
    url = search_syntax_head + text_search + search_syntax_end
    wd.get(url)

    # Return List src img for url web
    def get_link_url_image(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        images = soup.find_all("img")
        return [img["src"] for img in images if "src" in img.attrs]

    # Scroll web
    def scroll_windows(wd, delay):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    # Download image with url
    def downloadImg(url, nameFile, result_dir):
        http = urllib3.PoolManager()
        try:
            response = http.request("GET", url, preload_content=False, timeout=10)
            with open(r"%s\%s.jpg" % (result_dir, nameFile), "wb") as out_file:
                shutil.copyfileobj(response, out_file)
            response.release_conn()
        except Exception as e:
            print(f"Error downloading: {e}")

    num_start = 10000
    while True:
        link_url = get_link_url_image(url)
        for url in link_url:
            if num_imgs <= 0:
                wd.close()
                return
            downloadImg(url, num_start, name_dir)
            num_start += 1
            num_imgs -= 1
        else:
            scroll_windows(wd, 10)


if __name__ == "__main__":
    main()
