import json
from bs4 import BeautifulSoup
import requests
from api.errors.crawler_error import CrawlerError

"""
Function that crawls the html menu from the studentenwerk website and returns it as json.
"""
def mensa_meals_as_dict(date:str, location:str):
    try:
        response = requests.get(f"https://www.studentenwerk-goettingen.de/fileadmin/templates/php/mensaspeiseplan/cached/d/{date}/{location}.html")
        my_str_as_bytes = str.encode(response.text, encoding='ISO-8859-1')
        html_text = my_str_as_bytes.decode('UTF-8')
        soup = BeautifulSoup(html_text, 'html.parser')
        table = soup.find('table', {'class': 'sp_tab'})

        meals = []

        for row in table.find_all('tr')[1:]:
            cells = row.find_all('td')
            meal_type = cells[0].text.strip()
            meal_name = cells[1].find('strong').text.strip() if cells[1].find('strong') else ""

            br_tags = cells[1].find_all('br')
            siblings = [tag.next_sibling for tag in br_tags]

            # print the text between the br tags
            meal_ingredients = (''.join([str(sibling) for sibling in siblings if sibling is not None and sibling.name != 'i']))
            meal_content = cells[1].find('i', {'class': 'smaller'}).text.strip() if cells[1].find('i', {'class': 'smaller'}) else ""
            meal_content = meal_content.replace("(", "").replace(")", "")

            meal = {
                'type': meal_type,
                'name': meal_name,
                'meal_ingredients' : meal_ingredients,
                'content': meal_content,
            }

            meals.append(meal)

        return {'location': soup.find(class_='sp_date').previous.text.strip(),'date': soup.find(class_='sp_date').text.strip(), 'meals': meals}
    except:
        raise CrawlerError("Error while crawling the mensa meals")