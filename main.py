#!/usr/bin/env python
import time
import requests
from multiprocessing import Process, Queue, current_process

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

options_str = ''

for options in menu_options:
  options_str += options

NUM_WORKERS = 4

done_queue = Queue()  # This is messages from the child processes for parent
process_queue = Queue()  # This is the domains to process

def scraper(process_queue, done_queue):
  done_queue.put("{} starting".format(current_process().name))

  for domain in iter(process_queue.get, 'STOP'):
    result = requests.get(domain)
    print("{}: Domain {} retrieved with {} bytes".format(current_process().name, domain, len(result.text)))
    done_queue.put("{}: Domain {} retrieved with {} bytes".format(current_process().name, domain, len(result.text)))

  # Print initial menu / everytime the scraper is ran 
  print(options_str)

for i in range(NUM_WORKERS):
  Process(target=scraper, args=(process_queue, done_queue)).start()

def main():
  print(options_str)

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

        for domain in domain_list:
          process_queue.put(domain)
          
        for message in iter(done_queue.get, 'STOP'):
          print(message)
          message = 'STOP'
          done_queue.put(message)

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
