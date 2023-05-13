from bs4 import BeautifulSoup
import requests
import datetime

url = "https://tickets.funcode.hu/event/rammstein-d-2023"

result = requests.get(url)
#print(result.text)
doc = BeautifulSoup(result.text, "html.parser")

# availability = doc.find_all(string="Elfogyott")
# print(availability)
# parent = availability[0].parent
# print(parent)
# print(parent.string)

availability = doc.findAll(string="Manuális")
print(availability)

# availability = doc.find_all(string="em")
# print(availability)
# parent = 'em'
# print(parent.string)


# elso = availability[0].string
# masodik = availability[1].string
# harmadik = availability[2].string
# print('elso '+elso)
# print('masodik '+masodik)
# print('harmadik '+harmadik)

# datetag = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
# filename = 'scraping_output_'+datetag+'.html'
# print('The saved file is:'+filename)
# f = open(filename,"w")
# f.write(result.text)
# f.close()