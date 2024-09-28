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
  dbname="postgres",
  user="postgres",
  host="localhost",
  password="tlswo3850",
  port="5432"
)
cursor = conn.cursor()

print(menu_items)

for item in menu_items:
    catId = item.get("data-productcatid")
    division = "side"

    name = item.find("h5", class_="product-title").text
    price = int(item.find("span", class_="starting-price").text.replace("₩ ", "").replace(",", ""))
    
    # kcal 값을 찾기 전에 해당 요소가 존재하는지 확인
    kcal_span = item.find("span", class_="text-default")
    if kcal_span:  # kcal_span이 None이 아니면
        try:
            kcal = int(kcal_span.text.split()[0])
        except (ValueError, IndexError):
            kcal = 0
    else:  # kcal_span이 None이면
        kcal = 0

    photourl = item.find("img", class_="img-block")['src']

    # 데이터베이스에 데이터 삽입
    cursor.execute("INSERT INTO product (p_division, p_name, p_price, p_kcal, p_photourl) VALUES (%s, %s, %s, %s, %s)",
                   (division, name, price, kcal, photourl))

# 변경사항 저장 및 연결 종료
conn.commit()
conn.close()

print("데이터베이스에 McDonald's 메뉴가 성공적으로 저장되었습니다.")