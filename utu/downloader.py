from .endpoints import *
from .utils import *
from io import BytesIO
import requests 
from zipfile import ZipFile

class Downloader:
    
    def __init__(self) -> None:
        pass    

    def get_papers(self, year: int, season: str) -> dict:

        url = QUESTION_PAPERS.format(academic_year=resolve_academic_year(year, season), season=season, year=year)
        
        response = requests.get(url)

        return parse_html(response.text, season)
    
    def download_zip(self, url: str) -> str:
        url = ZIP_URL.format(zip_url=url)
        
        response = requests.get(url)
        
        with ZipFile(BytesIO(response.content)) as zipf:
            files = {}
            for file_name in zipf.namelist():
                if file_name.endswith('.pdf'):
                    data = zipf.read(file_name)
                    if data: files[file_name] = data 
                
        return files