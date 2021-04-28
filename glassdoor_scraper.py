# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 17:49:21 2021

@author: Nikhil DragNeel
"""

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd

def get_jobs(keyword, num_jobs, verbose,path,slp_time):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    # driver = webdriver.Chrome(executable_path="/Users/omersakarya/Documents/GitHub/scraping-glassdoor-selenium/chromedriver", options=options)
    # path = "ChromeDriver/chromedriver"   # I have made a folder:"ChromeDriver" and put file"chromedriver.exe"inside this folder. 
    #         ^^^Folder^^^/^^^this is .exe file
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)
    
    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword="+keyword+"&sc.keyword="+keyword+"&locT=N&locId=115&jobType="
    # url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword='+ keyword +'&includeNoSalaryJobs=false&radius=100'
    #url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=false&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        #print('worked 1')
        time.sleep(slp_time)
        #print('worked 2')

        #Test for the "Sign Up" prompt and get rid of it.
        # try:
        #     driver.find_element_by_class_name("selected").click()
        # except ElementClickInterceptedException:
        #     pass

        # time.sleep(.1)

        try:
            driver.find_element_by_class_name("ModalStyle__xBtn___29PT9").click()  #clicking to the X.
        except NoSuchElementException:
            pass
            #print('worked 3')
        # found_popup = False 
        currentJoblist = 0
        
        #print('worked 4')
        if not (len(jobs) >= num_jobs):
            #print('worked 5')
            listButtonsCount = len(driver.find_elements_by_xpath('//*[@id="MainCol"]//div[1]//ul//li[@data-test="jobListing"]'))
            print("&&& job butons:" +str(listButtonsCount))
            #Going through each job in this page
            # job_buttons = driver.find_elements_by_class_name("jl")  #jl for Job Listing. These are the buttons we're going to click.
            job_buttons = driver.find_elements_by_xpath('.//*[@id="MainCol"]//a[@class="jobLink"]')  #jl for Job Listing. These are the buttons we're going to click.
            #print('worked 6')
            for job_button in job_buttons:  
                #print('worked 7')
                print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
                if len(jobs) >= num_jobs:
                    break
                #print('worked 8')
                            
                job_button.click()  #You might 
                #print('worked 9')
                time.sleep(4)
                #print('worked 10')
                #___________ code to kill the sign-up pop-up after it render on screen
                # if not found_popup:
                try:
                    driver.find_element_by_css_selector('[alt="Close"]').click()
                    #print('worked 11')
                    # print("&&& line 89")
                    # found_popup = True
                except NoSuchElementException:
                    #print('worked 12')# print("&&& line 92")
                    pass
                          
                # __________
                
                
                collected_successfully = False
                #print('worked 13')
                while not collected_successfully:
                    try:
                        #print('worked 14')# company_name = driver.find_element_by_xpath('.//div[@class="employerName"]').text
                        company_name = driver.find_element_by_xpath('//*[@id="MainCol"]//li['+ str(currentJoblist + 1) +']//div[2]//a//span').text
                        
                        #print('worked 15')# location = driver.find_element_by_xpath('.//div[@class="location"]').text
                        location = driver.find_element_by_xpath('//*[@id="MainCol"]//li['+ str(currentJoblist + 1) +']//div[2]//div[2]/span').text
                        
                        #print('worked 16')# job_title = driver.find_element_by_xpath('.//div[contains(@class, "title")]').text
                        job_title = driver.find_element_by_xpath('//*[@id="MainCol"]//li['+ str(currentJoblist + 1) +']//a[@data-test="job-link"]').text
                        #print('worked 17')
                        job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                        
                        #print('worked 18')# job_function is an additional information not included in previous code
                        #job_function = driver.find_element_by_xpath('//*[@id="JDCol"]//strong[text()[1]="Job Function"]//following-sibling::*').text
                        job_function = driver.find_element_by_xpath('//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[3]/div[2]/div[2]/span').text
                        #print('worked 19')
                        collected_successfully = True
                        #print('worked 20')
                    except:
                        #print('worked 21')# print("&&& line 67")
                        # collected_successfully=True
                        time.sleep(5)
    
                try:
                    #print('worked 22')# salary_estimate = driver.find_element_by_xpath('.//span[@class="gray small salary"]').text
                    salary_estimate = driver.find_element_by_xpath('//*[@id="JDCol"]//span[@data-test="detailSalary"]').text
                except NoSuchElementException:
                    salary_estimate = -1 #You need to set a "not found value. It's important."
                    #print('worked 23')
                try:
                    #print('worked 24')# rating = driver.find_element_by_xpath('.//span[@class="rating"]').text
                    rating = driver.find_element_by_xpath('//*[@id="JDCol"]//span[@data-test="detailRating"]').text
                except NoSuchElementException:
                    rating = -1 #You need to set a "not found value. It's important."
                    #print('worked 25')
                # #Printing for debugging
                if verbose:
                    print("Job Title: {}".format(job_title))
                    print("Salary Estimate: {}".format(salary_estimate))
                    print("Job Description: {}".format(job_description[:500]))
                    print("Rating: {}".format(rating))
                    print("Company Name: {}".format(company_name))
                    print("Location: {}".format(location))
                    print("Job Function: {}".format(job_function))
    
                #Going to the Company tab...
                #clicking on this:
                #<div class="tab" data-tab-type="overview"><span>Company</span></div>
                time.sleep(1)
                try:
                    #print('worked 24')# driver.find_element_by_xpath('.//div[@class="tab" and @data-tab-type="overview"]').click()
                    driver.find_element_by_xpath('.//div[@id="SerpFixedHeader"]//span[text()="Company"]').click()
    
                #     try:
                #         #<div class="infoEntity">
                #         #    <label>Headquarters</label>
                #         #    <span class="value">San Francisco, CA</span>
                #         #</div>
                #         headquarters = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
                         # ^^^^^^^^^^ couldn't abel to find "headquarters"
                #     except NoSuchElementException:
                #         headquarters = -1
    
                    try:
                        # size = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
                        size = driver.find_element_by_xpath('.//div[@id="EmpBasicInfo"]//span[text()="Size"]//following-sibling::*').text
                    except NoSuchElementException:
                        size = -1
    
                    try:
                        # founded = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
                        founded = driver.find_element_by_xpath('.//div[@id="EmpBasicInfo"]//span[text()="Founded"]//following-sibling::*').text
                    except NoSuchElementException:
                        founded = -1
    
                    try:
                        # type_of_ownership = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
                        type_of_ownership = driver.find_element_by_xpath('.//div[@id="EmpBasicInfo"]//span[text()="Type"]//following-sibling::*').text
                    except NoSuchElementException:
                        type_of_ownership = -1
    
                    try:
                        # industry = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
                        industry = driver.find_element_by_xpath('.//div[@id="EmpBasicInfo"]//span[text()="Industry"]//following-sibling::*').text
                    except NoSuchElementException:
                        industry = -1
    
                    try:
                        # sector = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
                        sector = driver.find_element_by_xpath('.//div[@id="EmpBasicInfo"]//span[text()="Sector"]//following-sibling::*').text
                    except NoSuchElementException:
                        sector = -1
    
                    try:
                        # revenue = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
                        revenue = driver.find_element_by_xpath('.//div[@id="EmpBasicInfo"]//span[text()="Revenue"]//following-sibling::*').text
                    except NoSuchElementException:
                        revenue = -1
    
                #     try:
                #         competitors = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
                          # ^^^^^^^^^^^ couldn't able to find "competitors"
                #     except NoSuchElementException:
                #         competitors = -1
    
                except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
                #     headquarters = -1
                    size = -1
                    founded = -1
                    type_of_ownership = -1
                    industry = -1
                    sector = -1
                    revenue = -1
                #     competitors = -1
    
                    
                if verbose:
                    
                    print("Size: {}".format(size))
                    print("Founded: {}".format(founded))
                    print("Type of Ownership: {}".format(type_of_ownership))
                    print("Industry: {}".format(industry))
                    print("Sector: {}".format(sector))
                    print("Revenue: {}".format(revenue))
                    # print("Headquarters: {}".format(headquarters))
                    # print("Competitors: {}".format(competitors))
                    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    
                jobs.append({"Job Title" : job_title,           
                "Salary Estimate" : salary_estimate,
                "Job Function" : job_function,
                "Job Description" : job_description,            
                "Company Name" : company_name,
                "Rating" : rating,            
                "Location" : location,
                "Size" : size,
                "Founded" : founded,
                "Type of ownership" : type_of_ownership,
                "Industry" : industry,
                "Sector" : sector,
                "Revenue" : revenue})
                # "Headquarters" : headquarters,
                # "Competitors" : competitors})
                # ^^^^^^^^ couldn't able to find "Headquarters" and "Competitors"
                #add job to jobs
    
                currentJoblist=currentJoblist+1 # increasing the count of the list of buttons clicked and saved
                
                if not (currentJoblist < listButtonsCount): # to check the list last button and to go to next page
                        currentJoblist = 0  # resetting the button list count for new page button's list
                        break
            #Clicking on the "next page" button
            try:                
                # driver.find_element_by_xpath('.//li[@class="next"]//a').click()
                driver.find_element_by_xpath('//*[@id="FooterPageNav"]//a[@data-test="pagination-next"]').click()
                
            except NoSuchElementException:
                print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
                break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.