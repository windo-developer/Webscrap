import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://de.indeed.com/Jobs?q=python&limit={LIMIT}"


def extract_indeed_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")

    listPagination = soup.find("div", {"class": "pagination"})

    links = listPagination.find_all('a')
    pages = []

    for link in links[:-1]:
        pages.append(int(link.find("span").string))

    max_page = pages[-1]

    return max_page


def extract_job(html):
    title = html.find("h2", {"class": "title"}).find('a')["title"]
    company = html.find("span", {"class": "company"})
    company_anchor = company.find("a")
    if company:
        if company_anchor is not None:
            company = str(company_anchor.string)
        else:
            company = str(company.string)
        company = company.strip()
    else:
        company = None

    location = html.find("div", {"class": "recJobLoc"})['data-rc-loc']
    job_id = html['data-jk']

    return {'title': title, "company": company, 'location': location, 'apply_link': f'https://de.indeed.com/viewjob?jk={job_id}'}


def extract_indeed_jabs(last_page):
    jobs = []

    for page in range(last_page):
        print(f"Scrapping Indeed Page:{page}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})

        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs


def get_jobs():
    last_indeed_page = extract_indeed_pages()
    indeed_jobs = extract_indeed_jabs(last_indeed_page)  # last page
    return indeed_jobs
