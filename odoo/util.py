
import csv

def list_2_csv(filename, records, header = ""):

    with open(filename, 'w') as csv_file:

        writer = csv.writer(csv_file, quoting = csv.QUOTE_ALL)

        if header:
          writer.writerow(header.split(","))

        writer.writerows(records)

        rec_count = len(records)
        print("\n{:0,} rows written to {}\n".format(rec_count, filename))