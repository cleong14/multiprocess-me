#!/usr/bin/env python
from multiprocessing import Pool
import bs4 as bs
import requests
import re

menu_options = [
  '\n1. Add a domain name\n',
  '2. Start processing queue\n',
  '3. Stop processing queue\n',
  '4. Display logs\n',
  '5. Exit\n',
  '\nPlease select a process from the menu'
]

domain_list = [
  'https://devleague.com',
  'https://sudokrew.com',
  'https://google.com',
  'https://facebook.com'
]
scraped_domain_list = []
compare_url_list = []

options_str = ''

for options in menu_options:
  options_str += options

def handle_local_links(url, link):
  if link.startswith('/'):
    return url + link
  else:
    return link

def scraper():
  print('SCRAPER')
  try:
    to_scrape_list = {link for link in domain_list if link not in scraped_domain_list}
    # print('TO SCRAPE', to_scrape_list)
    for domain in domain_list:
      print('DOMAIN', domain)
      
      response = requests.get(domain)

      scraped_html = bs.BeautifulSoup(response.text, 'html.parser')
      # print('SOUP', soup)

      body = scraped_html.body
      # print('BODY', body)

      links = body.find_all('a')

      for link in links:
        url = str(link.get('href'))
        # print('URL', url)

        if url == '/':
          pass
        elif url == '#':
          pass
        elif url == '#!':
          pass
        elif url == 'None':
          pass
        elif url.startswith('/'):
          new_url = domain + url
          domain_list.append(new_url)
          pass
        else:
          # print('URL', url)
          # print(domain_list)
          domain_list.append(url)

        # if str(link) == '/':
        #   print('ONLY /////')

      scraped_domain_list.append(domain)
      domain_list.remove(domain)
      # print('TO SCRAPE', to_scrape_list)

      print(domain_list)
      print(scraped_domain_list)

      # links = [link.get('href') for link in body.find_all('a')]
      # links = [handle_local_links(url,link) for link in links]
      # links = [str(link.encode('ascii')) for link in links]
      # return links


  except TypeError as e:
    print(e)
    print('Got a TypeError, probably got a None that we tried to iterate over')
    return []

  except IndexError as e:
    print(e)
    print('We probably did not find any useful links, returning empty list')
    return []

  except AttributeError as e:
    print(e)
    print('Likely got None for links, so we are throwing this')

  except Exception as e:
    print(str(e))
    return []
 
def main():
  print(options_str)

  num_processes = 4
  p = Pool(processes=num_processes)

  while True:
    try:
      value = int(input())

      if value == 1:
        print('\nInput domain info below:\n')

        domain_str = 'https://' + input('Domain Name: ')

        domain_list.append(domain_str)
        print('Domains: ', domain_list)

        main()

      if value == 2:
        print('\nProcessing...\n')

        scraper()
        print('\nDONE SCRAPING')

        p.close()

        main()

      if value == 3:
        print('Stopping queue...')

        main()

      if value == 4:
        print('Logs below...')
        return value

      if value == 5:
        print('Exiting...')
        return value

    except ValueError:
      print('Please enter an integar')
      continue

    # if value not in (0, 6):
    #   print('Please select an option from the menu')
    #   continue
    # else:
    #   break

  print('VALUE', value)
  pass


if __name__ == "__main__":
  main()
