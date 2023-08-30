from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import csv

target_xpath = "/html/body/center/form/table/tbody/tr[8]/td/table/tbody/tr[5]/td"

data = [
    ["Pruefungstermin", "Ergebnis bundesweit", "Ergebnis NRW", "Ergebnis Koeln"]
]

query_parameter = (
  'Fachinformatiker/-in Fachrichtung: Anwendungsentwicklung',
  'bundesweit',
  'Nordrhein-Westfalen',
  'Köln'
)
season_list = []

driver = webdriver.Firefox()
driver.get("https://pes.ihk.de/")

season_values = Select(driver.find_element(by=By.NAME , value="termin"))

for item in season_values.options:
  season_list.append(item.text)
  
driver.quit()

def grab_data(current_season):
  driver = webdriver.Firefox()
  driver.get("https://pes.ihk.de/")
  
  data_row = [current_season.replace(" ","")]

  season_selection = Select(driver.find_element(by=By.NAME , value="termin"))
  season_selection.select_by_visible_text(current_season)
   
  job_selection = Select(driver.find_element(by=By.CLASS_NAME, value="berufe"))
  job_selection.select_by_visible_text(query_parameter[0])
    
  scope_selection_global = Select(driver.find_element(by=By.NAME, value="pm1"))
  scope_selection_global.select_by_visible_text(query_parameter[1])
    
  scope_selection_regional = Select(driver.find_element(by=By.NAME, value="pm2"))
  scope_selection_regional.select_by_visible_text(query_parameter[2])
    
  scope_selection_local = Select(driver.find_element(by=By.NAME, value="pm3"))
  scope_selection_local.select_by_visible_text(query_parameter[3])

  WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, target_xpath)))
    
  matches = driver.find_elements(by = By.XPATH, value = target_xpath)
  only_data_matches = matches [1
    
  for values in only_data_matches:
    cleaned_value = values.text.replace(",", ".").replace(" %", "")
    data_row.append(float(cleaned_value))
  
  driver.quit()
  return data_row
    
for i in range(5):                    # Testlauf - kurz
# for i in range(len(season_list)):   # echter Durchlauf - lang
  row = grab_data(season_list[i])
  data.append(row)

csv_file_path = "output.csv"

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerows(data)
