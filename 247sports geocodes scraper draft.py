import requests
import pandas as pd
from lxml import html
import re
import datetime
from time import sleep


sports = ['football']
years = ['2023']
states = ['fl']
positions = ['']
#institution_groups = ['HighSchool','JuniorCollege','PrepSchool']
institution_groups = ['HighSchool']
txt = str(datetime.datetime.now().date())
current_date = re.sub("-", "_", txt)
print(current_date)


def geocoords_247(high_school_name,hometown2):
    YOUR_API_KEY = ''
    stem = high_school_name + ' high school' + ',' + hometown2
    address = stem.replace(' ','+')
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + address + '&key=' + YOUR_API_KEY
    #print(url)
    payload={}
    response = requests.request("GET", url, data=payload)
    #print(response.text)
    return response.json()


def pages_to_scrape(years,sports,institution_groups,states):
    pages = []
    for year in years:
        for sport in sports:
            for institution_group in institution_groups:
                for state in states:
                    sleep(2)
                    print('step1')
                    url = 'https://247sports.com/Season/' + str(year) + '-' + sport + '/CompositeRecruitRankings/?InstitutionGroup=' + institution_group + '&State=' + state             
                    print(url)
                    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}
                    recruits = requests.get(url, headers=headers)
                    root = html.fromstring(recruits.content)
                    s = root.xpath('//*[@id="page-content"]/div/section/header/h1/span/text()')[0]
                    print(s)
                    total = round(int(s[s.find('(')+1:s.find(')')])/50)+1
                    pages.append(total)
                    print('step2')
    return pages



def high_school_scraper(url):
    sleep(2)
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}
    recruits = requests.get(url, headers=headers)
    root = html.fromstring(recruits.content)
    print(url)
    try:
        high_school_name = root.xpath('//*[@id="page-content"]/div/section/header/div[1]/ul[3]/li[1]/span[2]/a/text()')[0]
    except:
        try:
            high_school_name = root.xpath('//*[@id="page-content"]/div/section/header/div[1]/ul[3]/li[1]/span[2]/text()')[0].strip()
        except:
            high_school_name = ''
    try:
        high_school_url = root.xpath('//*[@id="page-content"]/div/section/header/div[1]/ul[3]/li[1]/span[2]/a/@href')[0]
    except:
        try:
            high_school_url = root.xpath('//*[@id="page-content"]/div/section/header/div[1]/ul[3]/li[1]/span[2]/@href')[0].strip()
        except:
            high_school_url = ''
    try:
        hometown2 = root.xpath('//*[@id="page-content"]/div/section/header/div[1]/ul[3]/li[2]/span[2]/text()')[0].strip()
    except:
        hometown2 = ''
    return [high_school_name, high_school_url, hometown2]
    

