##### Note for users:

# 1. You might need to reconfigure this code depending on the interface size/device you are using
# I used the MacBook Pro 13-inch 2020 for this exercise

# 2. In order for this code to work, you have to create an account with topuniversities.com
# This is because when the webdriver opens Chrome, it starts a completely new/signed-out session
# The code does the login for you and will require your credentials

# Write the email and password you'd like to use here:
email = ""
password = ""

##### Now for the code:

# Import packages
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

# Go to topuniversities website and log in
browser = webdriver.Chrome()
browser.get('https://www.topuniversities.com/')
time.sleep(5)
browser.maximize_window()
browser.find_element(By.XPATH, '//*[@id="page"]/header/div[1]/div/div[2]/ul/li[4]/a').click()
time.sleep(10)
if email == "" or password == "":
    print("Email and password are required. Exiting the program.")
    exit()
browser.find_element(By.XPATH, '//*[@id="edit-name"]').send_keys(email)
browser.find_element(By.XPATH, '//*[@id="edit-pass"]').send_keys(password)
browser.find_element(By.XPATH, '//*[@id="edit-actions-submit"]').click()
time.sleep(10)

# Go to the top university rankings webpage
navbar_item = browser.find_element(By.XPATH, '//*[@id="top_menu"]/ul[1]/li[1]/a')
action_chains = ActionChains(browser)
action_chains.move_to_element(navbar_item).perform()
menu_item = browser.find_element(By.XPATH, '//*[@id="top_menu"]/ul[1]/li[1]/ul/li[2]/a')
menu_item.click()

##### Filter for 2021 data
    # Note the standard fields to parse: Rank and Uni
    # And the schema on this page: 
        # Overall Score
        # International Students Ratio
        # International Faculty Ratio
        # Faculty Student Ratio
        # Citations per Faculty
        # Academic Reputation
        # Employer Reputation

# Filter to 2021
browser.execute_script("window.scrollTo(0, 1440);")
time.sleep(5)
browser.find_element(By.XPATH, '//*[@id="filterAccordion"]/div[1]/div/div/div/div').click()
time.sleep(5)
browser.find_element(By.XPATH, '//*[@id="filterAccordion"]/div[1]/div/div/div/div/div[2]/div[1]').click()
time.sleep(10)

# Filter to only Australia
browser.find_element(By.XPATH, '//*[@id="locCont"]/div/div[2]/div/div').click()
time.sleep(5)
browser.find_element(By.XPATH, '//*[@id="locCont"]/div/div[2]/div/div/div[2]/div[2]').click()
time.sleep(10)

# Select the full view option
browser.find_element(By.XPATH, '//*[@id="it-will-be-fixed-top"]/div/div[1]/div/ul/li[2]/a').click()
time.sleep(5)

# Click 'load more' two times to show all results
browser.find_element(By.XPATH, '//*[@id="ranking-data-load"]/div[34]/div[2]/button').click()
time.sleep(5)
browser.find_element(By.XPATH, '//*[@id="ranking-data-load"]/div[65]/div[2]/button').click()
time.sleep(5)

# Start scraping the data
page_source = browser.page_source
qs_soup = BeautifulSoup(page_source, "html.parser")

Uni_rank_html = qs_soup.find_all('div', {"class": "_univ-rank"})
Uni_rank_html = [Uni_rank_html[i] for i in range(0, len(Uni_rank_html), 2)]
Uni_names_html = qs_soup.find_all('a', {"class": "uni-link"})
Uni_names_html = [Uni_names_html[i] for i in range(0, len(Uni_names_html), 2)]
Overall_score_html = qs_soup.find_all('div', {"class": "overall-score-span-ind overall"})
Int_students_ratio_html = qs_soup.find_all('div', {"class": 'overall-score-span-ind ind_14'})
Int_faculty_ratio_html = qs_soup.find_all('div', {"class": 'overall-score-span-ind ind_18'})

# Click the right button 2 times and collect the data again 
browser.find_element(By.XPATH, '//*[@id="it-will-be-fixed-top-filter"]/div/div/div/div[4]/span[2]').click()
time.sleep(3)
browser.find_element(By.XPATH, '//*[@id="it-will-be-fixed-top-filter"]/div/div/div/div[4]/span[2]').click()
time.sleep(5)

