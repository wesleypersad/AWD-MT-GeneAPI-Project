from django.urls import include, path
from . import views
from . import api

urlpatterns = [
    path('', views.index, name='index'),
    # THE FOLLOWING FULLY WORK AS REQUIRED BY THE MIDTERM SPEC !!!
    path('api/protein/', api.protein_create),
    path('api/protein/<str:protein_id>/', api.protein_detail),
    # Same as api/pfam/<str:pfam_id>/
    path('api/pfam/<str:domain_id>/', api.domain_detail),
    path('api/proteins/<str:taxa_id>/', api.proteins_for_organism_list),
    path('api/pfams/<str:taxa_id>/', api.domains_in_proteins_for_organism_list),
    path('api/coverage/<protein_id>/', api.protein_coverage),
    # THE PATHS BELOW WORK BUT ARE NOT A REQUIREMENT OF MIDTERM SPEC !!!
    path('api/pfams/', api.domain_list),
    path('api/proteins/', api.protein_list),
    path('api/domains/', api.domain_list),
    path('api/assignments/', api.assignment_list),
    path('api/assignments/<str:protein_id>', api.assignment_list),
]