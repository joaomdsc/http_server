# webscrap.py - RunDigital

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

    drv.find_element_by_id('btnLogin').click()

#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------

opt = Options()
# opt.headless = True
drv = webdriver.Firefox(options=opt)

# Login
get_login('https://client.premiumcontact.fr/')
sleep(10)

# RunDigital
print(f'Getting RunDigital', file=sys.stderr)
drv.get('https://client.premiumcontact.fr/Event/cLickEvent/370')
sleep(10)

# # Speed Meetingqs
# print(f'Getting Speed meetings', file=sys.stderr)
# drv.get('https://client.premiumcontact.fr/speedmeetings/370')
# filepath = r'c:\a\rundigital\Speed Meetings - page1.html'
# with open(filepath, 'w', encoding='utf-8') as f:
#     f.write(drv.page_source)
# sleep(10)

# # Go to pagination
# ul = drv.find_element_by_xpath('//div[@class="pagination-container"]/ul/li/a')
# print('found ul: len(ul)={len(ul)}')

# Getting pages
print(f'Getting pages', file=sys.stderr)
for i in range(5):
    url = f'https://client.premiumcontact.fr/speedmeetings/370?page={i+1}'
    drv.get(url)
    sleep(5)
    filepath = rf'c:\a\rundigital\Speed Meetings - page{i+1}.html'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(drv.page_source)

# Stop the firefox process
drv.close()