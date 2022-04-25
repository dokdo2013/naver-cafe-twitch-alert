import dotenv
import naver_token
import os
import urllib.request
from urllib.parse import urlencode
import time
import db


def write(subject, content):
    try_count = 0

    while try_count < 2:
        try:
            dotenv.load_dotenv()
            access_token = os.getenv('ACCESS_TOKEN')
            access_token = access_token.replace("'", "")  # .env 저장하는 과정에서 따옴표 추가되는 문제 보정
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


def create_content(database, data):
    res = db.get_info(database, data[0])
    subject = f"[{res['streamer_name_ko']}] {res['streamer_name_ko']} 뱅온!!"
    content = f"<p>얼른 방송 보러 오세요!!</p><a href='https://twitch.tv/{res['streamer_name']}'>https://twitch.tv/{res['streamer_name']}</a>"
    return [subject, content]
