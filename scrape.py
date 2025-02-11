from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import os
from urllib.parse import urlparse
import ssl


url = 'https://html.duckduckgo.com/html?q=esg+report+filetype%3Apdf' #using duckduckgo because google has captcha for scraping
options = webdriver.EdgeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--headless') #no chrome popup
driver = webdriver.Edge(options=options)
driver.get(url)
start_time = time.time()
max_time = 10
results = []

def search():
    if time.time() - start_time > max_time: #optional timer :)
         return results
    time.sleep(3)
    container = driver.find_element(By.CLASS_NAME, 'results')
    individual_search = container.find_elements(By.CLASS_NAME, 'result__url')
    for i in individual_search:
        results.append(i.text)
    next_btn = driver.find_element(By.XPATH, '//input[@class="btn btn--alt" and @type="submit"]')
    if next_btn:
        next_btn.click()
        time.sleep(2)
        return search()

link_collated = search()
driver.close()

#to download the files
for i in link_collated:
    o = urlparse(f'https://{i}')
    oName = o.netloc.split('.')[1] #to get the part after www.[etcetc].com
    filename = os.path.basename(i) #get file name
    oName_filename = oName + filename
    try:
      r = requests.get(f'https://{i}')
      with open(f'{oName_filename}.pdf', 'wb') as file:
          file.write(r.content)
      print(f'Succesfully downloaded {oName_filename}.pdf')
    except Exception as e:
        print(f'Error downloading {oName_filename}.pdf')
        print(f"Error downloading {oName_filename}.pdf from {i}: {e}")
        continue



