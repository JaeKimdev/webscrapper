import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = "https://au.indeed.com/jobs?as_and=python&as_phr&as_any&as_not&as_ttl&as_cmp&jt=all&st&salary&radius=50&l=Western%20Australia&fromage=any&limit=50&sort&psf=advsrch&from=advancedsearch&vjk=7d34b0f4f9c24ea9"


def extract_indeed_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", class_="pagination")
    links = pagination.find_all('a')
    pages = []

    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page


def extract_job(html):
    job_title = html.find("h2", class_="jobTitle")
    title = job_title.find_all("span")[0].string
    company = html.find("span", class_="companyName")

    if title == "new":
        title = job_title.find_all("span")[1].string

    if company is not None:
        company = company.string
    else:
        company = None

    location = html.select_one("pre > div").text
    job_id = html["data-jk"]

    return {'title': title,
            'company': company,
            'location': location,
            'link': f"https://au.indeed.com/viewjob?jk={job_id}&from=web&vjs=3"}


def extract_indeed_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping page {page}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("a", class_="fs-unmask")
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs
