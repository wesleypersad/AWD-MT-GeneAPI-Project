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
from genedata.models import Organism

data_file = os.path.join(genesite,'csvfiles/assignment_data_set.csv')

# initialise the dictionary for hellos as a default dictionary
organisms = defaultdict(list)
last_taxa_id = 0

# open the CSV file(s) and read the data into dictionaries 
with open(data_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    #header = csv_reader.__next__()
    for row in csv_reader:
        if row[1] != last_taxa_id :
            organisms[row[1]] = row[2:4]
            #print(organisms[row[1]])
            last_taxa_id = row[1]

# Delete the contents of the tables
Organism.objects.all().delete()

organism_rows = {}

# set the DB object(s), retrieve the data from the dictionary and save into the DB object
print('LOADING ORGANISMS')

for item in organisms.items():
# Split genus into genus & species
    genus_species = item[1][1].split(" ")
    row = Organism.objects.create(taxa_id=item[0], clade=item[1][0], genus=genus_species[0], species = genus_species[1])
    row.save()
    organism_rows[item[0]] = row
    #print(item[1][1])

print('LOADING ORGANISMS COMPLETE')
