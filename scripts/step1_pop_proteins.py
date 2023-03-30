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
from genedata.models import Protein

data_file = os.path.join(genesite,'csvfiles/assignment_data_sequences.csv')

# initialise the dictionary for hellos as a default dictionary
proteins = defaultdict(list)

# open the CSV file(s) and read the data into dictionaries 
with open(data_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    #header = csv_reader.__next__()
    for row in csv_reader:
        #print(f'{row[0]} is protein_id \t {row[1]} is sequence \t {len(row[1])}')
        proteins[row[0]] = row[1]
        #print(proteins[row[0]])

# Delete the contents of the tables
Protein.objects.all().delete()

protein_rows = {}

# set the DB object(s), retrieve the data from the dictionary and save into the DB object
print('LOADING PROTEINS')

for protein_id, sequence in proteins.items():
    row = Protein.objects.create(protein_id=protein_id, sequence=sequence, length=len(sequence))
    row.save()
    protein_rows[protein_id] = row

print('LOADING PROTEINS COMPLETE')
