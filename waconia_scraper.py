import os
import json
import requests
from bs4 import BeautifulSoup
from typing import Optional,List
from person_dataclass import Person_Data
from headers import pagination_headers,html_page_headers


class Waconia_Scraper:
    
    def __init__(self, proxy:dict = {}, debug:bool = False) -> None:
        
        self.debug = debug 
        self.session = requests.Session()
        self.session.proxies.update(proxy)
        self.all_extracted_data = []

    def __save_html_page(self, starting_page_response:Optional[requests.session]) -> None:
        
        current_wroking_dir = os.getcwd()
        with open(f"{current_wroking_dir}/front_page.html","wb") as html_file:
            html_file.write(starting_page_response.content)
            
    def __extract_fields(self, soup:Optional[BeautifulSoup],selector:str) -> None:

        if selector=="HTML":
            raw_personal_details_css_selector = '#node-32 > div > div.paragraph.staff.default > div > div.views-row'
        
        elif selector=='API':
            raw_personal_details_css_selector = 'div > div.views-row'
            
        all_raw_personal_details_html_tags = soup.select(raw_personal_details_css_selector)
        for raw_personal_details_html_tag in all_raw_personal_details_html_tags:
            raw_name_location_designation = raw_personal_details_html_tag.select('div > div[class="first group"]')[0]
            name = raw_name_location_designation.select('h2')[0].get_text().strip()
            school_name = list(map(lambda x: x.get_text().strip(),raw_name_location_designation.select('div > div[class="field-content"] > span')))
            department = raw_name_location_designation.select('div[class="field departments label-above"] > div.field-content')
            if department!=[]:
                department = department[0].get_text().strip()
            else:
                department = None
                
            phone_number = raw_personal_details_html_tag.select('div[class="field phone"]')[0].get_text().strip()
            email = raw_personal_details_html_tag.select('div[class="field email"]')[0].get_text().strip()
            
            self.all_extracted_data.append(Person_Data(name,school_name,phone_number,email,department))
    
    def __extract_data_from_paginattion(self, soup:Optional[BeautifulSoup]) -> None:
        
        dom_id = json.loads(soup.select('body > script:nth-child(3)')[0].get_text())["user"]["permissionsHash"]
        total_pages = soup.select('#node-32 > div > div.paragraph.staff.default > div > nav > ul > li.item.last > a')[0].get('href')[-1]
        
        for page_number in range(1,int(total_pages)+1):

            payload = f"view_name=staff_teaser&view_display_id=default&view_args=all%2F5&view_path=%2Fnode%2F32&view_base_path=&view_dom_id={dom_id}&pager_element=0&page={page_number}&_drupal_ajax=1&ajax_page_state%5Btheme%5D=wac&ajax_page_state%5Btheme_token%5D=&ajax_page_state%5Blibraries%5D=aeon%2Fbase%2Cblazy%2Fbio.ajax%2Ccore%2Fhtml5shiv%2Ccore%2Fpicturefill%2Cgoogle_analytics%2Fgoogle_analytics%2Cgtranslate%2Fjquery-slider%2Cmicon%2Fmicon%2Cparagraphs%2Fdrupal.paragraphs.unpublished%2Csystem%2Fbase%2Cux%2Fux.auto_submit%2Cux_form%2Fux_form.input%2Cux_header%2Fux_header%2Cux_offcanvas_menu%2Fux_offcanvas_menu%2Cviews%2Fviews.ajax%2Cviews%2Fviews.module%2Cwac%2Fbase"
     
            pagination_response = self.session.post("https://isd110.org/views/ajax?_wrapper_format=drupal_ajax", headers=pagination_headers, data=payload)
            
            json_pagination_response = json.loads(pagination_response.content)
            
            pagination_soup = BeautifulSoup(json_pagination_response[2]['data'], 'html.parser')
            
            self.__extract_fields(pagination_soup,"API")
    

    def __extract_data_from_html(self) -> Optional[BeautifulSoup]:
        
        starting_page_response = self.session.get('https://isd110.org/our-schools/laketown-elementary/staff-directory',headers=html_page_headers)

        if self.debug:
            self.__save_html_page(starting_page_response)
            
        soup = BeautifulSoup(starting_page_response.content, 'html.parser')
        
        self.__extract_fields(soup,"HTML")
        
        return soup
    
    def start(self) -> Optional[List[Person_Data]]:
        
        soup = self.__extract_data_from_html()
        self.__extract_data_from_paginattion(soup)

        return self.all_extracted_data

if __name__ == '__main__':
    print(Waconia_Scraper().start())