Faculty_student_ratio_html = qs_soup.find_all('div', {"class": 'overall-score-span-ind ind_36'})
Citations_per_faculty_html = qs_soup.find_all('div', {"class": 'overall-score-span-ind ind_73'})

# Click the right button 2 times and collect the data again 
browser.find_element(By.XPATH, '//*[@id="it-will-be-fixed-top-filter"]/div/div/div/div[4]/span[2]').click()
time.sleep(3)
browser.find_element(By.XPATH, '//*[@id="it-will-be-fixed-top-filter"]/div/div/div/div[4]/span[2]').click()
time.sleep(5)

Academic_reputation_html = qs_soup.find_all('div', {"class": 'overall-score-span-ind ind_76'})
Employer_reputation_html = qs_soup.find_all('div', {"class": 'overall-score-span-ind ind_77'})

### Optional: verify that list lengths are the same
# print(len(Uni_rank_html))
# print(len(Uni_names_html))
# print(len(Overall_score_html))
# print(len(Int_students_ratio_html))
# print(len(Int_faculty_ratio_html))
# print(len(Faculty_student_ratio_html))
# print(len(Citations_per_faculty_html))
# print(len(Academic_reputation_html))
# print(len(Employer_reputation_html))

# Get the text from all list items
Uni_rank = []
for item in Uni_rank_html:
    Uni_rank.append(item.getText())

Uni_names = []
for item in Uni_names_html:
    Uni_names.append(item.getText())

Overall_score = []
for item in Overall_score_html:
    Overall_score.append(item.getText())

Int_students_ratio = []
for item in Int_students_ratio_html:
    Int_students_ratio.append(item.getText())

Int_faculty_ratio = []
for item in Int_faculty_ratio_html:
    Int_faculty_ratio.append(item.getText())

Faculty_student_ratio = []
for item in Faculty_student_ratio_html:
    Faculty_student_ratio.append(item.getText())

Citations_per_faculty = []
for item in Citations_per_faculty_html:
    Citations_per_faculty.append(item.getText())

Academic_reputation = []
for item in Academic_reputation_html:
    Academic_reputation.append(item.getText())

Employer_reputation = []
for item in Employer_reputation_html:
    Employer_reputation.append(item.getText())

# Create a dataframe using all columns
df2021 = pd.DataFrame({
    'global rank': Uni_rank,
    'uni name': Uni_names,
    'overall score': Overall_score,
    'international students ratio': Int_students_ratio,
    'international faculty ratio': Int_faculty_ratio,
    'faculty student ratio': Faculty_student_ratio, 
    'citations_per_faculty': Citations_per_faculty,
    'academic reputation': Academic_reputation,
    'employer reputation': Employer_reputation
})

##### Filter 2022
    # Note the standard fields to parse: Rank and Uni
    # And the schema on this page: 
        # Overall Score
        # International Students Ratio
        # International Faculty Ratio
        # Faculty Student Ratio
        # Citations per Faculty
        # Academic Reputation
        # Employer Reputation

# Filter to 2022
browser.find_element(By.XPATH, '//*[@id="filterAccordion"]/div[1]/div/div/div/div').click()
time.sleep(5)
browser.find_element(By.XPATH, '//*[@id="filterAccordion"]/div[1]/div/div/div/div/div[2]/div[2]').click()
time.sleep(10)

# Filter to only Australia
browser.find_element(By.XPATH, '//*[@id="locCont"]/div/div[2]/div/div').click()
time.sleep(5)
browser.find_element(By.XPATH, '//*[@id="locCont"]/div/div[2]/div/div/div[2]/div[3]').click()
time.sleep(10)

# Select the full view option
browser.find_element(By.XPATH, '//*[@id="it-will-be-fixed-top"]/div/div[1]/div/ul/li[2]/a').click()
time.sleep(5)

# Click 'load more' two times to show all results
browser.find_element(By.XPATH, '//*[@id="ranking-data-load"]/div[34]/div[2]/button').click()
time.sleep(5)
browser.find_element(By.XPATH, '//*[@id="ranking-data-load"]/div[65]/div[2]/button').click()
time.sleep(5)

