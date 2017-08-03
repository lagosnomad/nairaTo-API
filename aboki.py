#!/usr/bin/env python
from __future__ import absolute_import, print_function
from json import dumps
from sys import exit

from bs4 import BeautifulSoup
from docopt import docopt
from requests import get, post, exceptions
from pkg_resources import get_distribution

# Globals
API_URI = 'https://www.abokifx.com'
VERSION = 'aboki %s' % get_distribution("aboki").version


class Aboki:
    def __init__(self):
        self.currencies = ('usd', 'gbp', 'eur')
        self.types = ['cbn', 'movement', 'lagos_previous', 'moneygram', 'westernunion', 'otherparallel']
        self.quotes = 'Quotes:\t*morning\t**midday\t***evening'
        self.note = '**NOTE**: Buy / Sell => 90 / 100\n'

    def make_request(self, path, params={}, data={}, method='GET'):
        """Make the specified API request, and return the HTML data, or quit
        with an error.
        """

        try:
            if method.lower() == 'post':
                resp = post('%s/%s' % (API_URI, path), params=params, data=dumps(data),
                            headers={'Content-Type': 'application/json'})
            else:
                resp = get('%s/%s' % (API_URI, path), params=params)

            if resp.status_code != 200:
                print('Error connecting. Please try again.')
                print('If the problem persists, please email r@akinjide.me.')
                exit(1)
            return resp.text

        except exceptions.RequestException, e:
            print('Error connecting. Please check network and try again.')
            print('If the problem persists, please email r@akinjide.me.')
            exit(1)

    def parse(self, content):
        soup = BeautifulSoup(content, "html5lib")
        records = soup.select("body .lagos-market-rates table tbody > tr")
        data = [[str(j) for j in record.stripped_strings
                 if str(j) not in ('NGN', 'Buy / Sell')] for record in records]
        return {'title': str(soup.title.string), 'data': data}

    def get_current_rates(self):
        """Return the current exchange rate for USD, GBP, EUR."""

        resp = self.make_request('')
        rjson = self.parse(resp)
        rates = ' / '.join(rjson['data'][0][1:]).split(' / ')
        return dict(zip(self.currencies, [float(rate) for rate in rates if '*' not in rate]))
