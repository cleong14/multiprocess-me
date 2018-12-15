#!/usr/bin/env python
import os
import requests
from multiprocessing import Process, Queue, current_process

menu_options = [
  '1. Add a domain name\n'
  '2. Start processing queue\n',
  '3. Stop processing queue\n',
  '4. Display logs\n',
  '5. Exit\n'
]

domain_list = []
processes = []
scraped_domains = []

NUM_WORKERS = 4

done_queue = Queue() # Messages from child process for parent
process_queue = Queue() # Domains to process

def scraper(p_queue, d_queue):
  # print('SCRAPER')
  # print('STARTING PROCESS QUEUE', p_queue)
  # print('STARTING DONE QUEUE', d_queue)

  done_queue.put('{} starting'.format(current_process().name))

  for domain in iter(process_queue.get, 'STOP'):
    print('DOMAIN BRUH!', domain)

    result = requests.get(domain['domain'])
    # result_text = result.text
    
    print('TEXT', result.text)
    print("{}: Domain {} retrieved with {} bytes".format(current_process().name, domain, len(result.text)))

    done_queue.put('{}: Domain {} retrieved with {} bytes'.format(current_process().name, domain, len(result.text)))

# starts processes in the beginning then listens for call to action
for i in range(NUM_WORKERS):
  p = Process(target=scraper, args=(process_queue, done_queue))
  # print('P', p)
  p.start()
  # print('P AFTER START', p)

def get_user_selection(prompt):
  options_str = '\n'

  for options in menu_options:
    options_str += options
  print(options_str)

  while True:
    try:
      value = int(input(prompt))

      if value == 1:
        print('\nInput domain info below\n')

        domain_vals = {
          'domain': input('Domain Name: '),
          'ip_address': input('IP Address: '),
          'port': input('Port Number: ')
        }

        domain_list.append(domain_vals)
        process_queue.put(domain_vals)
        
        print(domain_list)
        
        get_user_selection('Please select a process from the menu\n')

      if value == 2:
        print('\nStarting queue...\n')

        scraper(process_queue, done_queue)

        return get_user_selection('Please select a process from the menu\n')

      if value == 3:
        print('Stopping queue...')

        return value

      if value == 4:
        print('Logs below...')
        return value

      if value == 5:
        print('Exiting...')
        return value

    except ValueError:
      print('Please enter an integar')
      continue

    if value not in (0, 6):
      print('Please select an option from the menu')
      continue
    else:
      break

  print('VALUE', value)
  return value

# def write_logs(log_input):
#   while True:
#     try:
#       value = dict(log_input)

#       if type(value) is dict:
#         full_address = value['ip_address'] + ':' + value['port']
#         domain_name = value['domain']
#         ip_address = value['ip_address']
#         port_num = value['port']
#         log_text = '\n====================\n\n' + 'Domain Name: ' + domain_name + '\n' + 'IP Address: ' + ip_address + '\n' + 'Port: ' + port_num + '\n'

#         # Write to masterlogs.txt
#         master_text = '\nWriting to Master Logs...\n' + log_text
#         master_fh = open('./masterlogs.txt', 'a+')
#         master_fh.writelines(master_text)
#         master_fh.close()

#         master_fh_reopen = open('./masterlogs.txt', 'r')
#         master_contents = master_fh_reopen.read()
#         print(master_contents)

#         # Write to domains.txt
#         domains_text = '\nWriting to Domains Logs...\n' + log_text
#         domains_fh = open('./domains.txt', 'a+')
#         domains_fh.writelines(domains_text)
#         domains_fh.close()

#         domains_fh_reopen = open('./domains.txt', 'r')
#         domains_contents = domains_fh_reopen.read()
#         print(domains_contents)
#         break
      
#     except Exception as e:
#       print('Value Error!', e)
#       break

#   domain_dict = {
#     'domain': domain_name,
#     'ip': ip_address,
#     'port': port_num,
#     'ip_port': full_address
#   }

#   domain_list.append(domain_dict)
#   print('DOMAIN OPTIONS', domain_list)

#   return get_user_selection('Please select a process from the menu\n')

if __name__ == '__main__':
  get_user_selection('Please select a process from the menu\n')
