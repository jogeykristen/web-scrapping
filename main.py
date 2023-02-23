import time

import requests
from bs4 import BeautifulSoup

#

# import requests
import urllib.request
from bs4 import BeautifulSoup
# from urllib import urlopen
import re
from urllib.request import Request, urlopen
import uvicorn

import requests
from fastapi import FastAPI
from googletrans import Translator
from fastapi.responses import HTMLResponse
import html
import traceback

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def read_root():
    try:
        translator = Translator()
        print("inside conversion")
        my_session = requests.session()
        for_cookies = my_session.get("https://www.classcentral.com/")
        cookies = for_cookies.cookies
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36'}
        my_url = 'https://www.classcentral.com/'

        response = requests.get(my_url, headers=headers, cookies=cookies)
        print("got the response")
        soup = BeautifulSoup(response.content, 'html.parser')
        print("parsed the response")

        text_to_translate = soup.get_text(separator=' ')

        translated_text = ''
        for string in text_to_translate.split('\n'):
            #since google translate api can give timeout we are giving timing request as 1 req per second
            time.sleep(50)
            if string.strip() != '':
                translated_string = translator.translate(string, dest='hi').text
                translated_text += translated_string + '\n'

        soup.body.replace_with(translated_text)
        html = str(soup)



    except Exception as e:
        print(e)
        traceback.print_exc()

    return html


if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, host="0.0.0.0", reload=True)
