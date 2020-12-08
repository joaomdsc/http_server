# webscrap2.py - RunDigital 2ème site web, après acceptation des rdvs

import os
import sys
from time import sleep

from selenium import common, webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

#-------------------------------------------------------------------------------
# I want stdout and stderr to be unbuffered, always
#-------------------------------------------------------------------------------

class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

import sys
sys.stdout = Unbuffered(sys.stdout)
sys.stderr = Unbuffered(sys.stderr)
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# globals
#-------------------------------------------------------------------------------

part_sleep = 30

#-------------------------------------------------------------------------------
# get_login
#-------------------------------------------------------------------------------

def get_login(url):
    print(f'Getting {url}', file=sys.stderr)
    drv.get(url)

    name = drv.find_element_by_id('UserName')
    name.send_keys('anchavalie')
    pswd = drv.find_element_by_id('Password')
    pswd.send_keys('5Spu*bbj')
    
    btn = drv.find_element_by_xpath('//form[@id="frmLogin"]/a')
    btn.click()

#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------

opt = Options()
# opt.headless = True
drv = webdriver.Firefox(options=opt)

# Login
get_login('https://app.premiumcontact.fr/')
sleep(10)

# RunDigital
print(f'Getting Catalogue', file=sys.stderr)
drv.get('https://app.premiumcontact.fr/Catalogue/Index?idIntermediation=370')
sleep(10)

# Destination
dirpath = r'c:\a\rundigital\catalogue'

# Catalogue
urls = []
for a in drv.find_elements_by_xpath('.//section/div[@class="container"]/a'):
    url = a.get_attribute('href')
    print(f'Storing url={url}')
    urls.append(url)
sleep(10)

n = 0
for u in urls:
    print(f'Getting url={url}')
    drv.get(u)

    filepath = os.path.join(dirpath, f'contact{n}.html')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(drv.page_source)
    n += 1
    sleep(30)

# Stop the firefox process
drv.close()