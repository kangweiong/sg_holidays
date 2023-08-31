import pandas as pd
import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
# options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.get('https://www.moe.gov.sg/calendar')

while not driver.find_elements(By.XPATH, '//*[@id="moe-calendar"]/div/div[1]/div/div[1]/span[1]/div/div/div[1]/div'):
  time.sleep(0.5)

edu_level = driver.find_element(By.XPATH, '//*[@id="moe-calendar"]/div/div[1]/div/div[1]/span[1]/div/div/div[1]/div')
edu_level.click()

while not driver.find_elements(By.XPATH, '//*[@id="moe-calendar"]/div/div[1]/div/div[1]/span[1]/div/div[2]'):
  time.sleep(0.5)

primary = driver.find_element(By.XPATH, '//*[@id="react-select-2-option-1"]')
primary.click()
secondary = driver.find_element(By.XPATH, '//*[@id="react-select-2-option-2"]')
secondary.click()

event_type = driver.find_element(By.XPATH, '//*[@id="moe-calendar"]/div/div[1]/div/div[1]/span[2]/div/div/div[1]/div')
event_type.click()

while not driver.find_elements(By.XPATH, '//*[@id="moe-calendar"]/div/div[1]/div/div[1]/span[2]/div/div[2]'):
  time.sleep(0.5)

sch_hol = driver.find_element(By.XPATH, '//*[@id="react-select-3-option-1"]')
sch_hol.click()
public_hol = driver.find_element(By.XPATH, '//*[@id="react-select-3-option-2"]')
public_hol.click()

time.sleep(1)

elements = driver.find_elements(By.CLASS_NAME, 'fc-list-item')

holidays = [[e.find_element(By.CLASS_NAME,'event-l-title').text,
             e.find_element(By.CLASS_NAME,'event-l-type').text, 
             datetime.strptime(e.get_attribute('data-start'),'%d %b %Y').date().isoformat(),
             datetime.strptime(e.get_attribute('data-end'),'%d %b %Y').date().isoformat() if e.get_attribute('data-end') else pd.NA] for e in elements]

df = pd.DataFrame(holidays,columns=['name', 'type', 'start', 'end'])

df['end'] = df['end'].fillna(df['start'])


records = {'records': df.to_dict(orient='records')}

with open("db.json", "w") as outfile:
    json.dump(records, outfile)
