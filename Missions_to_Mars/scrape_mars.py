from splinter import Browser
from bs4 import BeautifulSoup
import requests
import re
import time
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': r'C:\Users\smith\Downloads\chromedriver_win32\chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_info():
    # mars news
    browser = init_browser()
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.select_one('ul.item_list li.slide div.content_title').text
    news_text = soup.select_one('div.article_teaser_body').text

    # mars image
    space_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(space_url)
    html_space = browser.html
    time.sleep(5)
    soup_space = BeautifulSoup(html_space, 'html.parser')
    featured_image_url_path = soup_space.find('article', class_='carousel_item').get('style')
    featured_image_url_split = featured_image_url_path.split("'")
    featured_image_url_pos = featured_image_url_split[1]
    featured_image_url = f"https://www.jpl.nasa.gov/{featured_image_url_pos}"

    # mars weather
    url_weather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_weather)
    time.sleep(10)
    html_weather = browser.html
    soup_weather = BeautifulSoup(html_weather, 'html.parser')
    mars_weather = soup_weather.find_all('span', text=re.compile(r'sol'))
    tweet = mars_weather[0].text

    # mars facts
    url_facts = 'https://space-facts.com/mars/'
    browser.visit(url_facts)
    time.sleep(5)
    tables = pd.read_html(url_facts)
    html_table = tables[0].to_html()
    # html_table = df.to_html()

    # hemispheres
    url_hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemi)
    time.sleep(5)
    hemi_list = browser.links.find_by_partial_text('Hemisphere')
    img = []
    for i in range(4):
        browser.links.find_by_partial_text('Hemisphere')[i].click()
        html_hemi = browser.html
        soup_hemi = BeautifulSoup(html_hemi, 'html.parser')
        hemi_link = soup_hemi.find('a', text='Sample')
        img.append(hemi_link.get('href'))
        browser.back()
        time.sleep(5)


    mars_data = {
        "news_title": news_title,
        "news_text": news_text,
        "featured_image": f"{featured_image_url}",
        "latest_weather":tweet,
        "mars_facts": html_table,
        "hemi_1":f"{img[0]}",
        "hemi_2":f"{img[1]}",
        "hemi_3":f"{img[2]}",
        "hemi_4":f"{img[3]}"
    }


    return mars_data




