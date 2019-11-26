from amazon_api_parser import AmazonAPI


api_config = {}
api_config["associate_tag"] = "your_tag"
api_config["subscription_id"] = "your_subscription_id"
api_config["endpoint"] = "webservices.amazon.com" # Amazon US 
api_config["secret_key"] = 'your_key'

amazon_api = AmazonAPI(api_config)
# node_id is the BrowseNode id defined by amazon
amazon_api.item_search_key_words(node_id="your_browse_node_id", key_words="iphone")
# asin = Amazon Standard Identification Number
amazon_api.lookup_product_by_asin(asin="B07ZPP48B4")
