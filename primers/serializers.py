from rest_framework import serializers
from .models import PrimerPair

class PrimerPairSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrimerPair
        # Add all your new model fields here to expose them in the API
        fields = [
            'gene', 'f_sequence', 'r_sequence', 'pickr_score',
            'f_Tm_C', 'r_Tm_C', 'f_GC_pct', 'r_GC_pct',
            'f_pmcid_count', 'r_pmcid_count',
            'f_match_start', 'f_match_end', 'r_match_start', 'r_match_end',
            'evidence_score', 'biophysics_score', 'synergy_score',

            # Add the new complementarity scores
            'f_self_comp', 'r_self_comp', 'pair_comp',

            # Add the new citation counts for the details dropdown
            'f_reg_pmcid_count', 'r_reg_pmcid_count',
            'f_inv_pmcid_count', 'r_inv_pmcid_count',

            # Add the shared citation count and list
            'pair_shared_pmcid_count',
            'pair_shared_pmcid_list',

            # Add the specific citation lists for the details section
            'f_reg_pmcid_list', 'f_inv_pmcid_list',
            'r_reg_pmcid_list', 'r_inv_pmcid_list',
        ]
