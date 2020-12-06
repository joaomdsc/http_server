# typingstudy_fr.py -

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

row_sleep = 3
part_sleep = 30
lesson_sleep = 120
last_part = [0, 8, 13, 12, 13, 14, 11, 11, 11, 11, 11, 11, 11, 11, 11, 8]

#-------------------------------------------------------------------------------
# get_part
#-------------------------------------------------------------------------------

def get_part(url):
    print(f'Getting {url}', file=sys.stderr)
    drv.get(url)

    words = []
    while True:
        try:
            nd = drv.find_element_by_xpath('//div[@id="text"]/span[@class="current"]')
        except common.exceptions.NoSuchElementException:
            try:
                nd = drv.find_element_by_xpath('//div[@id="text"]/span[@class="current_txt"]')
            except common.exceptions.NoSuchElementException:
                return words
        c = nd.text
        try:
            nd = drv.find_element_by_xpath('//div[@id="text"]/span[@class="next"]')
        except common.exceptions.NoSuchElementException:
            nd = drv.find_element_by_xpath('//div[@id="text"]/span[@class="next_txt"]')
        s = f'{c} {nd.text}'
        s = s.replace('↵', ' ')
        w = s.split()
        words.extend(w)

        nd = drv.find_element_by_xpath('//form[@name="type_form"]/textarea')
        s = 'x '*len(w)
        nd.send_keys(s)
        sleep(row_sleep)

#-------------------------------------------------------------------------------
# get_lesson
#-------------------------------------------------------------------------------

def get_lesson(lesson):
    # Numbered parts
    for n in range(last_part[lesson]):
        part = n+1
        
        url = f'https://www.typingstudy.com/fr-french-2/lesson/{lesson}/part/{part}'
        words = get_part(url)
        print(f'Lesson {lesson}, part {part}')
        print(' '.join(words) + '')
        sleep(lesson_sleep)
        part += 1
    
    # Touche supplémentaire
    url = f'https://www.typingstudy.com/fr-french-2/lesson/{lesson}/extra_key_drill'
    words = get_part(url)
    print(f'Lesson {lesson}, extra_key_drill')
    print(' '.join(words) + '')
    sleep(lesson_sleep)
    
    # Mot supplémentaire
    url = f'https://www.typingstudy.com/fr-french-2/lesson/{lesson}/extra_word_drill'
    words = get_part(url)
    print(f'Lesson {lesson}, extra_word_drill')
    print(' '.join(words) + '')
    sleep(lesson_sleep)
    
#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------

opt = Options()
opt.headless = True
drv = webdriver.Firefox(options=opt)

for n in range(15):
    get_lesson(n+1)

# Stop the firefox process
drv.close()