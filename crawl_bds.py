from typing import List
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import time

import config

class RealEstateCrawler:
    def __init__(self, type_realestate: str) -> None:
        self.type_realestate: str = type_realestate
        self.df_res: pd.DataFrame = pd.DataFrame()

    def crawl_number_pages(self) -> int:
        self.options = uc.ChromeOptions()
        self.options.headless = False
        self.browser = uc.Chrome(use_subprocess=True, options=self.options)
        self.browser.get(f"{config.url1}/{self.type_realestate}")

        pages = self.browser.find_elements(By.CLASS_NAME, "re__pagination-group")
        res_pages = [page.text.split("\n") for page in pages]
        max_page = max(map(int, res_pages[0]))

        self.browser.quit()

        return max_page

    def crawl_page(self, page_number: int) -> pd.DataFrame:
        self.options = uc.ChromeOptions()
        self.options.headless = False
        self.browser = uc.Chrome(use_subprocess=True, options=self.options)
        self.browser.get(f"{config.url1}/{self.type_realestate}/p{page_number}")

        titles = self.browser.find_elements(By.CLASS_NAME, "pr-title.js__card-title")
        prices = self.browser.find_elements(By.CLASS_NAME, "re__card-config-price.js__card-config-item")
        areas = self.browser.find_elements(By.CLASS_NAME, "re__card-config-area.js__card-config-item")
        locations = self.browser.find_elements(By.CLASS_NAME, "re__card-location")

        res_title = [title.text for title in titles]
        res_price = [price.text for price in prices]
        res_area = [area.text for area in areas]
        res_location = [location.text for location in locations]

        max_len = max(len(res_title), len(res_price), len(res_area), len(res_location))
        if len(res_title) < max_len:
            res_title += [''] * (max_len - len(res_title))
        if len(res_price) < max_len:
            res_price += [''] * (max_len - len(res_price))
        if len(res_area) < max_len:
            res_area += [''] * (max_len - len(res_area))
        if len(res_location) < max_len:
            res_location += [''] * (max_len - len(res_location))

        df: pd.DataFrame = pd.DataFrame({
            'Title': res_title,
            'Price': res_price,
            'Area': res_area,
            'Location': res_location,
            'type': self.type_realestate
        })

        self.browser.quit()

        return df

    def crawl_and_save_data(self, start_page: int, end_page: int) -> None:
        number_pages = self.crawl_number_pages()
        print(f"number_pages of {self.type_realestate} is", number_pages)

        for i in range(start_page, end_page):
            start_time = time.time()
            print(f"Progress to page {i+1}")
            df = self.crawl_page(i+1)
            self.df_res = pd.concat([self.df_res, df], ignore_index=True)
            end_time = time.time()
            print(f"1 iteration takes {end_time-start_time}")
            if (i+1) % 10 == 0:
                self.df_res.to_csv(f"data_bds/{self.type_realestate}_order_{i+1}.csv", index=False, encoding='utf-8-sig')
                self.df_res = pd.DataFrame()

if __name__ == '__main__':
    types_realestate: List[str] = ["cho-thue-nha-tro-phong-tro"]

    for type_realestate in types_realestate:
        real_estate_crawler = RealEstateCrawler(type_realestate)
        real_estate_crawler.crawl_and_save_data(0, 1000)  # Thay đổi khoảng trang bạn muốn crawl ở đây
