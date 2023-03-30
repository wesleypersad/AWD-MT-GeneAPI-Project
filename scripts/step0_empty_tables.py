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
from genedata.models import Assignment, Protein, Domain, Organism

# Delete the contents of the tables
Assignment.objects.all().delete()
Protein.objects.all().delete()
Domain.objects.all().delete()
Organism.objects.all().delete()
