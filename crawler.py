import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import time

base_url = 'https://store.steampowered.com/search/?tags='

class UrlBuilder:
    url:str
    tag_counter:int
    
    def __init__ (self):
        self.url = base_url
        self.tag_counter = 0
        
    def add_tag(self, tag:str):
        if self.tag_counter > 0:
            self.url += '%2C'
            
        self.tag_counter += 1  
         
        match tag:
            case 'indie':
                self.url += '492'
            case 'singleplayer':
                self.url += '4182'
            case 'adventure':
                self.url += '21'
            case 'action':
                self.url += '19'
            case '2d':
                self.url += '3871'
            case 'pixel_graphics':
                self.url += '3964'
            case 'platformer':
                self.url += '1625'
            case 'casual':
                self.url += '597'
            case 'rpg':
                self.url += '122'
            case 'story_rich':
                self.url += '1742'
            case 'strategy' :
                self.url += '9'
            case 'simulation' :
                self.url += '599'
            case 'first_person' :
                self.url += '3839'
            case 'shooter' :
                self.url += '1774'
            case 'pvp' :
                self.url += '1775'
            case 'coop' :
                self.url += '1685'
            
    def add_tags (self, list):
        for tag in list:
            self.add_tag(tag)
                        
    def finish_url (self):
        self.url += '&supportedlang=english&ndl=1.html'

def parse_tag_list(bool_list):
    tag_list = []
    if bool_list[0]:
        tag_list.append('indie')
    if bool_list[1]:
        tag_list.append('singleplayer')
    if bool_list[2]:
        tag_list.append('adventure')
    if bool_list[3]:
        tag_list.append('action')
    if bool_list[4]:
        tag_list.append('2d')
    if bool_list[5]:
        tag_list.append('pixel_graphics')
    if bool_list[6]:
        tag_list.append('platformer')
    if bool_list[7]:
        tag_list.append('casual')
    if bool_list[8]:
        tag_list.append('rpg')
    if bool_list[9]:
        tag_list.append('story_rich')
    if bool_list[10]:
        tag_list.append('strategy')
    if bool_list[11]:
        tag_list.append('simulation')
    if bool_list[12]:
        tag_list.append('first_person')
    if bool_list[13]:
        tag_list.append('shooter')
    if bool_list[14]:
        tag_list.append('pvp')
    if bool_list[15]:
        tag_list.append('coop')

    return tag_list
    
def save_html (response, file_path):
    
    fd = open(file_path, 'w')
    fd.write(response.text)
    fd.close

def get_game_urls (html, max):
    urls = []
    url_count = 0 

    soup = BeautifulSoup(html, 'html5lib')

    div = soup.find('div', attrs={'id': 'search_resultsRows'})

    anchors = div.find_all('a')
    
    for anchor in anchors:
        if 'href' in anchor.attrs:
            if url_count < max:
                url_count += 1
                urls.append(anchor['href'])
            else:
                return urls
    return urls 
        
def generate_store_html (url, scroll_range):  
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    
    for i in range(scroll_range):
        driver.execute_script("window.scrollBy(0, 1000);")
        #time.sleep(1)
    
    html = driver.page_source
    
    driver.quit()
    
    return html          

def generate_store_url (tag_list):
    url = UrlBuilder()
    url.add_tags(tag_list)
    url.finish_url()
    return url.url

def generate_game_urls(tag_list, url_count):
    url = generate_store_url(tag_list)
    
    if url_count < 50:
        hops = 0
    elif url_count < 100:
        hops = 1
    elif url_count < 150:
        hops = 3
    else:
        hops = 6
        
    html = generate_store_html(url, hops)    
    
    game_urls = get_game_urls(html, url_count)
    
    return game_urls

def main():
    # old testing stuff
    tag_list = ['pixel_graphics']
    
    game_urls = generate_game_urls(tag_list, 200)
    
    lmao = 0 
    for i in game_urls:
        lmao += 1
        print(i)
    print(lmao)

