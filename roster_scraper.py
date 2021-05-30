from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import csv 
from selenium.webdriver.chrome.options import Options  
from random import uniform
from itertools import zip_longest
from bs4 import BeautifulSoup
import requests
import pandas as pd
from lxml import html
import re
import datetime

driver = webdriver.Chrome("chromedriver.exe")
df = pd.read_csv('team_roster_urls.csv', sep='\t')
teams = len(df) + 1
print(teams)

print('teams')

commits = [df.team_url.tolist()]
print(commits)
print('commits')
csv_columns = ['url', 'name', 'jersey', 'position', 'height', 'weight', 'year', 'age', 'hs', 'rating', 'team']
data_dict = []
for teams in commits:
    print(teams[0])
    for i in range(1,len(teams)):
        driver.get(teams[i])
        for row in range(1,200):
            try:
                url = driver.find_element_by_xpath('//*[@id="page-content"]/div/section[2]/div/section/div/table/tbody/tr[' + str(row) + ']/td/a').get_attribute('href').lower()
                name = driver.find_element_by_xpath('//*[@id="page-content"]/div/section[2]/div/section/div/table/tbody/tr[' + str(row) + ']/td/a').text.lower()
                jersey = driver.find_element_by_xpath('//*[@id="page-content"]/div/section[2]/div/section/div/div/table/tbody/tr[' + str(row) + ']/td[1]').text.lower()
                position = driver.find_element_by_xpath('//*[@id="page-content"]/div/section[2]/div/section/div/div/table/tbody/tr[' + str(row) + ']/td[2]').text.lower()
                height = driver.find_element_by_xpath('//*[@id="page-content"]/div/section[2]/div/section/div/div/table/tbody/tr[' + str(row) + ']/td[3]').text.lower()
                weight = driver.find_element_by_xpath('//*[@id="page-content"]/div/section[2]/div/section/div/div/table/tbody/tr[' + str(row) + ']/td[4]').text.lower()
                year = driver.find_element_by_xpath('//*[@id="page-content"]/div/section[2]/div/section/div/div/table/tbody/tr[' + str(row) + ']/td[5]').text.lower()
                age = driver.find_element_by_xpath('//*[@id="page-content"]/div/section[2]/div/section/div/div/table/tbody/tr[' + str(row) + ']/td[6]').text.lower()
                hs = driver.find_element_by_xpath('//*[@id="page-content"]/div/section[2]/div/section/div/div/table/tbody/tr[' + str(row) + ']/td[7]').text.lower()
                rating = driver.find_element_by_css_selector('tr:nth-child(' + str(row) + ') > td:nth-child(8) > span.rating').text.lower()
                
                data = {'url': url, 'name': name, 'jersey':jersey, 'position': position, 'height':height,
                        'weight': weight, 'year': year, 'age':age, 'hs': hs, 'rating':rating, 'team':teams[i]}
                data_dict.append(data)
            except NoSuchElementException:
                try:
                    url = driver.find_element_by_xpath('//*[@id="page-content"]/div/section[2]/div/section/div/table/tbody/tr[' + str(row) + ']/td/a').get_attribute('href').lower()
                    name = driver.find_element_by_xpath('//*[@id="page-content"]/div/section[2]/div/section/div/table/tbody/tr[' + str(row) + ']/td/a').text.lower()
                    jersey = driver.find_element_by_xpath('//*[@id="page-content"]/div/section[2]/div/section/div/div/table/tbody/tr[' + str(row) + ']/td[1]').text.lower()
                    position = driver.find_element_by_xpath('//*[@id="page-content"]/div/section[2]/div/section/div/div/table/tbody/tr[' + str(row) + ']/td[2]').text.lower()
                    height = driver.find_element_by_xpath('//*[@id="page-content"]/div/section[2]/div/section/div/div/table/tbody/tr[' + str(row) + ']/td[3]').text.lower()
                    weight = driver.find_element_by_xpath('//*[@id="page-content"]/div/section[2]/div/section/div/div/table/tbody/tr[' + str(row) + ']/td[4]').text.lower()
                    year = driver.find_element_by_xpath('//*[@id="page-content"]/div/section[2]/div/section/div/div/table/tbody/tr[' + str(row) + ']/td[5]').text.lower()
                    age = driver.find_element_by_xpath('//*[@id="page-content"]/div/section[2]/div/section/div/div/table/tbody/tr[' + str(row) + ']/td[6]').text.lower()
                    hs = driver.find_element_by_xpath('//*[@id="page-content"]/div/section[2]/div/section/div/div/table/tbody/tr[' + str(row) + ']/td[7]').text.lower()
                    rating = driver.find_element_by_xpath('//*[@id="page-content"]/div/section[2]/div/section/div/div/table/tbody/tr[' + str(row) + ']/td[8]').text.lower()
                    
                    data = {'url': url, 'name': name, 'jersey':jersey, 'position': position, 'height':height,
                            'weight': weight, 'year': year, 'age':age, 'hs': hs, 'rating':rating, 'team':teams[i]}
                    data_dict.append(data)
                except NoSuchElementException:
                    continue

csv_file = "team_roster_teams.csv"
try:
    with open(csv_file, 'w',newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter='\t')
        writer.writeheader()
        for data in data_dict:
            writer.writerow(data)
except IOError:
    print("I/O error")        
print(data_dict)
