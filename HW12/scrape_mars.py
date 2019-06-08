from splinter import Browser
from bs4 import BeautifulSoup

import time
import requests
import pymongo
import pandas as pd

def init_browser():
    # Window Users
    # executable_path = {'executable_path': 'chromedriver.exe'}
    # browser = Browser('chrome', **executable_path, headless=False)

    # Mac Users
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # NASA Mars News

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

    news_title = soup.title.text.strip()
    news_p = soup.body.p.text



    # JPL Mars Space Images - Featured Image 

    # URL of page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Get the correct div
    featured_img = soup.find("div", class_="default floating_text_area ms-layer").find("a")

    # Get the attribute of anchor tag
    jp_img = featured_img['data-fancybox-href']
    home_url = 'https://www.jpl.nasa.gov' + jp_img
    
    featured_image_url = home_url



    # Mars Weather

    # URL of page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    tweet =  soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')

    mars_weather = tweet.text



    # Mars Facts 

    # URL of page to be scraped
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    time.sleep(1)

    tables = pd.read_html(url)

    df = tables[0]
    df.columns = ['Label', 'Info']

    mars_table = df.to_html()
    mars_table.replace('\n', '')



    # Mars Hemispheres 

    # URL of page to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Mars Hemispheres Sample Image Page 1 

    img_1 = soup.find("div", class_="item").find("a")
    url_1 = img_1['href']

    # URL of page to be scraped
    url = 'https://astrogeology.usgs.gov' + url_1
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find title
    web_find = soup.find("div", class_="content").find("h2")
    title_1 = web_find.text

    # Find URL 
    web_find = soup.find("div", class_="wide-image-wrapper").find("a")
    img_url_1 = web_find["href"]


    # Mars Hemispheres Sample Image Page 2 

    browser.click_link_by_partial_text("Schiaparelli Hemisphere Enhanced")

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find title: Schiaparelli Hemisphere Enhanced
    web_find = soup.find("div", class_="content").find("h2")
    title_2 = web_find.text

    # Find URL
    web_find = soup.find("div", class_="wide-image-wrapper").find("a")
    img_url_2 = web_find["href"]


    # Mars Hemispheres Sample Image Page 3 

    browser.click_link_by_partial_text("Syrtis Major Hemisphere Enhanced")

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find title: Syrtis Major Hemisphere Enhanced
    web_find = soup.find("div", class_="content").find("h2")
    title_3 = web_find.text

    # Find URL
    web_find = soup.find("div", class_="wide-image-wrapper").find("a")
    img_url_3 = web_find["href"]


    # Mars Hemispheres Sample Image Page 4 

    browser.click_link_by_partial_text("Valles Marineris Hemisphere Enhanced")

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find title: Valles Marineris Hemisphere Enhanced
    web_find = soup.find("div", class_="content").find("h2")
    title_4 = web_find.text

    # Find URL: http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg
    web_find = soup.find("div", class_="wide-image-wrapper").find("a")
    img_url_4 = web_find["href"]


    hemisphere_image_urls = [
    {"title": title_1, "img_url": img_url_1},
    {"title": title_2, "img_url": img_url_2},
    {"title": title_3, "img_url": img_url_3},
    {"title": title_4, "img_url": img_url_4},
    ]



    # Store data in a dictionary
    mars_dict = {
        "News_Title": news_title,
        "News_Paragraph": news_p,
        "Featured_Image": featured_image_url,
        "Weather": mars_weather,
        "Facts": mars_table,
        "Hemisphere": hemisphere_image_urls,
        "Title_1": title_1,
        "Title_2": title_2,
        "Title_3": title_3,
        "Title_4": title_4,
        "Image_1": img_url_1,
        "Image_2": img_url_2,
        "Image_3": img_url_3,
        "Image_4": img_url_4
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_dict
