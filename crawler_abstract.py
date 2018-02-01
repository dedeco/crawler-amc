from pyvirtualdisplay import Display

from selenium import webdriver

from bs4 import BeautifulSoup

import time

import csv

import argparse

from utils import limpa_unicode

def export_to_csv(rows):

	print (rows)

	file = './data/with_abstract.csv'

	print(u'Exportando para csv...')

	header = ["type","id","author","editor","advisor","note","title","pages","article_no",\
				"num_pages","keywords","doi","journal","issue_date","volume","issue_no",\
				"description","month","year","issn","booktitle","acronym","edition","isbn",\
				"conf_loc","publisher","publisher_loc","abstract"]

	with open(file, 'w', encoding='utf-8') as csvfile:
		outcsv = csv.writer(csvfile, delimiter=',',quotechar='"', quoting = csv.QUOTE_MINIMAL)

		outcsv.writerow(header)    

		for row in rows:
			outcsv.writerow(row)    

def crawler(file):

	articles = []

	#file = './data/ACMDL201801283245326.csv'

	with open(file, newline='') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in spamreader:
			articles.append(row)

	display = Display(visible=0, size=(800, 600))
	display.start()
	driver = webdriver.Chrome()

	rows = []

	for row in articles[1:]:

		URL =('https://dl.acm.org/citation.cfm?id=%s' %row[1]) 
		
		driver.get(URL)

		time.sleep(1) 
		
		soup = BeautifulSoup(driver.page_source, 'html.parser')
		abstract = soup.find("div",{"id": "cf_layoutareaabstract"})

		rows.append(row + [limpa_unicode(abstract.text.strip())]) 

	driver.close()

	export_to_csv(rows)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("file", help=u"Informe o arquivo csv exportado da ACM (tem que ser padrão da ACM).\
		Os resumos serão buscados automaticamente e será criado um novo csv com a coluna de abstract.")
	
	args = parser.parse_args()

	crawler(args.file)
