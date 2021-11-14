from helium import *
from bs4 import BeautifulSoup
import pandas as pd

next_page = True
page = 1

job_titles = []
job_links = []
job_companies = []
job_locations = []
job_types = []
job_levels = []
job_times = []
job_contracts = []

while next_page:

        print(f'Scraping page no.{page}')

        url = f'https://www.pracuj.pl/praca/gdansk;wp?rd=10&et=3&pn={page}'

        browser = start_chrome(url, headless=True)

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}

        soup = BeautifulSoup(browser.page_source, 'html.parser')

        result_html = soup.find('div', {'class': 'results'}, id="results")

        jobs = result_html.find_all('div', {'class': 'offer__info'})

        for job in jobs:
            job_title = job.find('a', {'class': 'offer-details__title-link'}).text
            job_link = job.find('a', {'class': 'offer-details__title-link'})['href']
            try:
                job_company = job.find('a', {'class': 'offer-company__name'}).text
            except AttributeError:
                job_company = ''
            try:
                job_location = job.find('li', {'class': 'offer-labels__item--location'}).text
            except AttributeError:
                job_location = ''
            try:
                job_type = job.find('li', {'data-test': 'list-item-offer-work-modes'}).text
            except AttributeError:
                job_type = ''
            try:
                job_level = job.find('li', {'data-test': 'list-item-offer-employment-level'}).text
            except AttributeError:
                job_level = ''
            try:
                job_time = job.find('li', {'data-test': 'list-item-offer-work-schedule'}).text
            except AttributeError:
                job_time = ''
            try:
                job_salary = job.find('li', {'data-test': 'list-item-offer-salary'}).text
            except AttributeError:
                job_salary = ''
            try:
                job_contract = job.find('li', {'data-test': 'list-item-offer-type-of-contract'}).text
            except AttributeError:
                job_contract = ''

            job_titles.append(job_title)
            job_links.append(job_link)
            job_companies.append(job_company)
            job_locations.append(job_location)
            job_types.append(job_type)
            job_levels.append(job_level)
            job_times.append(job_time)
            job_contracts.append(job_contract)

        try:
            next_page = soup.find('i', {'class': 'mdi mdi-chevron-right pagination_element-icon'})

        except AttributeError:
            next_page = False

        print(f'Page no.{page} scraped')

        page += 1

        continue

df = pd.DataFrame([job_companies, job_titles, job_locations, job_levels, job_contracts, job_types, job_times, job_links]).T
df.columns = ['Pracodawca', 'Stanowisko','Lokalizacja','Poziom stanowiska','Rodzaj umowy', 'Typ pracy','Wymiar pracy', 'Link']
df.to_excel('job_offers_pracuj.xlsx', index=False)
print('Job offers exported to Excel successfully.')