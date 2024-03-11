from flask import Flask, render_template
import requests
import os
import base64
from dotenv import load_dotenv
import xmltodict
from datetime import datetime
from requests.auth import HTTPBasicAuth
from weekdates import get_start_end_dates

app = Flask(__name__)

load_dotenv()

kracht_app = os.getenv('APP_NAME')
kracht_token = os.getenv('APP_TOKEN')
credentials = f"{kracht_app}:{kracht_token}"
credentials_base64 = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')


session = requests.Session()
session.auth = HTTPBasicAuth(kracht_app, kracht_token)
headers = {
    'Authorization': f'Basic {credentials_base64}',
    'Content-type': 'application/xml'
}

def get_activities(week_nr, stage):
    f_start_date, f_end_date, week_number = get_start_end_dates(week_nr, 2024)
    base_url = 'https://api.carerix.com/CRMatch/'
    show_params = f'?show=attributeChanges.attributeName&show=attributeChanges.effectiveDate&show=attributeChanges.value'
    qualifier = f'&qualifier=(attributeChanges.attributeName == "statusInfo" and attributeChanges.value == "{stage}" and attributeChanges.effectiveDate > (NSCalendarDate)"{f_start_date}" and attributeChanges.effectiveDate < (NSCalendarDate)"{f_end_date}")' 
    url = base_url + show_params + qualifier
   
    response = session.get(url)
     
    if response.status_code == 200:
        data_dict = xmltodict.parse(response.content)
        count_value = int(data_dict['array']['@count'])
        
        print(f"Aantal activiteiten: {count_value}")

        return count_value
    else:
        return f'Fout bij het ophalen van data: {response.status_code}', week_nr

@app.route('/')
def index():
    weeknr = 11
    qualified_candidates = get_activities(weeknr, 27)
    intakes = get_activities(weeknr, 5)
    offers = get_activities(weeknr, 6)
    interviews = get_activities(weeknr, 7)
    placements = get_activities(weeknr, 34)
    return render_template('funnel.html', weeknr=weeknr, qualified_candidates=qualified_candidates, intakes=intakes, offers=offers, interviews=interviews, placements=placements)

if __name__ == '__main__':
    app.run(debug=False)
