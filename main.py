import requests
from bs4 import BeautifulSoup

indeed_result = requests.get("https://au.indeed.com/jobs?q=python&l=Perth%20WA&limit=50")

indeed_soup = BeautifulSoup(indeed_result.text, "html.parser")

pagination = indeed_soup.find("div", class_="pagination")

links = pagination.find_all('a')

pages = []

for link in links:
    pages.append(int(link.string))
max_page = pages[-1]