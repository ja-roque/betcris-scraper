from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.firefox.options import Options
import time
import datetime

import csv

format_str = '%m/ %d'
now = datetime.datetime.now()

url = "https://www.betcris.com/es"
username=""
password=""

driver = webdriver.Firefox()
driver.get( url )

# after_surfing_link = WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, '//form//input[@id="account"]')))

user_input    = driver.find_element_by_xpath("//form//input[@id='account']")
pw_input      = driver.find_element_by_xpath("//form//input[@id='password']")
submit_input  = driver.find_element_by_xpath("//form//input[@type='submit']")

user_input.send_keys(username)
pw_input.send_keys(password)
submit_input.click()

WebDriverWait(driver, 60).until(expected_conditions.presence_of_element_located((By.XPATH, './/div[@class="sports-schedule american-schedule"]')))

xpath_decimal_dropdown_link = ".//*[@id='wagerls_decimal']"

driver.execute_script("$('#wagerls_decimal')[0].click()")

xpath_league_in_box = ".//div[@class='sports-league']"
xpath_titulo = ".//div[@class='sports-league-banner']/a"
xpath_sidebar_leagues = "//a[@type='league']"
xpath_sidebar_soccer_leagues = ".//a[@cat='SOCCER']/following-sibling::app-sports//div[@data-parent='#leagues']//a[@type='league']"

xpath_games_in_league = ".//*[contains(@class, 'sports-league-game ')]"

xpath_game_date	=	".//*[contains(@class, 'game-time')]/span"
xpath_game_time	=	"..//*[contains(@class, 'game-time')]/span"

xpath_game_visitor	=	".//*[@class='visitor']/span"
xpath_game_home		=	".//*[@class='home']/span"

xpath_game_visitor_odd	=	".//div[@class='mline-1']//*[@class='odds']"
xpath_game_home_odd	=	".//div[@class='mline-2']//*[@class='odds']"
xpath_game_draw_odd	=	".//div[@class='mline-X']//*[@class='odds']"

xpath_game_over_odd = ".//div[@class='ou']//span[@class='odds']"
xpath_game_under_odd = ".//div[@class='ou']//span[@class='odds']"

gameRecords = []
WebDriverWait(driver, 5)
leagueInBox = ""

WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, xpath_sidebar_soccer_leagues)))
with open('betcris_juegos '+ str(now.day) +"-"+ str(now.month) + "-"+ str(now.year) +'.csv', 'w') as writeFile:
	writer = csv.writer(writeFile)
	writer.writerow(['Liga', 'Dia','Hora', 'Visita', 'Local', 'cuota_visita', 'cuota_local', 'cuota_empate', 'cuota_over', 'cuota_under'])

	soccerLeagues = driver.find_elements_by_xpath(xpath_sidebar_soccer_leagues)
	for league in soccerLeagues:
		print("in soccerLeagues")
		league.click() if league.get_attribute("class") != "selected" else ""
		WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, xpath_league_in_box)))
		leagueInBox = driver.find_elements_by_xpath(xpath_league_in_box)	

		for gameDay in leagueInBox:
			print("in leagueInBox")
			WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, xpath_titulo)))
			current_league = gameDay.find_element_by_xpath(xpath_titulo).text
			gamesInDay = gameDay.find_elements_by_xpath(xpath_games_in_league)

			for game in gamesInDay:
				print("in gamesInDay")
				try:
					WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, xpath_game_visitor)))
					game_record = {}
					game_record['league'] = current_league
					game_record['date'] = game.find_elements_by_xpath(xpath_game_date)[0].text
					game_record['time'] = game.find_elements_by_xpath(xpath_game_time)[1].text
					game_record['visitor'] = game.find_element_by_xpath(xpath_game_visitor).text
					game_record['home'] = game.find_element_by_xpath(xpath_game_home).text
					game_record['visitor_odd'] = game.find_element_by_xpath(xpath_game_visitor_odd).text
					game_record['home_odd'] = game.find_element_by_xpath(xpath_game_home_odd).text
					game_record['draw_odd'] = game.find_element_by_xpath(xpath_game_draw_odd).text
					game_record['over_odd'] = game.find_elements_by_xpath(xpath_game_over_odd)[0].text
					game_record['under_odd'] = game.find_elements_by_xpath(xpath_game_under_odd)[1].text
					print("print in progress...")
					writer.writerow([game_record['league'], game_record['date'], game_record['time'], game_record['visitor'], game_record['home'], game_record['visitor_odd'], game_record['home_odd'], game_record['draw_odd'], game_record['over_odd'],  game_record['under_odd']])
					pass
				except Exception as e:
					print (e)
print("finished printing...")
writeFile.close()

	    


