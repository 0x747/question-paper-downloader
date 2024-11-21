import base64
from typing import Any
from bs4 import BeautifulSoup, ResultSet
from urllib.parse import quote

def parse_table(html: ResultSet[Any] | str) -> dict:
    data = {}
    for row in html.find_all('tr')[1:]:
        cells = row.find_all('td')
        course = cells[0].get_text(strip=True).replace('td>', '')
        values = {}

        for index, cell in enumerate(cells[1:]):
            a = cell.find('a', href=True)
            zip_link = a['href'] if a else None
            if zip_link is not None: values[index + 1] = quote(zip_link)
        
        data[course] = values
    
    return data

def parse_html(html: str, season: str) -> dict:
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table')
    
    if season.lower() == 'summer' and tables:
        return parse_table(tables[0])
    elif season.lower() == 'winter' and tables:
        table_index = 1 if len(tables) == 2 else 0
        return parse_table(tables[table_index])
    
    return {'error': 'Not found'} 


def resolve_academic_year(year: int, season: str) -> str:
    if season.lower() == 'winter':
        academic_year = f'{year}-{str(year + 1)[-2:]}'
    elif season.lower() == 'summer':
        academic_year = f'{year - 1}-{str(year)[-2:]}'
    else:
        raise ValueError("Argument 'season' must be 'Summer' or 'Winter'")
    
    return academic_year

def b64encode_filter(data):
    if isinstance(data, bytes):
        return base64.b64encode(data).decode('utf-8')
    return ''