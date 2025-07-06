from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from pathlib import Path
import pandas as pd
import re
import ast

from primers.models import PrimerPair
from django.db import models

class Command(BaseCommand):
    help = 'Import primer CSVs from a specified directory for a given species, with explicit column handling.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path', type=str, required=True,
            help='Path to the directory containing the CSV files.'
        )
        parser.add_argument(
            '--species', type=str, required=True,
            help='The species for this dataset (e.g., "human", "mouse").'
        )
        parser.add_argument(
            '--clear', action='store_true',
            help='Clear all primers for the specified species before importing.'
        )

    def handle(self, *args, **options):
        csv_dir = Path(options['path'])
        species = options['species'].lower()

        if not csv_dir.exists():
            raise CommandError(f'CSV directory not found: {csv_dir}')

        if options['clear']:
            self.stdout.write(self.style.WARNING(f"Clearing all existing primer data for species: '{species}'..."))
            deleted_count, _ = PrimerPair.objects.filter(species=species).delete()
            self.stdout.write(self.style.SUCCESS(f"Deleted {deleted_count} primer pairs."))

        files = list(csv_dir.glob('*.csv'))
        if not files:
            self.stdout.write(self.style.WARNING(f'No CSV files found in {csv_dir}'))
            return

        self.stdout.write(f"Starting import for species: '{species}' from directory: {csv_dir}")

        field_map = {f.name: f for f in PrimerPair._meta.get_fields() if f.name != 'id'}
        
        total_created = 0
        total_updated = 0

        for file in files:
            gene = file.stem.upper()
            self.stdout.write(f'Processing {file.name} (gene={gene})')

            try:
                df = pd.read_csv(file, sep=None, engine='python', dtype=str).fillna('')
                df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Could not read or process CSV {file.name}: {e}"))
                continue

            for row in df.itertuples(index=False):
                row_dict = row._asdict()

                f_seq = row_dict.get('f_sequence', '').strip()
                r_seq = row_dict.get('r_sequence', '').strip()

                if not f_seq or not r_seq:
                    continue
                
                defaults = {}

                # --- START DEBUGGING BLOCK ---
                is_debug_gene = (gene == 'SLC2A3') 
                if is_debug_gene:
                    self.stdout.write(self.style.NOTICE(f"\n--- DEBUGGING ROW for {gene} ---"))
                    self.stdout.write(f"Raw f_cross_specificity_0 from CSV: '{row_dict.get('f_cross_specificity_0', '')}'")
                    self.stdout.write(f"Raw f_cross_specificity_1 from CSV: '{row_dict.get('f_cross_specificity_2', '')}'")
                # --- END DEBUGGING BLOCK ---

                for field_name, model_field in field_map.items():
                    csv_key = field_name.lower()
                    if csv_key not in row_dict:
                        continue

                    raw_val = row_dict.get(csv_key, '').strip()

                    if raw_val:
                        try:
                            if isinstance(model_field, models.JSONField):
                                if raw_val.startswith('[') and raw_val.endswith(']'):
                                    defaults[field_name] = ast.literal_eval(raw_val)
                                else:
                                    items = [x.strip() for x in str(raw_val).replace(';', ',').split(',') if x.strip()]
                                    if 'pmcid_list' in field_name:
                                        defaults[field_name] = [int(re.sub(r'\D', '', item)) for item in items if re.sub(r'\D', '', item)]
                                    else:
                                        defaults[field_name] = items
                            elif isinstance(model_field, models.IntegerField):
                                defaults[field_name] = int(float(raw_val))
                            elif isinstance(model_field, models.FloatField):
                                defaults[field_name] = float(raw_val)
                            else:
                                defaults[field_name] = raw_val
                        except (ValueError, TypeError, SyntaxError) as e:
                            self.stdout.write(self.style.WARNING(f"Could not convert value '{raw_val}' for field '{field_name}' in {gene}. Error: {e}. Skipping field."))
                            continue
                
                # --- START DEBUGGING BLOCK ---
                if is_debug_gene:
                    self.stdout.write(f"Final `defaults` dictionary before saving:")
                    self.stdout.write(str(defaults))
                    self.stdout.write("--- END DEBUGGING ROW ---\n")
                # --- END DEBUGGING BLOCK ---

                defaults.pop('species', None)
                defaults.pop('gene', None)
                defaults.pop('f_sequence', None)
                defaults.pop('r_sequence', None)

                try:
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
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error saving row for {gene} ({f_seq}/{r_seq}): {e}"))


        self.stdout.write(self.style.SUCCESS(f"Import for species '{species}' complete. Created: {total_created}, Updated: {total_updated} primer pairs."))
