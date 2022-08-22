import requests

def send(to):
    message = "레븐 뱅온알림봇 동작중! 오늘 방송도 화이팅입니다 :)"
    url = f"https://leaven-tmi.haenu.xyz/send?to={to}&message={message}"
    requests.get(url)