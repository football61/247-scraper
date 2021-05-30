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
df = pd.read_csv('team_roster_urls.csv')
teams = len(df) + 1


commits = df[df.columns[1]].tolist()
print(commits)
csv_columns = ['url', 'name', 'hometown', 'position', 'size', 'rating', 'national_rank', 'position_rank', 'state_rank', 'status', 'team', 'season']
data_dict = []
for team in commits:
    for season in range(2000,2021):
        driver.get('https://247sports.com/college/' + str(team) + '/Season/' + str(season) + '-Football/Commits/')
        for row in range(1,40):
            try:
                url = driver.find_element_by_xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/ul/li[' + str(row) + ']/div[1]/div[2]/a').get_attribute('href').lower()
                name = driver.find_element_by_xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/ul/li[' + str(row) + ']/div[1]/div[2]/a').text.lower()
                hometown = driver.find_element_by_xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/ul/li[' + str(row) + ']/div[1]/div[2]/span').text.lower()
                position = driver.find_element_by_xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/ul/li[' + str(row) + ']/div[1]/div[6]').text.lower()
                size = driver.find_element_by_xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/ul/li[' + str(row) + ']/div[1]/div[3]').text.lower()
                rating = driver.find_element_by_xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/ul/li[' + str(row) + ']/div[1]/div[4]/div[1]/span[6]').text.lower()
                national_rank = driver.find_element_by_xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/ul/li[' + str(row) + ']/div[1]/div[4]/div[3]/a[1]').text.lower()
                position_rank = driver.find_element_by_xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/ul/li[' + str(row) + ']/div[1]/div[4]/div[3]/a[2]').text.lower()
                state_rank = driver.find_element_by_xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/ul/li[' + str(row) + ']/div[1]/div[4]/div[3]/a[3]').text.lower()
                status = driver.find_element_by_xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/ul/li[' + str(row) + ']/div[1]/div[5]').text.lower()
                print(status)
                
                data = {'url': url, 'name': name, 'hometown':hometown, 'position': position, 'size':size,
                        'rating': rating, 'national_rank': national_rank, 'position_rank':position_rank, 'state_rank': state_rank, 'status':status, 'team':team, 'season':season}
                data_dict.append(data)
            except NoSuchElementException:
                continue

csv_file = "team_commits.csv"
try:
    with open(csv_file, 'w',newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter='\t')
        writer.writeheader()
        for data in data_dict:
            writer.writerow(data)
except IOError:
    print("I/O error")        
print(data_dict)