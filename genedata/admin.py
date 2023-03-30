from django.contrib import admin
from .models import *

class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain_id', 'domain_description')

admin.site.register(Domain, DomainAdmin)

class ProteinAdmin(admin.ModelAdmin):
    list_display = ('protein_id', 'length', 'taxonomy', 'sequence')

admin.site.register(Protein, ProteinAdmin)

class OrganismAdmin(admin.ModelAdmin):
    list_display = ('taxa_id', 'clade', 'genus', 'species')

admin.site.register(Organism, OrganismAdmin)

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('protein', 'pfam_id', 'start', 'stop')

admin.site.register(Assignment, AssignmentAdmin)
