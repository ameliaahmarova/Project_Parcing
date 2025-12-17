import re
from bs4 import BeautifulSoup

def load_html(path="data/torgi.html"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def parse_price(price_str: str) -> int:
    # Удаляем "руб." и пробелы
    price_str = price_str.replace("руб.", "").strip()
    
    # Заменяем пробелы (разделители тысяч) на пустую строку
    price_str = price_str.replace(" ", "")
    
    # Убираем все нецифровые символы, кроме точки
    cleaned = ""
    for char in price_str:
        if char.isdigit() or char == ".":
            cleaned += char
    
    if cleaned:
        # Преобразуем в float и округляем до рублей
        return int(float(cleaned))
    
    return 0

def parse_lots(html: str):
    soup = BeautifulSoup(html, "html.parser")

    # все строки таблицы (lots)
    rows = soup.find_all("tr")

    lots = []

    for row in rows:
        cols = row.find_all("td")

        # строки лотов всегда содержат >= 6 столбцов
        if len(cols) < 6:
            continue

        try:
            code = cols[0].text.strip()
            title = cols[1].text.strip()
            price_str = cols[5].text.strip()
            price = parse_price(price_str)

            lots.append({
                "code": code,
                "title": title,
                "price": price,
                # ссылки в HTML нет, поэтому оставляем пустой
                "link": None
            })
        except:
            continue

    return lots

def filter_by_price(lots, min_price=None, max_price=None):
    result = []
    for lot in lots:
        price = lot["price"]
        
        if min_price is not None and price < min_price:
            continue
        if max_price is not None and price > max_price:
            continue
            
        result.append(lot)
    return result

def main():
    html = load_html()
    lots = parse_lots(html)

    lots.sort(key=lambda x: x["price"], reverse=True)

    print("Введите минимальную цену (или Enter): ")
    min_p = input().strip()
    min_p = int(min_p) if min_p else None

    print("Введите максимальную цену (или Enter): ")
    max_p = input().strip()
    max_p = int(max_p) if max_p else None

    filtered = filter_by_price(lots, min_p, max_p)

    print("\nПодходящие лоты:\n")

    if not filtered:
        print("Нет лотов, подходящих под ваш диапазон цен.")
        return

    for lot in filtered:
        print(f"{lot['price']:,} руб. — {lot['title']} (код {lot['code']})".replace(",", " "))
        print()

if __name__ == "__main__":
    main()
