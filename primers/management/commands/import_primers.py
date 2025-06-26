from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from pathlib import Path
import pandas as pd
import re

from primers.models import PrimerPair


class Command(BaseCommand):
    help = 'Import primer CSVs from a specified directory into the database for a given species.'

    def add_arguments(self, parser):
        # Argument for the CSV directory path
        parser.add_argument(
            '--path', type=str, required=True,
            help='Path to the directory containing the CSV files.'
        )
        # NEW: Argument to specify the species being imported
        parser.add_argument(
            '--species', type=str, required=True,
            help='The species for this dataset (e.g., "human", "mouse").'
        )

    def handle(self, *args, **options):
        csv_dir = Path(options['path'])
        species = options['species'].lower()

        if not csv_dir.exists():
            raise CommandError(f'CSV directory not found: {csv_dir}')

        files = list(csv_dir.glob('*.csv'))
        if not files:
            self.stdout.write(self.style.WARNING(f'No CSV files found in {csv_dir}'))
            return

        self.stdout.write(f"Starting import for species: '{species}' from directory: {csv_dir}")

        # Build mapping of lowercase model field names to actual field names
        field_map = {f.name.lower(): f.name for f in PrimerPair._meta.get_fields()}

        # Define fields that should be parsed as lists
        list_fields = {
            'f_author_gene_list', 'r_author_gene_list', 'f_pmcid_list', 'r_pmcid_list',
            'f_reg_pmcid_list', 'r_reg_pmcid_list', 'f_inv_pmcid_list', 'r_inv_pmcid_list',
            'pair_shared_pmcid_list'
        }

        total_created = 0
        total_updated = 0
        for file in files:
            gene = file.stem.upper()
            self.stdout.write(f'Processing {file.name} (gene={gene})')

            df = pd.read_csv(file, sep=None, engine='python', dtype=str).fillna('')

            for _, row in df.iterrows():
                raw = row.to_dict()
                defaults = {}

                # Map CSV columns to model fields
                for raw_key, raw_val in raw.items():
                    key = raw_key.strip().lower().replace(' ', '_') # More robust key cleaning
                    if key in field_map:
                        field_name = field_map[key]

                        # Parse list fields from comma/semicolon-separated strings
                        if field_name in list_fields:
                            if not raw_val:
                                parsed = []
                            else:
                                # Standardize delimiters and split
                                items = [x.strip() for x in str(raw_val).replace(';', ',').split(',') if x.strip()]
                                # Check if the field is a PMCID list to convert to integers
                                if 'pmcid_list' in field_name:
                                    parsed = []
                                    for item in items:
                                        # Extract digits only to handle formats like 'PMC12345'
                                        digits = re.sub(r'\D', '', item)
                                        if digits:
                                            parsed.append(int(digits))
                                else:
                                    parsed = items # Keep as list of strings otherwise
                            defaults[field_name] = parsed

                        # Handle other fields, converting to correct types
                        else:
                            # Skip if value is empty/null, letting model defaults apply if any
                            if raw_val == '':
                                continue

                            field_type = PrimerPair._meta.get_field(field_name).get_internal_type()
                            try:
                                if 'IntegerField' in field_type:
                                    defaults[field_name] = int(float(raw_val))
                                elif 'FloatField' in field_type:
                                    defaults[field_name] = float(raw_val)
                                else:
                                    defaults[field_name] = raw_val
                            except (ValueError, TypeError):
                                self.stdout.write(self.style.WARNING(f"Could not convert value '{raw_val}' for field '{field_name}' in gene {gene}. Skipping field."))
                                continue

                # Extract the unique identifiers for the object
                f_seq = raw.get('f_sequence', '').strip()
                r_seq = raw.get('r_sequence', '').strip()

                if not f_seq or not r_seq:
                    self.stdout.write(self.style.WARNING(f"Skipping row in {file.name} due to missing sequence data."))
                    continue

                # Remove sequences from defaults dict to avoid conflict
                defaults.pop('f_sequence', None)
                defaults.pop('r_sequence', None)
                defaults.pop('gene', None)
                defaults.pop('species', None)

                # Upsert into the database using the new unique key (species, gene, sequences)
                obj, created = PrimerPair.objects.update_or_create(
                    species=species,
                    gene=gene,
                    f_sequence=f_seq,
                    r_sequence=r_seq,
                    defaults=defaults
                )

                if created:
                    total_created += 1
                else:
                    total_updated += 1

        self.stdout.write(self.style.SUCCESS(f"Import for species '{species}' complete. Created: {total_created}, Updated: {total_updated} primer pairs."))