# Start scraping
page_source = browser.page_source
qs_soup = BeautifulSoup(page_source, "html.parser")

Uni_rank_html = qs_soup.find_all('div', {"class": "_univ-rank"})
Uni_rank_html = [Uni_rank_html[i] for i in range(0, len(Uni_rank_html), 2)]
Uni_names_html = qs_soup.find_all('a', {"class": "uni-link"})
Uni_names_html = [Uni_names_html[i] for i in range(0, len(Uni_names_html), 2)]
Overall_score_html = qs_soup.find_all('div', {"class": "overall-score-span-ind overall"})
Int_students_ratio_html = qs_soup.find_all('div', {"class": 'overall-score-span-ind ind_14'})
Int_faculty_ratio_html = qs_soup.find_all('div', {"class": 'overall-score-span-ind ind_18'})

# Click the right button 2 times and collect the data again 
browser.find_element(By.XPATH, '//*[@id="it-will-be-fixed-top-filter"]/div/div/div/div[4]/span[2]').click()
time.sleep(3)
browser.find_element(By.XPATH, '//*[@id="it-will-be-fixed-top-filter"]/div/div/div/div[4]/span[2]').click()
time.sleep(5)

Faculty_student_ratio_html = qs_soup.find_all('div', {"class": 'overall-score-span-ind ind_36'})
Citations_per_faculty_html = qs_soup.find_all('div', {"class": 'overall-score-span-ind ind_73'})

# Click the right button 2 times and collect the data again 
browser.find_element(By.XPATH, '//*[@id="it-will-be-fixed-top-filter"]/div/div/div/div[4]/span[2]').click()
time.sleep(3)
browser.find_element(By.XPATH, '//*[@id="it-will-be-fixed-top-filter"]/div/div/div/div[4]/span[2]').click()
time.sleep(5)

Academic_reputation_html = qs_soup.find_all('div', {"class": 'overall-score-span-ind ind_76'})
Employer_reputation_html = qs_soup.find_all('div', {"class": 'overall-score-span-ind ind_77'})

# Get text from all list items
Uni_rank = []
for item in Uni_rank_html:
    Uni_rank.append(item.getText())

Uni_names = []
for item in Uni_names_html:
    Uni_names.append(item.getText())

Overall_score = []
for item in Overall_score_html:
    Overall_score.append(item.getText())

Int_students_ratio = []
for item in Int_students_ratio_html:
    Int_students_ratio.append(item.getText())

Int_faculty_ratio = []
for item in Int_faculty_ratio_html:
    Int_faculty_ratio.append(item.getText())

Faculty_student_ratio = []
for item in Faculty_student_ratio_html:
    Faculty_student_ratio.append(item.getText())

Citations_per_faculty = []
for item in Citations_per_faculty_html:
    Citations_per_faculty.append(item.getText())

Academic_reputation = []
for item in Academic_reputation_html:
    Academic_reputation.append(item.getText())

Employer_reputation = []
for item in Employer_reputation_html:
    Employer_reputation.append(item.getText())

# Create a dataframe using all the columns
df2022 = pd.DataFrame({
    'global rank': Uni_rank,
    'uni name': Uni_names,
    'overall score': Overall_score,
    'international students ratio': Int_students_ratio,
    'international faculty ratio': Int_faculty_ratio,
    'faculty student ratio': Faculty_student_ratio, 
    'citations_per_faculty': Citations_per_faculty,
    'academic reputation': Academic_reputation,
    'employer reputation': Employer_reputation
})

##### Filter 2023
    # Notethe standard fields to parse: Rank and Uni
    # And the schema on this page: 
        # Overall Score 
        # Academic Reputation
        # Employer Reputation
        # Citations per Faculty
        # Faculty Student Ratio
        # International Students Ratio
        # International Faculty Ratio
        # International Research Network
        # Employment Outcomes

# Filter to 2023
browser.find_element(By.XPATH, '//*[@id="filterAccordion"]/div[1]/div/div/div/div').click()
time.sleep(5)
browser.find_element(By.XPATH, '//*[@id="filterAccordion"]/div[1]/div/div/div/div/div[2]/div[3]').click()
time.sleep(10)

