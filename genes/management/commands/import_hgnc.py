# genes/management/commands/import_hgnc.py
import csv
from django.core.management.base import BaseCommand
from genes.models import Gene

class Command(BaseCommand):
    help = 'Imports gene data from an HGNC TSV file'

    def add_arguments(self, parser):
        parser.add_argument('tsv_file', type=str, help='The path to the HGNC TSV file')

    def handle(self, *args, **options):
        tsv_file_path = options['tsv_file']
        self.stdout.write(self.style.SUCCESS(f'Starting import from {tsv_file_path}'))

        # Clear existing data
        Gene.objects.all().delete()
        self.stdout.write(self.style.WARNING('Existing Gene data cleared.'))

        with open(tsv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')
            genes_to_create = []
            for row in reader:
                # Check for the required symbol field
                if not row.get('symbol'):
                    continue

                genes_to_create.append(
                    Gene(
                        hgnc_id=row.get('hgnc_id'),
                        symbol=row.get('symbol'),
                        name=row.get('name'),
                        locus_group=row.get('locus_group'),
                        locus_type=row.get('locus_type'),
                        status=row.get('status'),
                        location=row.get('location'),
                        alias_symbol=row.get('alias_symbol'),
                        prev_symbol=row.get('prev_symbol'),
                        gene_group=row.get('gene_group'),
                        entrez_id=row.get('entrez_id'),
                        ensembl_gene_id=row.get('ensembl_gene_id'),
                    )
                )

        # Use bulk_create for efficiency
        Gene.objects.bulk_create(genes_to_create, batch_size=1000)

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(genes_to_create)} genes.'))