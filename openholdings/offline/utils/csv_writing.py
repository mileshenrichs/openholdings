import os
import csv

def write_funds_to_csv(funds, csv_file_name):
    csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', csv_file_name)
    with open(csv_file_path, mode='w') as funds_file:
        funds_file.truncate()
        writer = csv.writer(funds_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
        writer.writerow(['Ticker', 'URL'])
        for fund in funds:
            writer.writerow(fund)