# Filter to only Australia
browser.find_element(By.XPATH, '//*[@id="locCont"]/div/div[2]/div/div').click()
time.sleep(5)
browser.find_element(By.XPATH, '//*[@id="locCont"]/div/div[2]/div/div/div[2]/div[3]').click()
time.sleep(10)

# Select the full view option
browser.find_element(By.XPATH, '//*[@id="it-will-be-fixed-top"]/div/div[1]/div/ul/li[2]/a').click()
time.sleep(5)

# Click 'load more' two times to show all results
browser.find_element(By.XPATH, '//*[@id="ranking-data-load"]/div[34]/div[2]/button').click()
time.sleep(5)
browser.find_element(By.XPATH, '//*[@id="ranking-data-load"]/div[66]/div[2]/button').click()
time.sleep(5)

# Start scraping
page_source = browser.page_source
qs_soup = BeautifulSoup(page_source, "html.parser")

Uni_rank_html = qs_soup.find_all('div', {"class": "_univ-rank"})
Uni_rank_html = [Uni_rank_html[i] for i in range(0, len(Uni_rank_html), 2)]
Uni_names_html = qs_soup.find_all('a', {"class": "uni-link"})
Uni_names_html = [Uni_names_html[i] for i in range(0, len(Uni_names_html), 2)]
Overall_score_html = qs_soup.find_all('div', {"class": "overall-score-span-ind overall"})
Academic_reputation_html = qs_soup.find_all('div', {"class": 'overall-score-span-ind ind_76'})
Employer_reputation_html = qs_soup.find_all('div', {"class": 'overall-score-span-ind ind_77'})

# Click the right button 2 times and collect the data again 
browser.find_element(By.XPATH, '//*[@id="it-will-be-fixed-top-filter"]/div/div/div/div[4]/span[2]').click()
time.sleep(3)
browser.find_element(By.XPATH, '//*[@id="it-will-be-fixed-top-filter"]/div/div/div/div[4]/span[2]').click()
time.sleep(5)

Citations_per_faculty_html = qs_soup.find_all('div', {"class": 'overall-score-span-ind ind_73'})
Faculty_student_ratio_html = qs_soup.find_all('div', {"class": 'overall-score-span-ind ind_36'})

# Click the right button 2 times and collect the data again 
browser.find_element(By.XPATH, '//*[@id="it-will-be-fixed-top-filter"]/div/div/div/div[4]/span[2]').click()
time.sleep(3)
browser.find_element(By.XPATH, '//*[@id="it-will-be-fixed-top-filter"]/div/div/div/div[4]/span[2]').click()
time.sleep(5)

Int_students_ratio_html = qs_soup.find_all('div', {"class": 'overall-score-span-ind ind_14'})
Int_faculty_ratio_html = qs_soup.find_all('div', {"class": 'overall-score-span-ind ind_18'})

# Click the right button 2 times and collect the data again 
browser.find_element(By.XPATH, '//*[@id="it-will-be-fixed-top-filter"]/div/div/div/div[4]/span[2]').click()
time.sleep(3)
browser.find_element(By.XPATH, '//*[@id="it-will-be-fixed-top-filter"]/div/div/div/div[4]/span[2]').click()
time.sleep(5)

research_network_html = qs_soup.find_all('div', {"class": 'overall-score-span-ind ind_15'})
employment_outcomes_html = qs_soup.find_all('div', {"class": 'overall-score-span-ind ind_3819456'})

# Get text from all list items
Uni_rank = []
for item in Uni_rank_html:
    Uni_rank.append(item.getText())

Uni_names = []
for item in Uni_names_html:
    Uni_names.append(item.getText())

Overall_score = []
for item in Overall_score_html:
    Overall_score.append(item.getText())

Academic_reputation = []
for item in Academic_reputation_html:
    Academic_reputation.append(item.getText())

Employer_reputation = []
for item in Employer_reputation_html:
    Employer_reputation.append(item.getText())

Citations_per_faculty = []
for item in Citations_per_faculty_html:
    Citations_per_faculty.append(item.getText())

Faculty_student_ratio = []
for item in Faculty_student_ratio_html:
    Faculty_student_ratio.append(item.getText())

