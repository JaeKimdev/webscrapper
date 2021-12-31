import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q=python&sort=p&pg=1"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)


def extract_job(html):
    title = html.find("h2", {"class": "mb4"}).find("a")["title"]
    company, location = html.find("h3", {"class": "fc-black-700"}).find_all("span", recursive=0)
    print(company.get_text(strip=1), location.get_text(strip=1))
    # 0=False, 1 = True
    return {'title': title}


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        extract_page = requests.get(f"{URL}&pg={page + 1}")
        soup_extract_page = BeautifulSoup(extract_page.text, "html.parser")
        all_title = soup_extract_page.find_all("a", {"class": "s-link stretched-link"})
        for title in all_title:
            print(title["title"])


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
