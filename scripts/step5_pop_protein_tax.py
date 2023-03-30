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
from genedata.models import Organism, Protein

data_file = os.path.join(genesite,'csvfiles/assignment_data_set.csv')

# initialise the dictionary for organisms as a default dictionary
proteins = defaultdict(list)
last_protein_id = 0

# open the CSV file(s) and read the data into dictionaries 
with open(data_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    #header = csv_reader.__next__()
    for row in csv_reader:
        if row[0] != last_protein_id :
            proteins[row[0]] = row[1]
            #print(row[0],proteins[row[0]])
            last_protein_id = row[0]

# set the DB object(s), retrieve the data from the dictionary and save into the DB object
print('LOADING PROTEINS WITH TAX')

for item in proteins.items():
    # get the protein id and taxa_id data
    protein_id = item[0]
    taxa_id = item[1]

    #print(protein_id, taxa_id)
    
    # Look up the value in the of the taxa_id in the organism table
    try:
        protein = Protein.objects.get(protein_id=protein_id)
    except ObjectDoesNotExist:
        protein = None
    try:
        organism = Organism.objects.get(taxa_id=taxa_id)
    except ObjectDoesNotExist:
        organism = None

    # Set the protein.tax_id field only if it exists
    if protein != None:
        protein.taxonomy = organism
        protein.save()

print('LOADING PROTEINS WITH TAX COMPLETE')