Int_students_ratio = []
for item in Int_students_ratio_html:
    Int_students_ratio.append(item.getText())

Int_faculty_ratio = []
for item in Int_faculty_ratio_html:
    Int_faculty_ratio.append(item.getText())

research_network = []
for item in research_network_html:
    research_network.append(item.getText())

employment_outcomes = []
for item in employment_outcomes_html:
    employment_outcomes.append(item.getText())

# Create a dataframe using all columns
df2023 = pd.DataFrame({
    'global rank': Uni_rank,
    'uni name': Uni_names,
    'overall score': Overall_score,
    'international students ratio': Int_students_ratio,
    'international faculty ratio': Int_faculty_ratio,
    'faculty student ratio': Faculty_student_ratio, 
    'citations_per_faculty': Citations_per_faculty,
    'academic reputation': Academic_reputation,
    'employer reputation': Employer_reputation,
    'international research network': research_network,
    'employment outcomes': employment_outcomes
})

##### Filter 2024
    # Note the standard fields to parse: Rank and Uni
    # And the schema on this page: 
        # Overall Score 
        # Academic Reputation
        # Employer Reputation
        # Faculty Student Ratio
        # Citations per Faculty
        # International Faculty Ratio
        # International Students Ratio
        # International Research Network
        # Employment Outcomes
        # Sustainability

# Filter to 2024
browser.find_element(By.XPATH, '//*[@id="filterAccordion"]/div[1]/div/div/div/div').click()
time.sleep(5)
browser.find_element(By.XPATH, '//*[@id="filterAccordion"]/div[1]/div/div/div/div/div[2]/div[4]').click()
time.sleep(10)

# Filter to only Australia
browser.find_element(By.XPATH, '//*[@id="locCont"]/div/div[2]/div/div').click()
time.sleep(5)
browser.find_element(By.XPATH, '//*[@id="locCont"]/div/div[2]/div/div/div[2]/div[3]').click()
time.sleep(10)

# Select the full view option
browser.find_element(By.XPATH, '//*[@id="it-will-be-fixed-top"]/div/div[1]/div/ul/li[2]/a').click()
time.sleep(5)

# Click 'load more' two times to show all results
browser.find_element(By.XPATH, '//*[@id="ranking-data-load"]/div[34]/div[2]/button').click()
time.sleep(5)
browser.find_element(By.XPATH, '//*[@id="ranking-data-load"]/div[66]/div[2]/button').click()
time.sleep(5)

# Start scraping
page_source = browser.page_source
qs_soup = BeautifulSoup(page_source, "html.parser")

Uni_rank_html = qs_soup.find_all('div', {"class": "_univ-rank"})
Uni_rank_html = [Uni_rank_html[i] for i in range(0, len(Uni_rank_html), 2)]
Uni_names_html = qs_soup.find_all('a', {"class": "uni-link"})
Uni_names_html = [Uni_names_html[i] for i in range(0, len(Uni_names_html), 2)]
Overall_score_html = qs_soup.find_all('div', {"class": "overall-score-span-ind overall"})
Academic_reputation_html = qs_soup.find_all('div', {"class": 'overall-score-span-ind ind_76'})
Employer_reputation_html = qs_soup.find_all('div', {"class": 'overall-score-span-ind ind_77'})

# Click the right button 2 times and collect the data again 
browser.find_element(By.XPATH, '//*[@id="it-will-be-fixed-top-filter"]/div/div/div/div[4]/span[2]').click()
time.sleep(3)
browser.find_element(By.XPATH, '//*[@id="it-will-be-fixed-top-filter"]/div/div/div/div[4]/span[2]').click()
time.sleep(5)

Faculty_student_ratio_html = qs_soup.find_all('div', {"class": 'overall-score-span-ind ind_36'})
Citations_per_faculty_html = qs_soup.find_all('div', {"class": 'overall-score-span-ind ind_73'})

# Click the right button 2 times and collect the data again 
browser.find_element(By.XPATH, '//*[@id="it-will-be-fixed-top-filter"]/div/div/div/div[4]/span[2]').click()
time.sleep(3)
browser.find_element(By.XPATH, '//*[@id="it-will-be-fixed-top-filter"]/div/div/div/div[4]/span[2]').click()
time.sleep(5)

