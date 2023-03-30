from django.db import models

# Create the pfam/domain class
class Domain(models.Model):
    domain_id = models.CharField(max_length=200, null=False, blank=False)
    domain_description = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self): 
        return self.domain_id

# Create the organism class
class Organism(models.Model):
    taxa_id = models.CharField(max_length=200, null=False, blank=False)
    clade = models.CharField(max_length= 1, null=False, blank=False)
    genus = models.CharField(max_length=200, null=False, blank=False)
    species = models.CharField(max_length=200, default='EMPTY', null=False, blank=False)

    def __str__(self): 
        return self.taxa_id

# Create the proteins class
class Protein(models.Model):
    protein_id = models.CharField(max_length=200, null=False, blank=False)
    sequence = models.CharField(max_length=40000, null=False, blank=True)
    length = models.IntegerField(null=False, default=0)
    taxonomy = models.ForeignKey(Organism, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self): 
        return self.protein_id

# Create the assignment class
class Assignment(models.Model):
    protein = models.ForeignKey(Protein, blank=True, null=True, on_delete=models.SET_NULL)
    pfam_id = models.ForeignKey(Domain, blank=True, null=True, on_delete=models.SET_NULL)
    start = models.IntegerField(null=False, blank=False)
    stop = models.IntegerField(null=False, blank=False)
