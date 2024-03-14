import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup as soup

# Setting up Selenium and navigating to the website
driver = webdriver.Edge()
driver.get(url='https://www.iplt20.com/stats/2023')

try:
    # Define wait object with a timeout of 10 seconds
    wait = WebDriverWait(driver, 10)

    # Wait for the batting tab to be clickable and click on it
    batting_tab = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="battingTAB"]/div/a')))
    batting_tab.click()

    # Wait for the table with player data to appear
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.st-table.statsTable.ng-scope')))

    # Get the page source after the JavaScript execution
    page_source = driver.page_source

except TimeoutException:
    print("Timeout occurred while waiting for elements to load.")

finally:
    # Closing the webdriver
    driver.quit()

# Parse the page source using BeautifulSoup
soup_page = soup(page_source, 'html.parser')

# Extract images
player_images = [img_element.find('img')['src'] for img_element in soup_page.select('div.pbi img')]
if not player_images:
    print("Images not found.")

# Extract player profiles
player_profiles = soup_page.select('table.st-table.statsTable.ng-scope tr')[1:]
players_data = [[data.text for data in profile.select('td')[2:]] for profile in player_profiles]

# Extract player names
player_names = [name_element.text for name_element in soup_page.select('div.st-ply-name.ng-binding')]

# Extract team names
team_names = [team_element.text for team_element in soup_page.select('div.st-ply-tm-name.ng-binding')]

# Create DataFrame
data = pd.DataFrame(players_data, columns=['Mat', 'Inns', 'NO', 'Runs', 'HS', 'Avg', 'BF', 'SR', '100', '50', '4s', '6s'])
data['Team'] = team_names
data['Player Name'] = player_names
data['Image URL'] = player_images

# Save data to CSV
data.to_csv('All_players_2023.csv', index=False)