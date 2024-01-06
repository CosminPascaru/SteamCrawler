import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import time

base_url = 'https://store.steampowered.com/search/?'

class UrlBuilder:
    url:str
    tag_counter:int
    feature_counter:int
    os_counter:int
    
    def __init__ (self):
        self.url = base_url
        self.tag_counter = 0
        self.feature_counter = 0 
        self.os_counter = 0
        
    def add_tag(self, tag:str):
        if self.tag_counter == 0:
            self.url += 'tags='
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
    
    def add_feature(self, feature:str):
        
        
        match feature:
            case 'achievement':
                if self.feature_counter == 0:
                    self.url += '&category2=22'
                if self.feature_counter > 0:
                    self.url += '%2C22'
                self.feature_counter += 1
            case 'workshop':
                if self.feature_counter == 0:
                    self.url += '&category2=30'
                if self.feature_counter > 0:
                    self.url += '%2C30'
                self.feature_counter += 1
            case 'cloud':
                if self.feature_counter == 0:
                    self.url += '&category2=23'
                if self.feature_counter > 0:
                    self.url += '%2C23'
                self.feature_counter += 1
            case 'windows':
                if self.os_counter == 0:
                    self.url += '&os=win'
                else:
                    self.url += '%2Cwin'
                self.os_counter = 1    
            case 'linux':
                if self.os_counter == 0:
                    self.url += '&os=linux'
                else: 
                    self.url += '%2Clinux'
                self.os_counter = 1  
                
    def add_features(self, list):
        for feature in list:
            self.add_feature(feature)
    
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

def parse_feature_list(bool_list):
    feature_list = []
    if bool_list[0]:
        feature_list.append('achievement')
    if bool_list[1]:
        feature_list.append('workshop')
    if bool_list[2]:
        feature_list.append('cloud')
    if bool_list[3]:
        feature_list.append('windows')
    if bool_list[4]:
        feature_list.append('linux')
    
def generate_store_url (tag_list, feature_list):
    url = UrlBuilder()
    if tag_list != None:
        url.add_tags(tag_list)
    if feature_list != None:
        url.add_features(feature_list)
    url.finish_url()
    return url.url    
        
def get_store_html (url, scroll_range):  
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

def extract_game_urls (html, max):
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

def get_game_urls(tag_list, feature_list, url_count):
    url = generate_store_url(tag_list, feature_list)
    
    if url_count < 50:
        hops = 0
    elif url_count < 100:
        hops = 1
    elif url_count < 150:
        hops = 3
    else:
        hops = 6
        
    html = get_store_html(url, hops)    
    
    game_urls = extract_game_urls(html, url_count)
    
    return game_urls

def extract_game_data(url):
    html  = requests.get(url)
    #div class = gameHeaderImageCtn
    #img class = game_header_image_full src = "--> img url <--"

    soup = BeautifulSoup(html.text, 'html5lib')
    
    img_anchor = soup.find('img', class_='game_header_image_full')
    img_src = img_anchor['src']
    print(img_src)
    

def main():
    #testing stuff
    
    tag_list = ['pixel_graphics']
    feature_list = ['cloud']
    url = generate_store_url(tag_list, feature_list)
    
    print(url)
    
main()
    

