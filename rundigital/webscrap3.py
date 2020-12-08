# webscrap2.py - RunDigital 2ème site web, après acceptation des rdvs

# Les pages de détail de chaque entreprise n'ont pas le nom de l'entreprise,
# elles ont des logos. On n'a nulle part textuellement le nom de la boîte. Ce
# code re-parcourt le catalogue pour extraire juste la liste des noms. 

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
# get_page
#-------------------------------------------------------------------------------

def get_page(url):
    print(f'Getting {url}', file=sys.stderr)
    drv.get(url)

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

# Catalogue
urls = []
for h2 in drv.find_elements_by_xpath('//div[@class="media-body m-t-5"]/h2'):
    name = h2.text
    print(f'Nom={name}')
print()

for s in drv.find_elements_by_xpath('//div[@class="media-body m-t-5"]/h2/small'):
    stext = s.text
    print(f's={stext}')

# Stop the firefox process
drv.close()