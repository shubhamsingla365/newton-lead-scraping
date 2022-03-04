from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
import time
import csv
import re
with open('HiristPostings.csv', 'w', newline='\n') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow([
        "Job Link", "Role", "Company Name", "Job Location",
        "Minimum Experience", "Tech Stack Requirements", "Ideal/Not Ideal",
        "Phone Number", "Email ID"
    ])
    chrome_path = r"/Users/shubhamsingla/Documents/Python Scripts/chromedriver"
    driver = webdriver.Chrome(options=chrome_options)
    roles = [
        "frontend%20developer", "fullstack%20developer", "web%20developer",
        "react%20developer", "ui%20developer"
    ]
    job_links = []
    for role in roles:
        driver.get("https://www.hirist.com/search/" + str(role) +
                   "-0-1-0-1-1-AND-1.html?range=1")
        time.sleep(2)
        last_height = driver.execute_script(
            "return document.body.scrollHeight")
        while True:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            try:
                linke_eles = driver.find_elements_by_css_selector('a')
            except:
                continue
            for link_ele in linke_eles:
                try:
                    templink = str(link_ele.get_attribute("href"))
                except:
                    continue
                if "/j/" in templink and templink.split(
                        "?")[0] not in job_links:
                    job_links.append(templink.split("?")[0])
            new_height = driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    for job_link in job_links:
        driver.get(job_link)
        time.sleep(2)
        try:
            role_name = str(
                driver.find_element_by_css_selector(
                    'div.job-detail-title').text)
            company_name = str(
                driver.find_element_by_css_selector(
                    'div.company-detail-wrapper').text)
            job_location = str(
                driver.find_element_by_css_selector('div.old-job').text)
            job_text = str(
                driver.find_element_by_css_selector(
                    'div.details-container').text)
        except:
            continue
        match = re.search(
            r'[0-9]([ ]|)([-]|to|To)([ ]|)[0-9]([ ]|)([Y]|[y]|ex|Ex)',
            job_text)
        if match:
            exp_req = match.group()
        else:
            match = re.search(r'[0-9](|[ ])([+]|[-]|)([ ]|)([Y]|[y]|ex|Ex)',
                              job_text)
            if match:
                exp_req = match.group()
            else:
                match = re.search(
                    r'[0-9]([ ]|)([Y]|[y]|yrs|years|Years|Yrs|ex|Ex)(|[ ])([-]|to)(|[ ])[0-9]([ ]|)([Y]|[y]|yrs|years|Years|Yrs|Ex|ex)',
                    job_text)
                if match:
                    exp_req = match.group()
                else:
                    exp_req = ""
        tech_stack = ""
        if "reactjs" in job_text.lower() or "react.js" in job_text.lower(
        ) or "react js" in job_text.lower(
        ) or "react javascript" in job_text.lower():
            tech_stack = tech_stack + "ReactJS"
        else:
            if "react" in job_text.lower():
                tech_stack = tech_stack + "React"
        if "angular" in job_text.lower():
            if tech_stack != "":
                tech_stack = tech_stack + ", " + "Angular"
            else:
                tech_stack = tech_stack + "Angular"
        if "html" in job_text.lower() or "css" in job_text.lower():
            if tech_stack != "":
                tech_stack = tech_stack + ", " + "HTML/CSS"
            else:
                tech_stack = tech_stack + "HTML/CSS"
        if "JS" in job_text or "javascript" in job_text.lower():
            if tech_stack != "":
                tech_stack = tech_stack + ", " + "JS"
            else:
                tech_stack = tech_stack + "JS"
        if "python" in job_text.lower():
            if tech_stack != "":
                tech_stack = tech_stack + ", " + "Python"
            else:
                tech_stack = tech_stack + "Python"
        if " c " in job_text.lower() or "c++" in job_text.lower():
            if tech_stack != "":
                tech_stack = tech_stack + ", " + "C/C++"
            else:
                tech_stack = tech_stack + "C/C++"
        if "php" in job_text.lower():
            if tech_stack != "":
                tech_stack = tech_stack + ", " + "PHP"
            else:
                tech_stack = tech_stack + "PHP"
        if "dsa" in job_text.lower():
            if tech_stack != "":
                tech_stack = tech_stack + ", " + "DSA"
            else:
                tech_stack = tech_stack + "DSA"
        if "node" in job_text.lower():
            if tech_stack != "":
                tech_stack = tech_stack + ", " + "Node"
            else:
                tech_stack = tech_stack + "Node"
        if ".net" in job_text.lower():
            if tech_stack != "":
                tech_stack = tech_stack + ", " + ".NET"
            else:
                tech_stack = tech_stack + ".NET"
        if tech_stack == "ReactJS, HTML/CSS, JS" or tech_stack == "ReactJS, HTML/CSS" or tech_stack == "ReactJS, JS" or tech_stack == "HTML/CSS, JS" or tech_stack == "HTML/CSS" or tech_stack == "ReactJS" or tech_stack == "JS":
            ideal_flag = "Ideal"
        else:
            ideal_flag = "Not Ideal"
        match2 = re.search(r'[0-9]', exp_req)
        if match2:
            min_exp = match2.group()
        else:
            min_exp = "0"
        if int(min_exp) > 1:
            ideal_flag = "Not Ideal"
        match3 = re.search(
            r'[1-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]', job_text)
        if match3:
            phone_num = match3.group()
        else:
            match3 = re.search(
                r'[1-9][0-9][0-9]([ ]|[-])[0-9][0-9][0-9]([-]|[ ])[0-9][0-9][0-9][0-9]',
                job_text)
            if match3:
                phone_num = match3.group()
            else:
                phone_num = ""
        match4 = re.search(
            r'/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/',
            job_text.lower())
        if match4:
            email_id = match4.group()
        else:
            email_id = ""
        csvwriter.writerow([
            job_link, role_name, company_name, job_location, min_exp,
            tech_stack, ideal_flag, phone_num, email_id
        ])
