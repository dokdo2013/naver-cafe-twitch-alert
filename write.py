import dotenv
import naver_token
import os
import urllib.request
from urllib.parse import urlencode
import time


def write(subject, content):
    try_count = 0

    while try_count < 2:
        try:
            dotenv.load_dotenv()
            access_token = os.getenv('ACCESS_TOKEN')
            header = 'Bearer ' + access_token
            club_id = os.getenv('CLUB_ID')
            menu_id = os.getenv('MENU_ID')
            url = "https://openapi.naver.com/v1/cafe/" + club_id + "/menu/" + menu_id + "/articles"

            subject = urllib.parse.quote(subject)
            content = urllib.parse.quote(content)

            data = urlencode({'subject': subject, 'content': content}).encode()
            request = urllib.request.Request(url, data=data)
            request.add_header('Authorization', header)
            response = urllib.request.urlopen(request)
            rescode = response.getcode()
            print(rescode)
            break
        except:
            naver_token.refresh_token()
            try_count += 1
            time.sleep(5)


