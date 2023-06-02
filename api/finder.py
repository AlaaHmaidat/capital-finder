from http.server import BaseHTTPRequestHandler
from urllib import parse
import requests


class Handler(BaseHTTPRequestHandler):
    """
    A custom HTTP request handler that retrieves country and capital information from a REST API.

    The handler supports two types of queries:
    - Query by country: Provide the 'country' query parameter to get the capital of a specific country.
    - Query by capital: Provide the 'capital' query parameter to get the country corresponding to a capital.

    The REST API used is 'https://restcountries.com/v3.1/'.

    Example Usage:
    - http://localhost:8000/?country=Jordan
    - http://localhost:8000/?capital=Amman
    """

    def do_GET(self):
        """
        Handle GET requests.

        Retrieves the query parameters from the URL and retrieves country/capital information from the REST API.
        Constructs the response message based on the query results and sends it back to the client.
        """

        url = self.path
        url_components = parse.urlsplit(url)
        query_dict = dict(parse.parse_qsl(url_components.query))

        country = query_dict.get('country')
        capital = query_dict.get('capital')
        message = ""

        if country:
            country_url = f'https://restcountries.com/v3.1/name/{country}'
            response = requests.get(country_url)
            if response.status_code == 200:
                data = response.json()
                try:
                    capital_name = data[0]['capital'][0]
                    message = f"The capital of {country} is {capital_name}"
                except (KeyError, IndexError):
                    message = 'Please enter a valid country or capital'
            else:
                message = 'Error: Unable to retrieve country data'
        elif capital:
            capital_url = f'https://restcountries.com/v3.1/capital/{capital}'
            response = requests.get(capital_url)
            if response.status_code == 200:
                data = response.json()
                try:
                    country_name = data[0]['name']['common']
                    message = f"{capital} is the capital of {country_name}"
                except (KeyError, IndexError):
                    message = 'Please enter a valid country or capital'
            else:
                message = 'Error: Unable to retrieve capital data'

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))
        return
