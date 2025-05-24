# scraper_remoteok.py

import requests
from bs4 import BeautifulSoup

def scrape_remoteok(keyword="data scientist"):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    url = f"https://remoteok.com/remote-{keyword.replace(' ', '-')}-jobs"
    print(f"Scraping: {url}")
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    job_rows = soup.find_all("tr", class_="job")
    jobs = []

    for job in job_rows:
        try:
            title = job.find("h2").text.strip()
            company = job.find("h3").text.strip()
            location = job.find("div", class_="location")
            location = location.text.strip() if location else "Remote"
            date_posted = job.find("time")
            date_posted = date_posted["datetime"] if date_posted else "N/A"

            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "date_posted": date_posted
            })

        except Exception as e:
            print("Skipping job due to error:", e)

    return jobs
