from helium import *  # calculated risk
from bs4 import BeautifulSoup
import pandas as pd

# empty lists for data manipulation
job_titles = []
job_links = []
job_companies = []
job_locations = []
job_types = []
job_levels = []
job_times = []
job_contracts = []

next_page = True
page_num = 1

while next_page:

    url = f'https://www.pracuj.pl/praca/gdansk;wp?rd=10&pn={page_num}'

    print(f'Scraping page no.{page_num} - {url}\n')

    browser = start_chrome(url, headless=True)

    soup = BeautifulSoup(browser.page_source, 'html.parser')

    browser.close()

    result_html = soup.find('div', {'class': 'results'}, id="results")

    jobs = result_html.find_all('div', {'class': 'offer__info'})

    for job in jobs:
        try:
            job_title = job.find('a', {'class': 'offer-details__title-link'}).text
        except (AttributeError, TypeError):
            job_title = ''
        try:
            job_link = job.find('a', {'class': 'offer-details__title-link'})['href']
        except (AttributeError, TypeError):
            job_link = ''
        try:
            job_company = job.find('a', {'class': 'offer-company__name'}).text
        except (AttributeError, TypeError):
            job_company = ''
        try:
            job_location = job.find('li', {'class': 'offer-labels__item--location'}).text
        except (AttributeError, TypeError):
            job_location = ''
        try:
            job_type = job.find('li', {'data-test': 'list-item-offer-work-modes'}).text
        except (AttributeError, TypeError):
            job_type = ''
        try:
            job_level = job.find('li', {'data-test': 'list-item-offer-employment-level'}).text
        except (AttributeError, TypeError):
            job_level = ''
        try:
            job_time = job.find('li', {'data-test': 'list-item-offer-work-schedule'}).text
        except (AttributeError, TypeError):
            job_time = ''
        try:
            job_salary = job.find('li', {'data-test': 'list-item-offer-salary'}).text
        except (AttributeError, TypeError):
            job_salary = ''
        try:
            job_contract = job.find('li', {'data-test': 'list-item-offer-type-of-contract'}).text
        except (AttributeError, TypeError):
            job_contract = ''

        # add keywords to search for specific phrases in job titles
        keywords = ['python', 'data', 'science', 'scientist', 'developer', 'dev', 'programista']
        keywords.extend([keyword.capitalize() for keyword in keywords] + [keyword.upper() for keyword in keywords])

        if any(keyword in job_title for keyword in keywords):

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

        except (AttributeError, TypeError):
            next_page = False

    print(f'Page no.{page_num} scraped\n')
    page_num += 1

    continue

df = pd.DataFrame([job_companies, job_titles, job_locations, job_levels, job_contracts, job_types,
                   job_times, job_links]).T
df.columns = ['Pracodawca', 'Stanowisko', 'Lokalizacja', 'Poziom stanowiska', 'Rodzaj umowy', 'Typ pracy',
              'Wymiar pracy', 'Link']
df.to_excel('job_offers_pracuj.xlsx', index=False)
print('Job offers exported to Excel successfully.')
