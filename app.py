from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        known_skills = request.form.get('known_skills').split(',')
        unknown_skills = request.form.get('unknown_skills').split(',')
        return fetch_jobs(known_skills, unknown_skills)
    return render_template('index.html')

def fetch_jobs(known_skills, unknown_skills):
    base_url = 'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords='
    url = base_url + ','.join(known_skills)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')  # Update this based on the website's HTML structure

    relevant_jobs = []

    for job in jobs:
        job_title = job.find('h2').text.strip()  # Update selectors based on the website's structure
        company_name = job.find('h3').text.strip()
        skills = job.find('span', class_='srp-skills').text.strip()

        is_relevant = all(skill.lower() in skills.lower() for skill in known_skills)
        is_irrelevant = any(skill.lower() in skills.lower() for skill in unknown_skills)

        if is_relevant and not is_irrelevant:
            relevant_jobs.append((job_title, company_name, skills))
            
    return render_template('display.html', jobs=relevant_jobs)

if __name__ == '__main__':
    app.run(port=5001, debug=True)