import os
import sys
import django
import csv
from collections import defaultdict

homepath = os.environ['HOMEPATH']
genesite = os.path.join(homepath,'Desktop/AWD Development Area/advanced_web_dev/ZZZ_midterm/genesite')

sys.path.append(genesite)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genesite.settings')

django.setup() 
from genedata.models import Domain

data_file = os.path.join(genesite,'csvfiles/pfam_descriptionsv2.csv')

# initialise the dictionary for hellos as a default dictionary
domains = defaultdict(list)

# open the CSV file(s) and read the data into dictionaries 
with open(data_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    #header = csv_reader.__next__()
    for row in csv_reader:
        #print(f'{row[0]} is domain_id \t {row[1]} is domain_description')
        domains[row[0]] = row[1]
        #print(domains[row[0]])

# Delete the contents of the tables
Domain.objects.all().delete()

domain_rows = {}

# set the DB object(s), retrieve the data from the dictionary and save into the DB object
print('LOADING DOMAINS')

for domain_id, domain_description in domains.items():
    row = Domain.objects.create(domain_id=domain_id, domain_description=domain_description)
    row.save()
    domain_rows[domain_id] = row

print('LOADING DOMAINS COMPLETE')
