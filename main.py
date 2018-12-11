#!/usr/bin/env python

menu_options = [
  '1. Add a domain name\n'
  '2. Start processing queue\n',
  '3. Stop processing queue\n',
  '4. Display logs\n',
  '5. Exit\n'
]

domain_options = []

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

        print(domain_vals)

        return write_logs(domain_vals)

      if value == 2:
        print('Starting queue...')

        return value

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

def write_logs(log_input):
  while True:
    try:
      value = dict(log_input)

      if type(value) is dict:
        full_address = value['ip_address'] + ':' + value['port']
        domain_name = value['domain']
        ip_address = value['ip_address']
        port_num = value['port']
        log_text = '\n====================\n\n' + 'Domain Name: ' + domain_name + '\n' + 'IP Address: ' + ip_address + '\n' + 'Port: ' + port_num + '\n'

        # Write to masterlogs.txt
        master_text = '\nWriting to Master Logs...\n' + log_text
        master_fh = open('./masterlogs.txt', 'a+')
        master_fh.writelines(master_text)
        master_fh.close()

        master_fh_reopen = open('./masterlogs.txt', 'r')
        master_contents = master_fh_reopen.read()
        print(master_contents)

        # Write to domains.txt
        domains_text = '\nWriting to Domains Logs...\n' + log_text
        domains_fh = open('./domains.txt', 'a+')
        domains_fh.writelines(domains_text)
        domains_fh.close()

        domains_fh_reopen = open('./domains.txt', 'r')
        domains_contents = domains_fh_reopen.read()
        print(domains_contents)
        break
      
    except Exception as e:
      print('Value Error!', e)
      break

  domain_dict = {
    'domain': domain_name,
    'ip': ip_address,
    'port': port_num,
    'ip_port': full_address
  }

  domain_options.append(domain_dict)

  print('DOMAIN OPTIONS', domain_options)

  return get_user_selection('Please select a process from the menu\n')

if __name__ == '__main__':
  get_user_selection('Please select a process from the menu\n')
