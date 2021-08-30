import csv
import requests
import json
import argparse
import logging

# Remove when done
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def cl_arguments():
    parser = argparse.ArgumentParser(
        description=(
            'Script to perform bulk operations on through the BLABLA api. '
            'There are two main operations, download and upload. '
            'Download connects to the api, fetches site throttles and creates '
            'a csv file containing the data. '
            'Upload reads from a csv file and posts the objects to the api'
        )
    )

    parser.add_argument(
        'operation', type=str,
        help='Type of operation. Can be either "download" or "upload"',
        choices=['download', 'upload'], metavar='operation')

    parser.add_argument(
        'base_url', type=str,
        help='Domain name of the server you wish to connect to.')

    parser.add_argument(
        'username', type=str, help='Username')

    parser.add_argument(
        'password', type=str, help='Password belonging to username')

    parser.add_argument(
        '--log_level', '-l', type=str, choices=['info', 'debug'],
        help='Set logging level, default is set to warnings and above')

    parser.add_argument(
        '--filepath', '-f', type=str,
        help='Relative or absolute filepath of import/export file.')

    parser.add_argument(
        '--allow-duplicates', '-d', dest='allow_duplicates',
        action='store_true', help='Allow uploads of duplicates (obj name)')

    args = parser.parse_args()
    if args.log_level:
        logging.basicConfig(level=logging.INFO)
    if args.filepath:
        pass
    else:
        args.filepath = f'{args.username}_data.csv'

    return args


def fetch_token(url, usr, pwd):
    full_url = f'{url}/api/v2/session/login/'
    auth_data = {
        'username': usr,
        'password': pwd
    }
    logging.info(f'Fetching session token from {full_url}...')
    try:
        print(full_url)
        resp = requests.post(
            full_url,
            json=auth_data,
            verify=False,
            allow_redirects=True
        )
    except requests.exceptions.RequestException as err:
        raise SystemExit(
            'Request error while fetching token.'
            f'\nError message:\n{err}\n'
        )

    if resp.ok:
        logging.info('Session token received.')
        return resp.json()['data']['session']
    else:
        raise requests.exceptions.HTTPError(
            'HTTP response comes back with status code 4xx or 5xx.'
            f'\nCurrent HTTP response: {resp.status_code}\n')


def fetch_throttles(url, session_token):
    full_url = f'{url}/api/v2/site_throttles'
    logging.info(f'Fetching data from {full_url}...')
    try:
        resp = requests.get(
            full_url,
            headers={'session': session_token},
            verify=False
        )
    except requests.exceptions.RequestException as err:
        raise SystemExit(
            f'Request error while fetching token.\nError message:\n{err}\n')

    if resp.ok:
        resp_data = resp.json()['data']
        logging.info(f'Data received. {len(resp_data)} objects')
        return resp_data
    else:
        raise requests.exceptions.HTTPError(
            'HTTP response comes back with status code 4xx or 5xx.\n'
            f'Current HTTP response: {resp.status_code}\n')


def write_obj(url, session_token, obj):
    full_url = f'{url}/api/v2/site_throttles'

    resp = requests.post(
        full_url,
        headers={'session': session_token},
        data=json.dumps(obj),
        verify=False
    )
    if not resp.status_code == 200:
        logging.warning(
            f'Post of object failed. Object name: {obj["name"]}\n'
            f'SERVER RESPONSE: {resp.json()}\nFULL OBJECT:\n{obj}')
    else:
        return True


def csv_importer(filename):
    with open(filename, 'r') as csv_file:
        reader = csv.DictReader(csv_file, quoting=csv.QUOTE_NONNUMERIC)
        row_list = list(reader)

        objs = []
        for row in row_list:
            obj = {}
            for key, value in row.items():
                if type(value) == str and value[0] == '[' and value[-1] == ']':
                    obj[key] = eval(value)
                else:
                    obj[key] = value
            objs.append(obj)
        logging.info(
            f'{len(row_list)} rows in csv file conv to {len(objs)} objects')
        return objs


def csv_exporter(obj_list, filepath):
    objs = []  # List to store new objects without the id field
    for obj in obj_list:
        objs.append(
            {key: obj[key] for key in obj if key != 'id'}
        )
    obj_list = objs

    with open(filepath, 'w', newline='') as csv_file:
        fieldnames = obj_list[0].keys()
        writer = csv.DictWriter(
            csv_file, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for obj in obj_list:
            writer.writerow(obj)

    with open(filepath, 'r', newline='') as csv_file:
        row_num = len(list(csv.reader(csv_file)))
    logging.info(
        f'File {filepath} created. {row_num} lines written (including header)')


def download(args, token):
    throttles = fetch_throttles(args.base_url, token)
    csv_exporter(throttles, args.filepath)


def upload(args, token):
    current = [i['name'] for i in fetch_throttles(args.base_url, token)]
    csv_rows = csv_importer(args.filepath)

    success_counter, dup_counter = 0, 0
    for row in csv_rows:
        if args.allow_duplicates or row['name'] not in current:
            resp = write_obj(args.base_url, token, row)
            if resp:
                success_counter += 1
        else:
            logging.info(f'Duplicate not uploaded. Name: {row["name"]}')
            dup_counter += 1

    logging.info(
        f'{success_counter} objs uploaded. {dup_counter} duplicates omitted')


def main():
    args = cl_arguments()
    token = fetch_token(args.base_url, args.username, args.password)

    if args.operation == 'download':
        download(args, token)
    else:
        upload(args, token)


if __name__ == '__main__':
    main()
    print('End of script')
