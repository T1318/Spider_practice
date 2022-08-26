import requests
import re


heards = {
    'Cookies':'_octo=GH1.1.930811588.1657108512; _device_id=3bd17372cddc6fd6b4623a110072c018; user_session=02IXyQ3bBI_EtV2e12AFuGdqhThpTdf0nqwyxyJuTbTTOfkX; __Host-user_session_same_site=02IXyQ3bBI_EtV2e12AFuGdqhThpTdf0nqwyxyJuTbTTOfkX; logged_in=yes; dotcom_user=T1318; color_mode={"color_mode":"auto","light_theme":{"name":"light","color_mode":"light"},"dark_theme":{"name":"dark","color_mode":"dark"}}; has_recent_activity=1; _gh_sess=ZeIvjOSQo0BPiYtFOv4bm5uFx2sklZGBORY3FlZ9C1PwSJ6IAwox8+IZ7rHZCU3fJaAUCQJHoKlXlx/hY1IQLHtyAJIG8vYvOprN3+Y9VsYeYLSkZFatVyUmZWgAcVbze33BSPP5d/1hTHQg9jDpW6kZ5L/ZhTfSS+0X20OJNeGN8shr3olRV+buZn4XZp2u--19HV7Fxxpo4ccJ2l--HRHFtamflUFeTcfBJ9KONw==', 
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}
url = 'https://github.com/'
# pat = '<h2.*?>(.*?)</h2>'
# pattern = re.compile(pat, re.S)
r = requests.get(url, headers=heards)
# title = re.findall(pattern, r.text)
# print(title)
print(r.text)
