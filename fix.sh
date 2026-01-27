#!/bin/bash
echo "--- STARTING PRIMER UPLOADING ---"
python manage.py import_primers --species frog --path csv_data_frog
python manage.py import_primers --species fly --path csv_data_fly
python manage.py import_primers --species mouse --path csv_data_mouse
python manage.py import_primers --species monkey --path csv_data_monkey
python manage.py import_primers --species rat --path csv_data_rat
python manage.py import_primers --species pig --path csv_data_pig
python manage.py import_primers --species cow --path csv_data_cow
python manage.py import_primers --species worm --path csv_data_worm
python manage.py import_primers --species zebrafish --path csv_data_zebrafish
echo "--- PIPELINE FINISHED SUCCESSFULLY ---"