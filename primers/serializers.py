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
            'evidence_score', 'biophysics_score', 'synergy_score', 'percentile',

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
            'f_found_list', 'r_found_list',

            #cross specificity of genes
            'f_cross_specificity_0', 'r_cross_specificity_0',
            'f_cross_specificity_0_seq', 'r_cross_specificity_0_seq',
            'f_cross_specificity_1', 'r_cross_specificity_1',
            'f_cross_specificity_1_seq', 'r_cross_specificity_1_seq',
            'f_cross_specificity_2', 'r_cross_specificity_2',
            'f_cross_specificity_2_seq', 'r_cross_specificity_2_seq',
            'f_cross_specificity_3', 'r_cross_specificity_3',
            'f_cross_specificity_3_seq', 'r_cross_specificity_3_seq',
            'f_cross_specificity_4', 'r_cross_specificity_4',
            'f_cross_specificity_4_seq', 'r_cross_specificity_4_seq'

        ]
