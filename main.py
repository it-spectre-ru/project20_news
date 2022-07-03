import requests
from bs4 import BeautifulSoup


headers = {
  "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}

def get_articles_urls(url):
  s = requests.Session()
  response = s.get(url=url, headers=headers)

  pagination_count = 10

  for page in range(1, pagination_count):
    response = s.get(url=f"https://hi-news.ru/page/{page}", headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    articles_urls = soup.find_all('h2', class_="post__title")
    
    for au in articles_urls:
      art_url = au.find("a").get("href")
      print(art_url)

  # with open('index.html', "w") as file:
  #   file.write(response.text)

def main():
  get_articles_urls(url='https://hi-news.ru/')

if __name__ == "__main__":
  main()