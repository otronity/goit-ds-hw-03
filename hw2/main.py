import requests
from bs4 import BeautifulSoup
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
# from model import Book, Base
import json
from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi


# URL сайту для скрапінгу
base_url = 'http://quotes.toscrape.com'

client = MongoClient(
    "mongodb+srv://otronity:Podumai_1135@cluster0.a5df2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    server_api=ServerApi('1')
)

db = client.site


# Функція для отримання даних про автора
def get_author_info(author_url):
    response = requests.get(base_url + author_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Збираємо дані про автора
    fullname = soup.find('h3', class_='author-title').text.strip()
    born_date = soup.find('span', class_='author-born-date').text.strip()
    born_location = soup.find('span', class_='author-born-location').text.strip()
    description = soup.find('div', class_='author-description').text.strip()

    return {
        'fullname': fullname,
        'born_date': born_date,
        'born_location': born_location,
        'description': description
    }


def parse_data():
    quotes_ = []
    authors = {} 
    page = 1
    while True and page < 3:
        print(f"Parse data page {page}...")        
        url = f"{base_url}/page/{page}/"
        html_doc = requests.get(url)
        if html_doc.status_code == 200:
            soup = BeautifulSoup(html_doc.content, 'html.parser')
            quotes = soup.find_all('div', class_='quote')
            for quote in quotes:
                quote_text = quote.find('span', class_='text').text.strip()
                author_name = quote.find('small', class_='author').text.strip()
                tags = [tag.text for tag in quote.find_all('a', class_='tag')]

                # Збираємо інформацію про автора, якщо її ще немає
                if author_name not in authors:
                    author_url = quote.find('a')['href']
                    authors[author_name] = get_author_info(author_url)

                quotes_.append({
                    'tags': tags,
                    'author': author_name,
                    'quote': quote_text
                })            
        page += 1        
    return quotes_, authors


def storedata_tofile(filename, data):
    # Збереження даних у JSON файли
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Data saved to {filename}.")


def storedata_tobd(filename, collection):
    # Читання даних з JSON файла
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Вставка даних в колекцію
    try:
        collection.insert_many(data) 
    except errors.PyMongoError as e:
        print(f"Error occurred while inserting data to DB from {filename}: {e}")

    print(f"Дані успішно занесено в MongoDB з {filename}!")


def main():
    # Отримуємо цитати та авторів
    quotes, authors = parse_data()

    storedata_tofile('quotes.json', quotes)  

    authors_ = [author for author in authors.values()]
    storedata_tofile('authors.json', authors_)    

    storedata_tobd('quotes.json', db["quotes"])
    storedata_tobd('authors.json', db["authors"])


if __name__ == '__main__':
    main()

