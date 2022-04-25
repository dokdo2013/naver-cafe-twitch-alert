import requests
import base64
import dotenv
import os


# 최초 발급 시에만 필요
def get_token():
    dotenv.load_dotenv()

    redirect_uri=os.getenv('REDIRECT_URI')
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    state = 'SUCCESS'

    code = os.getenv('USER_CODE')
    access_token = ''

    if not code:
        url = f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&state={state}"
        print(url)
        return False

    if not access_token:
        clientConnect = client_id + ":" + client_secret
        clidst_base64 = base64.b64encode(bytes(clientConnect, "utf8")).decode()

        url = f'https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&code={code}&state={state}'
        r = requests.get(url,headers={"Authorization": "Basic "+clidst_base64})
        print(r.text)


# Refresh Token으로 Access Token 발급
def refresh_token():
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)

    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    refresh_token = os.getenv('REFRESH_TOKEN')

    url = f'https://nid.naver.com/oauth2.0/token?grant_type=refresh_token&client_id={client_id}&client_secret={client_secret}&refresh_token={refresh_token}'
    r = requests.get(url)
    print(r.text)
    os.environ["ACCESS_TOKEN"] = r.json()['access_token']
    dotenv.set_key(dotenv_file, 'ACCESS_TOKEN', os.environ["ACCESS_TOKEN"])


