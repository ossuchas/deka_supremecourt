# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy import Request
from scrapy.http import FormRequest
from deka_supremecourt.items import DekaSupremecourtItem
from bs4 import BeautifulSoup


def law_tag(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    val = []
    for tag in soup.find_all('li'):
        text = tag.text.strip()
        text = text.replace('\n\n', '')
        val.append(text.strip())

    law = ", ".join(val)
    law = law.replace('\n', '')
    return law


class DekaSpider(Spider):
    name = 'deka'
    allowed_domains = ['deka.supremecourt.or.th']
    start_urls = ['http://deka.supremecourt.or.th/search/']

    def parse(self, response):
        data = {'show_item_remark': '0',
                'show_item_primartcourt_deka_no': '0',
                'show_item_deka_black_no': '0',
                'show_item_department': '0',
                'show_item_primarycourt': '1',
                'show_item_judge': '1',
                'show_item_source': '1',
                'show_item_long_text': '0',
                'show_item_short_text': '1',
                'show_item_law': '1',
                'show_item_litigant': '1',
                'show_result_state': '1',
                'search_form_type': 'basic',
                'search_type': '1',
                'start': 'true',
                'search_doctype': '1',
                'search_word': '',
                'search_deka_no_ref': '',
                'search_deka_no': '',
                'search_deka_start_year': '2561',
                'search_deka_end_year': '2561'}

        return FormRequest(url=self.start_urls[0], formdata=data, callback=self.parse_deka)

    def parse_deka(self, response):
        dekaItem = DekaSupremecourtItem()
        results = response.xpath('//*[@class="clear result"]')
        for result in results:
            title = result.xpath('.//*[@class="css-label med elegant content-title"]/text()').extract_first()
            contents = result.xpath('.//*[@class="item_short_text content-detail"]/p/text()').extract()
            content = "".join(contents)

            plaintiff = result.xpath('.//*[@class="item_litigant content-option"]/ul/li[1]/text()').extract_first()
            defendent = result.xpath('.//*[@class="item_litigant content-option"]/ul/li[2]/text()').extract_first()

            quorum1 = result.xpath('.//*[@class="item_judge content-option"]/ul/li[1]/text()').extract_first()
            quorum2 = result.xpath('.//*[@class="item_judge content-option"]/ul/li[2]/text()').extract_first()
            quorum3 = result.xpath('.//*[@class="item_judge content-option"]/ul/li[3]/text()').extract_first()

            federal_court = result.xpath('.//*[@class="item_primarycourt content-option"]/ul/li[1]/text()').extract_first()
            court_of_appeal = result.xpath('.//*[@class="item_primarycourt content-option"]/ul/li[2]/text()').extract_first()

            law_html_doc = result.xpath('.//*[@class="item_law content-detail"]/ul').extract()
            law = law_tag(law_html_doc[0])

            dekaItem['title'] = title.strip()
            dekaItem['content'] = content
            dekaItem['plaintiff'] = plaintiff.strip()
            dekaItem['defendent'] = defendent.strip()
            dekaItem['quorum1'] = quorum1.strip()
            dekaItem['quorum2'] = quorum2.strip()
            dekaItem['quorum3'] = quorum3.strip()
            dekaItem['federal_court'] = federal_court
            dekaItem['court_of_appeal'] = court_of_appeal
            dekaItem['law'] = law

            yield dekaItem

            # yield {
            #     'title': title,
            #     'content': content
            # }

        # contents = result.xpath('.//*[@class="modal modal-wide fade"]')
        # contents.xpath('.//*[@class="modal-title"]/text()').extract_first()
        # contents.xpath('.//*[@class="width-max end modal-header"]/h4/text()').extract_first()
        # contents.xpath('.//*[@class="item show-display-left print_item_deka_no"]/label/text()').extract_first()
        # contents.xpath('.//*[@class="item show-display-right print_item_litigant "]/ul/li').extract()
        abs_next_page_url = response.xpath('.//a[span[@class="glyphicon glyphicon-chevron-right"]]/@href').extract_first()

        if abs_next_page_url is not None:
            yield Request(abs_next_page_url, callback=self.parse_deka)

