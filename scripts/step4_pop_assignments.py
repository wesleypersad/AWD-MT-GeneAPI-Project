import os
import sys
import django
import csv
from collections import defaultdict
from django.core.exceptions import ObjectDoesNotExist

homepath = os.environ['HOMEPATH']
genesite = os.path.join(homepath,'Desktop/AWD Development Area/advanced_web_dev/ZZZ_midterm/genesite')

sys.path.append(genesite)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genesite.settings')

django.setup() 
from genedata.models import Organism, Domain, Protein, Assignment

data_file = os.path.join(genesite,'csvfiles/assignment_data_set.csv')

# initialise the dictionary for hellos as a default dictionary
assignments = defaultdict(list)
rownum=1

# open the CSV file(s) and read the data into dictionaries 
with open(data_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
#    header = csv_reader.__next__()
    for row in csv_reader:
        #print(f'{row[0]} is protein_id \t {row[6]} is start \t {row[7]} is end \n')
        assignments[rownum] = row
        rownum+=1

# Delete the contents of the tables
Assignment.objects.all().delete()

# set the DB object(s), retrieve the data from the dictionary and save into the DB object
print('LOADING ASSIGNMENTS')

for item in assignments.items():
    #print(item[1][0])
    #get the data values
    protein = item[1][0]
    pfam_id = item[1][5]
    start = item[1][6]
    stop = item[1][7]

    # lookup the fks
    try:
        protein = Protein.objects.get(protein_id=protein)
    except ObjectDoesNotExist:
        protein = None
    try:
        pfam_id = Domain.objects.get(domain_id=pfam_id)
    except ObjectDoesNotExist:
        pfam_id = None

    row = Assignment.objects.create(protein=protein, pfam_id=pfam_id, start=start, stop=stop )
    row.save()

print('LOADING ASSIGNMENTS COMPLETE')
