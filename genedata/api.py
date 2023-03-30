from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *

@api_view(['GET'])
def domain_detail(request, domain_id):
    try:
        domain = Domain.objects.get(domain_id=domain_id)
    except Domain.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DomainSerializer(domain)
        return Response(serializer.data)

@api_view(['GET'])
def domain_list(request):
    try:
        domain = Domain.objects.all()
    except Domain.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DomainListSerializer(domain, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def protein_detail(request, protein_id):
    try:
        protein = Protein.objects.get(protein_id=protein_id)
    except Protein.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProteinSerializer(protein)
        return Response(serializer.data)

@api_view(['POST'])
def protein_create(request):
    # get the taxonomy which is used to find a taxa_id
    # check that if does not exist
    try:
        taxonomy = request.data["taxonomy"]
    except KeyError:
        taxonomy = []

    # search for the taxonomy id with that taxonomy
    try:
        organism = Organism.objects.get(taxa_id = taxonomy)
        taxa_id = organism.id
    except Organism.DoesNotExist:
        taxa_id = None

    # update the taxonomy with the id
    request.data.update({"taxonomy": taxa_id})

    serializer = ProteinPostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['GET'])
def protein_list(request):
    try:
        protein = Protein.objects.all()
    except Protein.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProteinListSerializer(protein, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def organism_detail(request, taxa_id):
    try:
        organism = Organism.objects.get(taxa_id=taxa_id)
    except Organism.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrganismSerializer(organism)
        return Response(serializer.data)

@api_view(['GET'])
def organism_list(request):
    try:
        organism = Organism.objects.all()
    except Organism.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrganismListSerializer(organism, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def assignment_list(request):
    try:
        assignment = Assignment.objects.all()
    except Assignment.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AssignmentListSerializer(assignment, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def assignment_protein_list(request, protein_id):
    try:
        assignment = Assignment.objects.filter(protein__protein_id=protein_id)
    except Assignment.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AssignmentListSerializer(assignment, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def proteins_for_organism_list(request, taxa_id):
    # find all the proteins for a given taxa_id
    try:
        protein = Protein.objects.filter(taxonomy__taxa_id=taxa_id)
    except Protein.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # call the serializer to validate and display the required fields
        serializer = ProteinListNoTaxSerializer(protein, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def domains_in_proteins_for_organism_list(request, taxa_id):
    # get the list of proteins that have this taxa_id
    try:
        protein = Protein.objects.filter(taxonomy__taxa_id=taxa_id)
    except Protein.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # then get a list of unique proteins
        protein_list = set(protein.values_list('protein_id', flat=True))

        # with this protein list find all matching assignments records with unique domains
        assignment = Assignment.objects.filter(protein__protein_id__in=protein_list)
        domain_list = set(assignment.values_list('pfam_id__domain_id', flat=True))

        # return the domain records for this list
        domain = Domain.objects.filter(domain_id__in=domain_list)

        # validate data of fileds to be displayed in serializer list
        serializer = DomainListSerializer(domain, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def protein_coverage(request, protein_id):
    # first get the record of the protein
    try:
        protein = Protein.objects.get(protein_id=protein_id)
    except Protein.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # then get its length
        length = protein.length

        # find all the domains for this protein from the assignments table
        assignment = Assignment.objects.filter(protein__protein_id=protein_id)

        # initialise the total for lengths of domains
        section=0

        # loop through every domain and add its lenth to the total
        for item in assignment:
            section = section + (item.stop-item.start)

        # calculate and return the protein's coverage
        coverage= {'coverage': section/length}
        return Response(coverage)