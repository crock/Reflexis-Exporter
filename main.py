#!/usr/bin/env python3
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from icalendar import Calendar, Event

cal = Calendar()

USERNAME = ""
PASSWORD = ""
LOCATION = "4101 Legendary Dr, Destin FL 32541, United States"
URL = "https://wfm.belk.com/RWSBELK/LoginSubmit.jsp"

def debug(msg):
    print("\n[DEBUG] %s\n" % msg)

def display(cal):
    return cal.to_ical().replace('\r\n', '\n').strip()

s = requests.Session()

def get_payload(username, password, offset=360):
    return {
        "localeCode": None,
        "uType": None,
        "switchUserID": None,
        "browserTimeZoneOffset": offset,
        "txtUserID": username,
        "txtPassword": password
    }

def get_headers(cookie=None):
    return {
        "Host": "wfm.belk.com",
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://wfm.belk.com/RWSBELK/",
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "keep-alive",
        "Cookie": cookie
    }

def parse_html(response):
    print("Parsing calendar page...\n")
    return BeautifulSoup(response, 'html.parser')

def extract_text(soup):
    print("Extracting text from page...\n")
    return soup.get_text()

def get_month_year(soup):
    print("Extracting current month and year...")
    monyr = soup.body.findAll(attrs={'class': 'stdcontainer-text'})[1].string
    values = monyr.split(' ')
    return tuple(values)

def get_days(soup):
    print("Extracting information for each scheduled day...\n")
    return soup.body.find_all('td', attrs={'class': 'tblrow-v'})

def make_events(days, combo):
    for day in days:
        info = day.get_text().strip().split('\n')
        date = "%s %s, %s" % (combo[0], info[0], combo[1])
        shift = info[1]
        if len(days) is 4:
            note = info[3]

        dt_start_str = date + " " + shift.split('-')[0].rstrip() + "m"
        dt_end_str = date + " " + shift.split('-')[1].split(' ')[1] + "m"
        start = datetime.strptime(dt_start_str, "%B %d, %Y %I:%M%p").isoformat().replace("-", "").replace(":", "")
        end = datetime.strptime(dt_end_str, "%B %d, %Y %I:%M%p").isoformat().replace("-", "").replace(":", "")

        event = Event()
        event['summary'] = "Belk"
        event['location'] = LOCATION
        if len(days) is 4:
            event['description'] = note
        event['dtstart'] = start
        event['dtend'] = end

        cal.add_component(event)


def main():
    print("Grabbing cookies...\n")
    resp = s.get(URL)
    if resp.status_code is 200:
        debug("Success!")

        sessid = resp.cookies['JSESSIONID']
        cookie_str = "JSESSIONID=%s" % sessid
        headers = get_headers(cookie_str)
        payload = get_payload(USERNAME, PASSWORD)

        print("Logging in...\n")
        resp = s.post(URL, data=payload, headers=headers)
        if resp.status_code is 200:
            debug("Success!")

            fx = open('cal.html', "w")
            fx.write(resp.text)
            fx.close()

            soup = parse_html(resp.text)
            monthyear = get_month_year(soup)
            days = get_days(soup)
            make_events(days, monthyear)

            f = open('work_calendar.ics', 'wb')
            f.write(cal.to_ical())
            f.close()



if __name__ == "__main__":
    main()
