import os
import sys
import time

import smtplib
from email.message import EmailMessage

from selenium import webdriver
from selenium.webdriver.common.by import By

# Add these as ENV variables
# GMAIL_PASSWORD should be a Google generated 'App Password'
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

mail_recipients = ["cirtorosandiana64@gmail.com", "petreioana25@yahoo.com"]
mail_subject = "Chirie noua pe Storia"

latest_apartment_link = "..."


def send_mail(last_added_apartment_link):
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.ehlo()
            server.login(GMAIL_USER, GMAIL_PASSWORD)

            mail = EmailMessage()
            mail["From"] = GMAIL_USER
            mail["To"] = mail_recipients
            mail["Subject"] = mail_subject
            mail.set_content("Link spre ultimul racnet: \n\n" + last_added_apartment_link)

            server.sendmail(GMAIL_USER, mail_recipients, mail.as_string())
            print("Mail sent successfully", file=sys.stdout)
    except:
        print("Failed to send mail", file=sys.stderr)

def start():
    global latest_apartment_link

    driver = webdriver.Chrome()
    driver.get("https://www.storia.ro/ro/rezultate/inchiriere/apartament/cluj/cluj--napoca?distanceRadius=0&page=1&limit=36&market=ALL&roomsNumber=%5BTWO%2CTHREE%5D&priceMax=500&by=DEFAULT&direction=DESC&viewType=listing")

    while True:
        list_of_apartments = driver\
            .find_element(By.XPATH, "//div[@data-cy='search.listing.organic']")\
            .find_element(By.TAG_NAME, "ul")\
            .find_elements(By.TAG_NAME, "li")
        last_added_apartment_link = list_of_apartments[0].find_element(By.TAG_NAME, "a").get_attribute("href")

        if last_added_apartment_link != latest_apartment_link:
            send_mail(last_added_apartment_link)
            latest_apartment_link = last_added_apartment_link
        else:
            print("Nothing new found", file=sys.stdout)

        driver.refresh()
        time.sleep(60)


if __name__ == '__main__':
    start()
