
URL_SEARCH = "https://api-cn.decathlon.com.cn/facade_offering/api/v1/search_tips?keyword={}"
URL_GET_INFO = "https://api-cn.decathlon.com.cn/facade_offering/api/v1/product_components?dsm_code={}"


HEADERS = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJCa0VhY2c1SjRneEV4SjNOYUU2b0Z5c1o5NkFROFFDYnRuM2RaM0VBRSIsInNvY2lhbF9pZCI6IjUzZDc5YTYwLWViZjItNGJhNy05NThiLTFkNGMwNTIwZGQ0MSIsImNhcmRfbnVtYmVyIjpudWxsLCJvcmlnaW4iOiJ1c2VyIiwic29jaWFsX21hc3Rlcl9pZCI6bnVsbCwiaXNzIjoiZmFjYWRlLWFwaS5ka3RhcHAuY2xvdWQiLCJtb2JpbGUiOm51bGwsImV4cCI6MTczMTYyMTkzOSwiY2xpZW50X25hbWUiOiJEQ04iLCJjbGllbnRfaWQiOiJCa0VhY2c1SjRneEV4SjNOYUU2b0Z5c1o5NkFROFFDYnRuM2RaM0VBRSIsInBlcnNvbl9pZCI6bnVsbH0.X_EXWNM1SM-dZRHnGMlPyv-RcjQ81ABETjIpM2PX6yTz_LCmlrNheAwpMVyv-NcHCK3jQ6BEbOtR3yZUjFp6Al2jzaqVEfIiRfbYQIGMPXupeNT9qDMh5SVcn6CTcX5S-FygQ17haZcVoNSUqwCLW9XUrctH7C6FcvyAPcHmywoSd6ir6aWWPsuL6WRjTfbrK2TOjsW0_U0WqRdVwHQj4GW_hriI6i0QrQ6yBQV3nRJ7FB8kSG6S14M-0pTY4GXYRCtUpducmyQk18ddTcHiKAb2SuDcMJoTE2zKTqybqyKKEXvY2obl7skhVRYoQfBeGykJi7XsWj3fgl-1bwJPSQ',
    'cookie': 'rxVisitor=17192145589716K710N4FAADCAVGFS65ELOO2VI1DU3E2; _ga=GA1.1.1843479477.1719404059; didomi_token=eyJ1c2VyX2lkIjoiMTkwNTQ3N2QtODhmNC02ZjIyLWJlZGMtNTg3YWFjOWY1Mzk1IiwiY3JlYXRlZCI6IjIwMjQtMDYtMjZUMTI6MTQ6MTguNzY3WiIsInVwZGF0ZWQiOiIyMDI0LTA2LTI2VDEyOjE0OjE4Ljc2OFoiLCJ2ZXJzaW9uIjpudWxsfQ==; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22190492c5b032c3-00944324976c3ab8-26001f51-2073600-190492c5b04fa3%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkwNDkyYzViMDMyYzMtMDA5NDQzMjQ5NzZjM2FiOC0yNjAwMWY1MS0yMDczNjAwLTE5MDQ5MmM1YjA0ZmEzIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22190492c5b032c3-00944324976c3ab8-26001f51-2073600-190492c5b04fa3%22%7D; _ga_0ME75SMY4S=GS1.1.1729152089.2.1.1729152105.44.0.0; dtCookie=v_4_srv_1_sn_BE065CB209D8857CFE6148F7F6CDD719_perc_100000_ol_0_mul_1_app-3A6435483c1eab6ca4_0; token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJCa0VhY2c1SjRneEV4SjNOYUU2b0Z5c1o5NkFROFFDYnRuM2RaM0VBRSIsInNvY2lhbF9pZCI6IjcwMTNjNGQ0LTA1OWQtNDEwZC1iMDRkLTEzMWFmY2MyMTEzZSIsImNhcmRfbnVtYmVyIjpudWxsLCJvcmlnaW4iOiJ1c2VyIiwic29jaWFsX21hc3Rlcl9pZCI6bnVsbCwiaXNzIjoiZmFjYWRlLWFwaS5ka3RhcHAuY2xvdWQiLCJtb2JpbGUiOm51bGwsImV4cCI6MTcyOTUxMTUyMSwiY2xpZW50X25hbWUiOiJEQ04iLCJjbGllbnRfaWQiOiJCa0VhY2c1SjRneEV4SjNOYUU2b0Z5c1o5NkFROFFDYnRuM2RaM0VBRSIsInBlcnNvbl9pZCI6bnVsbH0.Hi2PX1JAxyXlrybJ2Ut6LIT-ZD-saH9G5fKBMPkwf48wqhPIb853UZLegJpqWGhkAxUvx4pNja9kqWtusQXJZBl227qFAJzlfFKA2Z6STLzXHzOF951hrxiz0iKSwAecELNLRpEOOmYfddOyLYOcSKpbFL-WQIMI0upRXdnOreL5WHG4NFNallvqx3YpIONVD5_oEspDuxXh93o8JGDilakrU3UrhTVMOv4Ek7ZNk50djuq87eXDPsOIsWbNU2261FlGUHjbe-q9FI1pNUIR8_2TgarqcrTgGWKQbwea2GfEyqjEpREBLSVbrJfh0mOMMkq_P88nu-rBWqwNeT7W8A',
    'origin': 'https://www.decathlon.com.cn',
    'priority': 'u=1, i',
    'referer': 'https://www.decathlon.com.cn/',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
    }