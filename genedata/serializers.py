from rest_framework import serializers
from .models import *

class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ['domain_id', 'domain_description']

class DomainListSerializer(serializers.ModelSerializer):
    pfam_id = serializers.SerializerMethodField('get_domain_fields')

    class Meta:
        model = Domain
        fields = ['id', 'pfam_id']

    def get_domain_fields(self, obj):
        return DomainSerializer(obj).data

class DomainListLenSerializer(serializers.ModelSerializer):
    pfam_id = serializers.SerializerMethodField('get_domain_fields')
    description = serializers.SerializerMethodField('get_domain_description')
    start = serializers.SerializerMethodField('get_assignment_start')
    stop = serializers.SerializerMethodField('get_assignment_stop')

    class Meta:
        model = Domain
        fields = ['id', 'pfam_id', 'description', 'start', 'stop']

    def get_domain_fields(self, obj):
        return DomainSerializer(obj).data

    def get_domain_description(self, obj):
        return obj.domain_description

    def get_assignment_start(self, obj):
        # querey the assignment table where the taxa_id = self
        assignment = Assignment.objects.filter(pfam_id=obj)
        start = assignment.values_list()[0][3]
        return start

    def get_assignment_stop(self, obj):
        # querey the assignment table where the taxa_id = self
        assignment = Assignment.objects.filter(pfam_id=obj)
        stop = assignment.values_list()[0][4]
        return stop

class OrganismSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organism
        fields = ['taxa_id', 'clade', 'genus', 'species']

class OrganismListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organism
        fields = ['taxa_id', 'genus']

class ProteinSerializer(serializers.ModelSerializer):
    # validate taxonomy data and field to be displayed
    taxonomy = OrganismSerializer(read_only=True)
    # define extra fields for list of domain for this protein
    domains = serializers.SerializerMethodField('get_extra_fields')

    class Meta:
        model = Protein
        fields = ['protein_id', 'sequence', 'taxonomy', 'length', 'domains']

    def get_extra_fields(self, obj):
        # querey the assignment table for records where protein__protein_id = self
        assignments = Assignment.objects.filter(protein__protein_id=obj)
        # then find the list of pfams/domains for that protein
        domain_list = set(assignments.values_list('pfam_id__domain_id', flat=True))
        # get those domain records for validation and display by a serializer list
        domains = Domain.objects.filter(domain_id__in=domain_list)
        return DomainListLenSerializer(domains, many=True).data

class ProteinPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protein
        fields = ['protein_id', 'sequence', 'taxonomy', 'length']

class ProteinListSerializer(serializers.ModelSerializer):
    taxonomy = OrganismSerializer()
    #domains = DomainListSerializer()

    class Meta:
        model = Protein
        fields = ['protein_id', 'taxonomy', 'length']

class ProteinListNoTaxSerializer(serializers.ModelSerializer):
    # No domain field required

    class Meta:
        model = Protein
        fields = ['id', 'protein_id']

class AssignmentListSerializer(serializers.ModelSerializer):
    protein = ProteinSerializer()
    pfam_id = DomainSerializer()

    class Meta:
        model = Assignment
        fields = ['protein', 'pfam_id', 'start', 'stop']