Int_faculty_ratio_html = qs_soup.find_all('div', {"class": 'overall-score-span-ind ind_18'})
Int_students_ratio_html = qs_soup.find_all('div', {"class": 'overall-score-span-ind ind_14'})

# Click the right button 2 times and collect the data again 
browser.find_element(By.XPATH, '//*[@id="it-will-be-fixed-top-filter"]/div/div/div/div[4]/span[2]').click()
time.sleep(3)
browser.find_element(By.XPATH, '//*[@id="it-will-be-fixed-top-filter"]/div/div/div/div[4]/span[2]').click()
time.sleep(5)

research_network_html = qs_soup.find_all('div', {"class": 'overall-score-span-ind ind_15'})
employment_outcomes_html = qs_soup.find_all('div', {"class": 'overall-score-span-ind ind_3819456'})

# Click the right button 2 times and collect the data again 
browser.find_element(By.XPATH, '//*[@id="it-will-be-fixed-top-filter"]/div/div/div/div[4]/span[2]').click()
time.sleep(3)
browser.find_element(By.XPATH, '//*[@id="it-will-be-fixed-top-filter"]/div/div/div/div[4]/span[2]').click()
time.sleep(5)

Sustainability_html = qs_soup.find_all('div', {"class": 'overall-score-span-ind ind_3897497'})

# Get text from all list items
Uni_rank = []
for item in Uni_rank_html:
    Uni_rank.append(item.getText())

Uni_names = []
for item in Uni_names_html:
    Uni_names.append(item.getText())

Overall_score = []
for item in Overall_score_html:
    Overall_score.append(item.getText())

Academic_reputation = []
for item in Academic_reputation_html:
    Academic_reputation.append(item.getText())

Employer_reputation = []
for item in Employer_reputation_html:
    Employer_reputation.append(item.getText())

Citations_per_faculty = []
for item in Citations_per_faculty_html:
    Citations_per_faculty.append(item.getText())

Faculty_student_ratio = []
for item in Faculty_student_ratio_html:
    Faculty_student_ratio.append(item.getText())

Int_students_ratio = []
for item in Int_students_ratio_html:
    Int_students_ratio.append(item.getText())

Int_faculty_ratio = []
for item in Int_faculty_ratio_html:
    Int_faculty_ratio.append(item.getText())

research_network = []
for item in research_network_html:
    research_network.append(item.getText())

employment_outcomes = []
for item in employment_outcomes_html:
    employment_outcomes.append(item.getText())

Sustainability = []
for item in Sustainability_html:
    Sustainability.append(item.getText())

# Create a dataframe using all columns
df2024 = pd.DataFrame({
    'global rank': Uni_rank,
    'uni name': Uni_names,
    'overall score': Overall_score,
    'international students ratio': Int_students_ratio,
    'international faculty ratio': Int_faculty_ratio,
    'faculty student ratio': Faculty_student_ratio, 
    'citations_per_faculty': Citations_per_faculty,
    'academic reputation': Academic_reputation,
    'employer reputation': Employer_reputation,
    'international research network': research_network,
    'employment outcomes': employment_outcomes,
    'sustainability': Sustainability
})

# Quit 
browser.quit()

# Optional: print the first row to cross-check with the webpage data
# print(df2021.iloc[0])
# print(df2022.iloc[0])
# print(df2023.iloc[0])
# print(df2024.iloc[0])

# Combine the dataframes into one, using a union
df2021['year'] = 2021
df2022['year'] = 2022
df2023['year'] = 2023
df2024['year'] = 2024

df = pd.concat([df2021, df2022, df2023, df2024], ignore_index=True, sort=False)

### Clean all columns except uni name, by removing newlines
columns_to_clean = df.columns.tolist()
columns_to_clean.remove('uni name')
df[columns_to_clean] = df[columns_to_clean].replace({r'\n': ''}, regex=True)

### Output data to a text file
csv_file_path = 'qsrankingsdata.csv'
df.to_csv(csv_file_path, index=False)

### Output message
print(f'DataFrame has been successfully saved to {csv_file_path}')

