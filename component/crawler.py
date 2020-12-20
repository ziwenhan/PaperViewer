from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import sys
sys.path.append(os.path.normpath(f'{os.path.dirname(os.path.abspath(__file__))}/..'))
from typing import List, Dict, Union
import requests
import json


class BaseCrawler:
    def __init__(self):
        self.use_ip = ''

    @staticmethod
    def api_get(url: str, payload: Dict) -> Dict:
        ret = requests.get(url=url, params=payload)
        content = json.loads(ret.content)
        return content


class OpenReviewCrawler(BaseCrawler):
    def __init__(self):
        super(OpenReviewCrawler, self).__init__()
        self.content = ''
        self.scores = []
        self.confidence = []
        self.reviews = []

    def get_reviews(self, paper_uid: str) -> Dict:
        # url = 'https://ope?nreview.net/forum?'
        review_url = 'https://api.openreview.net/notes?'
        payload = {'forum': paper_uid}
        self.content = OpenReviewCrawler.api_get(review_url, payload)
        self.content = self.content['notes']
        return self.content

    def get_scores(self):
        for review in self.content:
            if 'AnonReviewer' in review['signatures'][0]:
                self.reviews.append(review['content'])
                self.scores.append(int(review['content']['rating'].split(':')[0]))
                self.confidence.append(int(review['content']['confidence'].split(':')[0]))
        return self.scores


# if __name__ == '__main__':
#     opc = OpenReviewCrawler()
#     opc.get_reviews('E3UZoJKHxuk')
#     opc.get_scores()
#     print(opc.scores)
#     print(opc.confidence)