def profile_scraper(years,sports,institution_groups,states,page_lists):
    profiles_list = []
    for i in range(0,len(years)):
        year = years[i]
        page_list = page_lists[i] + 1
        print(str(year) + ':  ' + str(page_list))
        for sport in sports:
            for institution_group in institution_groups:
                for state in states:
                    print(sport + ',' + institution_group + ',' + state)
                    for page in range(1,page_list):
                        print(page)
                        sleep(3)
                        pageurl = 'https://247sports.com/Season/' + str(year) + '-' + sport + '/CompositeRecruitRankings/?ViewPath=~%2FViews%2FSkyNet%2FPlayerSportRanking%2F_SimpleSetForSeason.ascx&State=' + state + '&InstitutionGroup=' + institution_group + '&Page='+ str(page)
                        print(pageurl)
                        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}
                        recruits = requests.get(pageurl, headers=headers)
                        root = html.fromstring(recruits.content)
                        #print(str(page) + ' ' + str(year))
                        #print(pageurl)
                        players = len(root.xpath('//*[@id="page-content"]/li'))+1
                        for row in range(1,players):
                            if row != 16:
                                df = {'class':'','current_date':'','institution_group':'','current_date':'','state':'','hometown':'','composite_ranking':'','top_247_ranking':'','name':'','profile_url':'','position':'','height_weight':'',
                                        'hometown2':'','rating':'','national_ranking':'','position_ranking':'','state_ranking':'','high_school_name':'','high_school_url':'','lat':'','lng':'','address':''}
                                try:
                                    df['composite_ranking'] = root.xpath('//*[@id="page-content"]/li[' + str(row) + ']/div[1]/div[1]/div[1]/text()')[0]
                                except:
                                    df['composite_ranking'] = ''
                                try:
                                    df['top_247_ranking'] = root.xpath('//*[@id="page-content"]/li[' + str(row) + ']/div[1]/div[1]/div[2]/text()')[0]
                                except:
                                    df['top_247_ranking'] = ''
                                try:
                                    df['name'] += root.xpath('//*[@id="page-content"]/li[' + str(row) + ']/div[1]/div[3]/a/text()')[0]
                                    df['profile_url'] = root.xpath('//*[@id="page-content"]/li[' + str(row) + ']/div[1]/div[3]/a/@href')[0]
                                    df['class'] = year
                                except:
                                    df['name'] = ''
                                    df['profile_url'] = ''
                                    df['class'] = ''
                                try:
                                    df['position'] = root.xpath('//*[@id="page-content"]/li[' + str(row) + ']/div[1]/div[4]/text()')[0]
                                except:
                                    df['position'] = ''
                                try:
                                    df['height_weight'] = root.xpath('//*[@id="page-content"]/li[' + str(row) + ']/div[1]/div[5]/text()')[0]
                                except:
                                    df['height_weight'] = ''
                                try:
                                    df['hometown'] = root.xpath('//*[@id="page-content"]/li[' + str(row) + ']/div[1]/div[3]/span/text()')[0]
                                except:
                                    df['hometown'] = ''
                                try:
                                    df['rating'] = root.xpath('//*[@id="page-content"]/li[' + str(row) + ']/div[1]/div[6]/div[1]/span[6]/text()')[0]
                                except:
                                    df['rating'] = ''
                                try:
                                    df['national_ranking'] = root.xpath('//*[@id="page-content"]/li[' + str(row) + ']/div[1]/div[6]/div[3]/a[1]/text()')[0]
                                except:
                                    df['national_ranking'] = ''
                                try:
                                    df['position_ranking'] = root.xpath('//*[@id="page-content"]/li[' + str(row) + ']/div[1]/div[6]/div[3]/a[2]/text()')[0]
                                except:
                                    df['position_ranking'] = ''
                                try:
                                    df['state_ranking'] = root.xpath('//*[@id="page-content"]/li[' + str(row) + ']/div[1]/div[6]/div[3]/a[3]/text()')[0]
                                    df['institution_group'] = institution_group
                                    df['current_date'] = current_date
                                    df['state'] = state
                                except:
                                    df['state_ranking'] = ''
                                    df['institution_group'] = ''
                                    df['current_date'] = ''
                                    df['state'] = ''
                                try:
                                    hs = high_school_scraper('https://www.247sports.com' + root.xpath('//*[@id="page-content"]/li[' + str(row) + ']/div[1]/div[3]/a/@href')[0])
                                except:
                                    hs = ['','','']
                                try:
                                    df['high_school_name'] = hs[0]
                                except:
                                    df['high_school_name'] = ''
                                try:
                                    df['high_school_url'] = hs[1]
                                except:
                                    df['high_school_url'] = ''
                                try:
                                    df['hometown2'] = hs[2]
                                except:
                                    df['hometown2'] = ''
                                coords = geocoords_247(hs[0],hs[2])
                                try:
                                    df['lat'] = coords['results'][0]['geometry']['location']['lat']
                                except:
                                    df['lat'] = ''
                                try:
                                    df['lng'] = coords['results'][0]['geometry']['location']['lng']
                                except:
                                    df['lng'] = ''
                                try:
                                    df['address'] = coords['results'][0]['formatted_address']
                                except:
                                    df['address'] = ''
                                df['current_date'] = current_date
                                print(df['address'])                                 
                                profiles_list.append(df.copy())
    return profiles_list


page_lists = pages_to_scrape(years, sports, institution_groups, states)
print(page_lists)
profiles_list = profile_scraper(years, sports, institution_groups, states, page_lists)
pd.DataFrame.from_dict(profiles_list).to_csv(str(current_date) + '_' + str(years) + '_' + str(sports) + '_' + str(institution_groups) + '_' + str(states) + '_' + str(positions) + '.csv',index=False)


