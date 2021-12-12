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

        url = f'https://www.pracuj.pl/praca/test;kw/it%20-%20rozw%C3%B3j%20oprogramowania;cc,5016/praca%20zdalna;wm,home-office?pn={page}'

        print(url)

        browser = start_chrome(url, headless=True)

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}

        soup = BeautifulSoup(browser.page_source, 'html.parser')

        browser.close()

        result_html = soup.find('div', {'class': 'results'}, id="results")

        jobs = result_html.find_all('div', {'class': 'offer__info'})

        for job in jobs:
            try:
                job_title = job.find('a', {'class': 'offer-details__title-link'}).text
            except:
                job_title = ''
            try:
                job_link = job.find('a', {'class': 'offer-details__title-link'})['href']
            except:
                job_link = ''
            try:
                job_company = job.find('a', {'class': 'offer-company__name'}).text
            except:
                job_company = ''
            try:
                job_location = job.find('li', {'class': 'offer-labels__item--location'}).text
            except:
                job_location = ''
            try:
                job_type = job.find('li', {'data-test': 'list-item-offer-work-modes'}).text
            except:
                job_type = ''
            try:
                job_level = job.find('li', {'data-test': 'list-item-offer-employment-level'}).text
            except:
                job_level = ''
            try:
                job_time = job.find('li', {'data-test': 'list-item-offer-work-schedule'}).text
            except:
                job_time = ''
            try:
                job_salary = job.find('li', {'data-test': 'list-item-offer-salary'}).text
            except:
                job_salary = ''
            try:
                job_contract = job.find('li', {'data-test': 'list-item-offer-type-of-contract'}).text
            except:
                job_contract = ''

            job_titles.append(job_title)
            job_links.append(job_link)
            job_companies.append(job_company)
            job_locations.append(job_location)
            job_types.append(job_type)
            job_levels.append(job_level)
            job_times.append(job_time)
            job_contracts.append(job_contract)

            print([job_company, job_title, job_location, job_level, job_contract, job_type, job_time, job_link])
        try:
            next_page = soup.find('i', {'class': 'mdi mdi-chevron-right pagination_element-icon'})

        except AttributeError:
            next_page = False

        print(f'Page no.{page} scraped\n')

        page += 1

        continue

df = pd.DataFrame([job_companies, job_titles, job_locations, job_levels, job_contracts, job_types, job_times, job_links]).T
df.columns = ['Pracodawca', 'Stanowisko','Lokalizacja','Poziom stanowiska','Rodzaj umowy', 'Typ pracy','Wymiar pracy', 'Link']
df.to_excel('pracuj_test_zdalnie.xlsx', index=False)
print('Job offers exported to Excel successfully.')
