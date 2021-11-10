from helium import *
from bs4 import BeautifulSoup
from math import ceil

url = f'https://www.pracuj.pl/praca/gdansk;wp/it%20-%20rozw%c3%b3j%20oprogramowania;cc,5016?rd=0&pn=1'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}

browser = start_chrome(url, headless=True)

soup = BeautifulSoup(browser.page_source, 'html.parser')

offer_counter = soup.find('span', {'class': 'results-header__offer-count-text-number'}).text

num_of_pages = ceil(int(offer_counter) / 50)

file = open('job_offers.txt','w',errors='ignore')

for page in range(1,num_of_pages+1):
    url = f'https://www.pracuj.pl/praca/gdansk;wp/it%20-%20rozw%c3%b3j%20oprogramowania;cc,5016?rd=0&pn={page}'

    browser = start_chrome(url, headless=True)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}

    soup = BeautifulSoup(browser.page_source, 'html.parser')

    result_html = soup.find('div', {'class': 'results'}, id="results")

    jobs = result_html.find_all('a', {'class': 'offer-details__title-link'})

    job_titles = []
    job_links = []

    for job in jobs:
        job_title = job.text
        job_link = job['href']

        job_titles.append(job_title)
        job_links.append(job_link)

        file.write(job_title + '\n' + job_link + '\n\n')

file.close()