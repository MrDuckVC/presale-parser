import time

from celery.task import periodic_task
from celery.schedules import crontab
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from .services import *


@periodic_task(run_every=(crontab(minute=30, hour=20)), name='check_for_a_tender')
def check_for_a_tender():
    with webdriver.Remote("http://webdriver:4444/wd/hub", desired_capabilities=DesiredCapabilities.CHROME) as browser:
        index_of_tender = 1
        browser.get("https://civic.md/anunturi/achizitii.html")
        last_checked_tender = get_last_checked_tender("civic.md")
        if last_checked_tender is None:
            condition = True
        else:
            condition = browser.find_element_by_css_selector(f"tr:nth-child({index_of_tender}) > td.list-title > a").get_attribute("href") != last_checked_tender
        civic_tenders_link = []
        while condition:
            try:
                civic_tenders_link.append(browser.find_element_by_css_selector(f"tr:nth-child({index_of_tender}) > td.list-title > a").get_attribute("href"))
                index_of_tender += 1
            except NoSuchElementException:
                try:
                    index_of_tender = 1
                    browser.find_element_by_css_selector("li.pagination-next > a").click()
                except NoSuchElementException:
                    break

        index_of_tender = 2
        browser.get("https://sc.undp.md/viewtenders2/")
        last_checked_tender = get_last_checked_tender("undp.md")
        if last_checked_tender is None:
            condition = True
        else:
            condition = browser.find_element_by_css_selector(f"tr:nth-child({index_of_tender}) > td:nth-child(2) > strong > a").get_attribute("href") != last_checked_tender
        undp_tenders_link = []
        while condition:
            try:
                undp_tenders_link.append(browser.find_element_by_css_selector(f"tr:nth-child({index_of_tender}) > td:nth-child(2) > strong > a").get_attribute("href"))
                index_of_tender += 1
            except NoSuchElementException:
                break

        index_of_tender = 2
        browser.get("https://achizitii.md/en/public/tender/list?page=1")
        last_checked_tender = get_last_checked_tender("achizitii.md")
        if last_checked_tender is None:
            condition = True
        else:
            condition = browser.find_element_by_css_selector(f"div:nth-child({index_of_tender}) > div > div > div > h2 > a:nth-child(1)").get_attribute("href") != last_checked_tender
        achizitii_tenders_link = []
        time.sleep(5)
        index_of_page = 2
        while condition:
            try:
                achizitii_tenders_link.append(browser.find_element_by_css_selector(
                    f"div:nth-child({index_of_tender}) > div > div > div > h2 > a:nth-child(1)").get_attribute(
                    "href"))
                index_of_tender += 1
            except NoSuchElementException:
                browser.get(f"https://achizitii.md/en/public/tender/list?page={index_of_page}")
                index_of_tender = 2
                if browser.find_element_by_css_selector(f"div:nth-child({index_of_tender}) > div > div > div > h2 > a:nth-child(1)").get_attribute("href") in achizitii_tenders_link:
                    break
                index_of_page += 1
                time.sleep(5)

        index_of_tender = 1
        last_checked_tender = get_last_checked_tender("mtender.md")
        if last_checked_tender is None:
            condition = True
        else:
            condition = browser.find_element_by_css_selector(f"div:nth-child({index_of_tender}) > div > div> div > div > a").get_attribute("href") != last_checked_tender
        browser.get("https://mtender.gov.md/plans?procedures=pin")
        time.sleep(5)
        mtender_tenders_link = []
        while condition:
            try:
                if browser.find_element_by_css_selector(
                        f"div:nth-child({index_of_tender}) > div > div> div > div > a").get_attribute("href") in mtender_tenders_link:
                    break
                mtender_tenders_link.append(browser.find_element_by_css_selector(
                    f"div:nth-child({index_of_tender}) > div > div> div > div > a").get_attribute("href"))
                index_of_tender += 1
            except NoSuchElementException:
                index_of_tender = 1
                browser.find_element_by_css_selector("button.btn-next > i").click()
                time.sleep(5)

        civic_tenders_content = []
        for civic_tender_link in civic_tenders_link:
            for i in range(3):
                try:
                    browser.get(civic_tender_link)
                except Exception as e:
                    pass
                else:
                    civic_tender_content = browser.find_element_by_css_selector("article > div > span").text.lower()
                    civic_tenders_content.append(clear_tender_content(civic_tender_content))
                    break
                if i == 2:
                    civic_tenders_content.append("")
                    print(f"{civic_tender_content} is broken")

        undp_tenders_content = []
        for undp_tender_link in undp_tenders_link:
            for i in range(3):
                try:
                    browser.get(undp_tender_link)
                except Exception as e:
                    pass
                else:
                    undp_tender_content = browser.find_element_by_css_selector("body").text.lower()
                    undp_tenders_content.append(clear_tender_content(undp_tender_content))
                    break
                if i == 2:
                    undp_tenders_content.append("")
                    print(f"{undp_tender_content} is broken")

        achizitii_tenders_content = []
        for achizitii_tender_link in achizitii_tenders_link:
            for i in range(3):
                try:
                    browser.get(achizitii_tender_link)
                except Exception as e:
                    pass
                else:
                    achizitii_tender_content = browser.find_element_by_css_selector("#description").text.lower()
                    achizitii_tenders_content.append(clear_tender_content(achizitii_tender_content))
                    break
                if i == 2:
                    achizitii_tenders_content.append("")
                    print(f"{achizitii_tender_content} is broken")

        mtender_tenders_content = []
        for mtender_tender_link in mtender_tenders_link:
            for i in range(3):
                try:
                    browser.get(mtender_tender_link)
                except Exception as e:
                    pass
                else:
                    time.sleep(2)
                    mtender_tender_content = browser.find_element_by_css_selector("div.info > div:nth-child(2)").text.lower()
                    mtender_tenders_content.append(clear_tender_content(mtender_tender_content))
            if i == 2:
                mtender_tenders_content.append("")
                print(f"{mtender_tender_link} is broken")

        print(
            f"{min(civic_tenders_content)}, civic"
            f"\n {min(undp_tenders_content)}, undp"
            f"\n {min(achizitii_tenders_content)}, achizitii"
            f"\n {min(mtender_tenders_content)}, mtender"
        )
        for user in get_users():
            user_needed_tenders = []

            user_key_words = get_key_words(user)
            for i in range(len(civic_tenders_content)):
                user_needed_tenders = get_needed_tenders(civic_tenders_content[i], user_needed_tenders,
                                                         civic_tenders_link[i], user_key_words)

            for i in range(len(undp_tenders_content)):
                user_needed_tenders = get_needed_tenders(undp_tenders_content[i], user_needed_tenders,
                                                         undp_tenders_link[i], user_key_words)
            
            for i in range(len(achizitii_tenders_content)):
                user_needed_tenders = get_needed_tenders(achizitii_tenders_content[i], user_needed_tenders,
                                                         achizitii_tenders_link[i], user_key_words)
            
            for i in range(len(mtender_tenders_content)):
                user_needed_tenders = get_needed_tenders(mtender_tenders_content[i], user_needed_tenders,
                                                         mtender_tenders_link[i], user_key_words)
            
            if user_needed_tenders is not []:
                result = "\n\r"
                for needed_tender in user_needed_tenders:
                    result += needed_tender
                    result += "\n\r"
                send_message(result, User.objects.filter(username=user).values_list("email")[0][0])
        put_last_checked_tender(mtender_tenders_link[-1], "mtender.md")
        put_last_checked_tender(civic_tenders_link[-1], "civic.md")
        put_last_checked_tender(undp_tenders_link[-1], "undp.md")
        put_last_checked_tender(achizitii_tenders_link[-1], "achizitii.md")
