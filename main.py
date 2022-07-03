import requests
from bs4 import BeautifulSoup
import time
from random import randrange
import json



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

  urls_count = len(urls_list)

  s = requests.Session()
  result_data = []

  for url in enumerate(urls_list):
    response = s.get(url=url[1], headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    try:
      article_title = soup.find('h1', class_='single-title').text.strip()
      article_time = soup.find('time', class_='post__date').text.strip()
      article_img_url = soup.find('div', class_='text').find('img').get('src')
      article_text = soup.find('div', class_='text').text.strip().replace('\n', '')
    except Exception as ex:
      print(f"errr: {ex}")
      continue

    result_data.append(
      {
        'original_url': url[1],
        'article_title': article_title,
        'article_time': article_time,
        'article_img_url': article_img_url,
        'article_text': article_text,
      }
    )

    print(f"Done {url[0] + 1} / {urls_count}")

  with open('result.json', 'w') as file:
    json.dump(result_data, file, indent=4, ensure_ascii=False)
  



def main():
  # print(get_articles_urls(url='https://hi-news.ru/'))
  get_data('articles_urls.txt')

if __name__ == "__main__":
  main()