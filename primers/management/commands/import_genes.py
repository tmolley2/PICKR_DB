# primers/management/commands/import_genes.py

import csv
from django.core.management.base import BaseCommand
from primers.models import GeneSymbol

class Command(BaseCommand):
    help = 'Imports gene symbols from a CSV file for a specified species, with an option to clear existing entries first.'

    def add_arguments(self, parser):
        # Argument for the CSV file path
        parser.add_argument('csv_file', type=str, help='The path to the CSV file.')
        # Argument for the species name (e.g., "human", "mouse")
        parser.add_argument('species', type=str, help='The species for these genes.')
        # [ADDED] Optional argument to clear existing genes for the species before import
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing gene symbols for this species before importing.',
        )

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        species = options['species'].lower()
        should_clear = options['clear']

        # [ADDED] Logic to clear existing data if the --clear flag is used
        if should_clear:
            self.stdout.write(self.style.WARNING(f"Deleting all existing gene symbols for '{species}'..."))
            deleted_count, _ = GeneSymbol.objects.filter(species=species).delete()
            self.stdout.write(self.style.SUCCESS(f"Successfully deleted {deleted_count} old symbols."))

        self.stdout.write(f"Starting import for '{species}' from '{csv_file_path}'...")

        # Keep track of how many genes are created
        created_count = 0
        
        try:
            with open(csv_file_path, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if not row:
                        continue
                    
                    symbol = row[0].strip().upper()
                    
                    if not symbol:
                        continue

                    # get_or_create is efficient and avoids creating duplicates
                    _, created = GeneSymbol.objects.get_or_create(
                        symbol=symbol,
                        species=species
                    )
                    if created:
                        created_count += 1
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Error: The file '{csv_file_path}' was not found."))
            return


        self.stdout.write(self.style.SUCCESS(
            f"Successfully imported genes for '{species}'. "
            f"Added {created_count} new symbols to the database."
        ))
