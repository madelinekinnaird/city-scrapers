# -*- coding: utf-8 -*-
from datetime import time

from dateutil.parser import parse

from city_scrapers.constants import BOARD
from city_scrapers.spider import Spider


class DetWreckingExaminersSpider(Spider):
    name = 'det_wrecking_examiners'
    agency_name = 'Detroit Wrecking Contractors Board of Examiners'
    timezone = 'America/Detroit'
    allowed_domains = ['www.detroitmi.gov']
    start_urls = [
        'https://www.detroitmi.gov/government/boards/board-wrecking-contractors-examiners/board-wrecking-contractors-meetings'  # noqa
    ]

    def parse(self, response):
        """
        `parse` should always `yield` a dict that follows the Event Schema
        <https://city-bureau.github.io/city-scrapers/06_event_schema.html>.

        Change the `_parse_id`, `_parse_name`, etc methods to fit your scraping
        needs.
        """
        location = {
            'neighborhood': '',
            'name': 'Coleman A. Young Municipal Center, Room 412',
            'address': '2 Woodward Avenue, Detroit, MI 48226'
        }
        meeting_name = 'Board of Wrecking Contractors Examiners'

        for item in response.xpath(
            '//div[contains(@class, "view-header")]//p[strong[contains(string(), '
            '"The Board of Wrecking Contractors")]]/following-sibling::p/text()'
        ).extract():

            data = {
                '_type': 'event',
                'name': meeting_name,
                'event_description': '',
                'classification': BOARD,
                'start': self._parse_start(item),
                'end': {
                    'date': None,
                    'time': None,
                    'note': ''
                },
                'all_day': False,
                'location': location,
                'documents': [],
                'sources': [{
                    'url': response.url,
                    'note': ''
                }],
            }

            data['status'] = self._generate_status(data)
            data['id'] = self._generate_id(data)

            yield data

    def _parse_start(self, item):
        """
        Parse start date and time.
        """
        try:
            meeting_date = parse(item)
            return {'date': meeting_date.date(), 'time': time(13, 00), 'note': ''}
        except ValueError:
            return {'date': None, 'time': None, 'note': item}
