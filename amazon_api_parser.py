import requests
import hmac, hashlib

from base64 import b64encode
from time import strftime, gmtime, sleep
from urllib import urlencode


from collections import OrderedDict


class AmazonAPI(object):

    def __init__(self, api_config):
        self.api_config = api_config
        self.endpoint = self.api_config.get("endpoint", "")

    def generate_amazon_url(self, params):
        uri = "/onca/xml"
        url = "http://%s%s" % (self.endpoint, uri)

        params = self.do_auth(params, uri)

        data = urlencode(params)
        data = data.replace('+', '%20')
        api_full_url = url + "?" + data

        return api_full_url

    def do_auth(self, params, uri):
        associate_tag = self.api_config.get("associate_tag", "")
        subscription_id = self.api_config.get("subscription_id", "")
        secret_key = self.api_config.get("secret_key", "")
        # api_version = "2013-08-01"

        params['AssociateTag'] = associate_tag
        params['AWSAccessKeyId'] = subscription_id
        # params['Version'] = api_version
        params["Timestamp"] = strftime("%Y-%m-%dT%H:%M:%S.000Z", gmtime())

        for k, v in params.iteritems():
            if isinstance(v, unicode):
                params[k] = v.encode('utf-8')

        params = OrderedDict(sorted(params.items(), key=lambda t: t[0]))
        canonical_query_string = urlencode(params, doseq=True)
        canonical_query_string = canonical_query_string.replace('+', '%20')

        string_to_sign = "GET\n%s\n%s\n%s" % (self.endpoint, uri, canonical_query_string)
        _hash = hmac.new(secret_key, string_to_sign, hashlib.sha256)
        signature = b64encode(_hash.digest())
        params['Signature'] = signature
        return params

    def item_search_key_words(self, node_id, key_words=None, brand=None, page=1):
        params = {
            "Service": "AWSECommerceService",
            "Operation": "ItemSearch",
            "BrowseNode": node_id,
            "ResponseGroup": ','.join(['ItemAttributes', 'Reviews', 'BrowseNodes', 'Images', 'ItemIds', 'SalesRank']),
            "SearchIndex": 'Electronics',
            "Sort": 'salesrank',
            "ItemPage": page,
            # always search for available products
            "Availability": 'Available'
        }
        if brand:
            params['Brand'] = brand

        if key_words:
            params['Keywords'] = key_words

        url = self.generate_amazon_url(params)
        print(url)
        return url

    def lookup_product_by_asin(self, asin):
        params = {
            "Service": "AWSECommerceService",
            "Operation": "ItemLookup",
            "ResponseGroup": ','.join(['ItemAttributes', 'Reviews', 'BrowseNodes', 'Images', 'ItemIds', 'SalesRank']),
            "Sort": 'salesrank',
            "Condition": "All",
            "IdType": "ASIN",
            "ItemId": asin
        }

        url = self.generate_amazon_url(params)
        print(url)
        return url

