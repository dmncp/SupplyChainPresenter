import json
import requests

base_url = 'https://openx.com'
error_4xx_msg = 'I cannot find your data.'
error_5xx_msg = 'Unfortunately, I cannot get a connection at this point. Please try again in a moment.'


def check_errors(response, *args):
    print(response.url + " => " + str(response.status_code))
    if 400 <= response.status_code < 500:
        return error_4xx_msg if not args else args[0]
    elif 500 <= response.status_code < 600:
        return error_5xx_msg
    elif 200 <= response.status_code < 300:
        response_after_redirect = requests.get(response.url + '/sellers.json')

        '''Some sellers' pages redirect to other pages so we have to make the request again eg. 33across.com'''
        return json.loads(response_after_redirect.content)['sellers']


def get_sellers_list():
    response = requests.get(base_url)
    return check_errors(response)


def get_sellers_of_seller(domain):
    try:
        response = requests.get('https://' + domain + '/sellers.json')
        return check_errors(response)
    except requests.exceptions.RequestException as e:
        print("ERROR: ")
