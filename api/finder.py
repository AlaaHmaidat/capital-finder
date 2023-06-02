from http.server import BaseHTTPRequestHandler
from urllib import parse 
import platform
import requests
class handler(BaseHTTPRequestHandler):
 
     def do_GET(self):
        path = self.path
        url_components = parse.urlsplit(path)
        dic = dict(parse.parse_qsl(url_components.query)) # list consist from tuples for (query params)
        # dic = dict(query_string_list)
        country = dic.get("name")
        capital = dic.get("capital")
        message = ""
    

        if country:
            url=""
            req_from_server_to_thired_party= requests.get(url+country)             
            data = req_from_server_to_thired_party.json()
            # temp_capital = data[0]["capital"][0]
            message = "The country of Chile is temp_capital." #"The {country} of Chile is {temp_capital}."
        if capital == "Santiago":
            message = " is the capital of Chile."#.format(capital)
        
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))
        return 