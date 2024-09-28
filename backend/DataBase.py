import requests
from bs4 import BeautifulSoup
import psycopg2

# McDonald's 메뉴 페이지 URL
#url = "https://www.mcdonalds.co.kr/kor/menu/list.do"
url = "https://www.mcdelivery.co.kr/kr/browse/menu.html?daypartId=1&catId=13"

# 웹 페이지 가져오기
response = requests.get(url)

# BeautifulSoup를 사용하여 HTML 파싱
soup = BeautifulSoup(response.text, "html.parser")

# 메뉴 항목 찾기
#menu_items = soup.find_all("li")
menu_items = soup.find_all("div", class_="product-card product-card--standard")

# PostgreSQL 연결
conn = psycopg2.connect(
    dbname="kiosk",
    user="postgres",
    password="goldenglow290$",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

print(menu_items)

# 메뉴 항목 반복하여 데이터베이스에 저장
for item in menu_items:
    catId = item.get("data-productcatid")
    division = "side"

    if catId == "11":
        division = "burger"
    elif catId == "13":
        division = "side"
    elif catId == "14":
        division = "drink"
        
    name = item.find("h5", class_="product-title").text
    price = int(item.find("span", class_="starting-price").text.replace("₩ ", "").replace(",", ""))
    kcal_element = item.find("span", class_="text-default")
    if kcal_element:
        try:
            kcal = int(item.find("span", class_="text-default").text.split()[0])
        except (ValueError, IndexError):
            kcal = 0
    photourl = item.find("img", class_="img-block")['src']

    # 데이터베이스에 데이터 삽입
    cursor.execute("INSERT INTO product (p_division, p_name, p_price, p_kcal, p_photourl) VALUES (%s, %s, %s, %s, %s)",
                   (division, name, price, kcal, photourl))

# 변경사항 저장 및 연결 종료
conn.commit()
conn.close()

print("데이터베이스에 McDonald's 메뉴가 성공적으로 저장되었습니다.")
