from urllib import response
import requests
from bs4 import BeautifulSoup
import time
from random import randrange



headers = {
  "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}

def get_articles_urls(url):
  s = requests.Session()
  response = s.get(url=url, headers=headers)

  pagination_count = 15


  articles_urls_list = []
  for page in range(1, pagination_count + 1):
    response = s.get(url=f"https://hi-news.ru/page/{page}", headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    articles_urls = soup.find_all('h2', class_="post__title")
    
    for au in articles_urls:
      art_url = au.find("a").get("href")
      articles_urls_list.append(art_url)

    time.sleep(randrange(2, 5))
    print(f'Done {page} / {pagination_count}')
 
  with open('articles_urls.txt', 'w') as file:
    for url in articles_urls_list:
      file.write(f'{url}\n')

  return 'Done'



def get_data(file_path):
  with open(file_path) as file:
    urls_list = [line.strip() for line in file.readlines()]

  s = requests.Session()

  for url in urls_list[:5]:
    response = s.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    article_title = soup.find('h1', class_='single-title').text.strip()
    article_time = soup.find('time', class_='post__date').text.strip()

    print(article_title)
    print(article_time)
  



def main():
  # print(get_articles_urls(url='https://hi-news.ru/'))
  get_data('articles_urls.txt')

if __name__ == "__main__":
  main()