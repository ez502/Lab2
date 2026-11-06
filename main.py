import csv
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from xml.dom import minidom


FOLDER = Path(__file__).resolve().parent


def read_books(path):
    with open(path, encoding="cp1251", newline="") as file:
        return list(csv.DictReader(file, delimiter=";"))


def search_books(books, author):
    author = author.strip().casefold()
    if not author:
        return []
    result = []
    for book in books:
        full_name = book["Автор"] + " " + book["Автор (ФИО)"]
        price = Decimal(book["Цена поступления"].replace(",", "."))
        if author in full_name.casefold() and price <= Decimal("150"):
            result.append(book)
    return result


def save_references(books, path):
    with open(path, "w", encoding="utf-8") as file:
        for number, book in enumerate(books[:20], start=1):
            year = datetime.strptime(book["Дата поступления"], "%d.%m.%Y %H:%M").year
            file.write(f'{number}. {book["Автор"]}. {book["Название"]} - {year}\n')


def read_currencies(path):
    document = minidom.parse(str(path))
    currencies = {}
    for currency in document.getElementsByTagName("Valute"):
        name = currency.getElementsByTagName("Name")[0].firstChild.data
        value = currency.getElementsByTagName("Value")[0].firstChild.data
        currencies[name] = float(value.replace(",", "."))
    return currencies



def main():
    books = read_books(FOLDER / "books.csv")
    count = sum(len(book["Название"]) > 30 for book in books)
    print("Количество названий длиннее 30 символов:", count)

    author = input("Введите фамилию или часть имени автора: ")
    found = search_books(books, author)
    print("Найдено записей с ценой до 150 рублей включительно:", len(found))
    for book in found:
        print(f'{book["Автор"]}. {book["Название"]} — {book["Цена поступления"]} руб.')

    save_references(books, FOLDER / "references.txt")
    print("20 библиографических ссылок сохранены в references.txt")

    currencies = read_currencies(FOLDER / "currency.xml")
    print("\nСловарь валют Name -> Value:")
    print(currencies)



if __name__ == "__main__":
    main()
