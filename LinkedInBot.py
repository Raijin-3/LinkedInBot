from selenium import webdriver
import time
import pandas

URL = "https://www.careerguide.com/career-options"

#setting up selenium chrome driver
chrome_driver_path = "E:\\Python\\Selenium\\chromedriver.exe"
driver = webdriver.Chrome(executable_path= chrome_driver_path)

driver.get(URL)

#if you get security error then for manually proceding to next step you need time
time.sleep(10)

#------------------------------------Part1----------------------------
cat_list = []
subcat_list =[]

#Getting the categories and subcategories
category = driver.find_elements_by_tag_name('h2')

for item in category:
    cat_list.append(item.text)

    
ul_list = driver.find_elements_by_class_name('c-theme')
for item in ul_list:
    sub_category = item.find_elements_by_tag_name('li')

    for kitem in sub_category:
        subcat_list.append(kitem.text)
        
data = {"category":cat_list, "subCategory": subcat_list}


#------------------------------------Part2-----------------------------
#List of american states and geo-location
states = {'Alabama':102240587,'Alaska':100290991,'Arizona':106032500,'Arkansas':102790221,'California':102095887,'Colorado':105763813,'Connecticut':106914527,'Delaware':105375497,'Florida':101318387,'Georgia':103950076,'Hawaii':105051999,'Idaho':102560739,'Illinois':101949407,'Indiana':103336534,'Iowa':103078544,'Kansas':104403803,'Kentucky':106470801,'Louisiana':101822552,'Maine':101102875,'Maryland':100809221,'Massachusetts':101098412,'Michigan':103051080,'Minnesota':103411167,'Mississippi':106899551,'Missouri':101486475,'Montana':101758306,'Nebraska':101197782,'Nevada':101690912}



    
#logging in into the LinkedIn
new_url = "https://www.linkedin.com/login"
driver.get(new_url)

email_id = 'your email'
password = 'your password'

username_searchBox = driver.find_elements_by_xpath('//*[@id="username"]')
for item in username_searchBox:
    item.send_keys(email_id)
    
    
password_searchBox = driver.find_element_by_xpath('//*[@id="password"]')
password_searchBox.send_keys(password)
password_searchBox.send_keys('\ue007')

#sending the enter key after touching the link
job_linkBar = driver.find_element_by_xpath('//*[@id="ember20"]')
job_linkBar.send_keys('\ue007')

time.sleep(5)


#building each link for each subcategory or job designation scraped earlier
link_list=[]
for item in states:
    for jitem in subcat_list:
        
        #The pattern of url is pretty much same for every company
        job_url = f"https://www.linkedin.com/jobs/search/?geoId={states[item]}&keywords={jitem}&location={item}%2C%20United%20States"
        job_url.replace(' ','%20')
        link_list.append(job_url)
        
part2Soluion =[]
 
#looping each link and getting the position name, company name and location   
for link in link_list:
    driver.get(link)
    job_list = driver.find_elements_by_class_name("occludable-update")
    for job in job_list:
        driver.execute_script("arguments[0].scrollIntoView();", job)
        job.click()
        time.sleep(5)
        try:
            details = job.text.split('\n')[:3]
            part2Soluion.append(details)
        except:
            print("Not sufficient item to store")
            job.click()
        print(details)

df = pandas.DataFrame(part2Soluion)
df.to_csv('jobDetails.csv', index=False, header=False)
