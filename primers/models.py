from django.db import models

class GeneSymbol(models.Model):
    """A model to store official gene symbols for fast lookups."""
    symbol = models.CharField(max_length=50, db_index=True)
    species = models.CharField(max_length=50, db_index=True)

    class Meta:
        # Ensure that each symbol is unique per species
        unique_together = ('symbol', 'species')
        verbose_name = "Gene Symbol"
        verbose_name_plural = "Gene Symbols"

    def __str__(self):
        return f"{self.symbol} ({self.species})"

class PrimerPair(models.Model):
    species = models.CharField(max_length=50, default='human', db_index=True)
    gene = models.CharField(max_length=32, db_index=True)
    f_sequence = models.CharField(max_length=255)
    r_sequence = models.CharField(max_length=255)
    f_gene = models.CharField(max_length=40)
    r_gene = models.CharField(max_length=40)

    f_author_gene_list = models.JSONField(default=list, blank=True)
    r_author_gene_list = models.JSONField(default=list, blank=True)
    f_pmcid_list = models.JSONField(default=list, blank=True)
    r_pmcid_list = models.JSONField(default=list, blank=True)
    f_reg_pmcid_list = models.JSONField(default=list, blank=True)
    r_reg_pmcid_list = models.JSONField(default=list, blank=True)
    f_inv_pmcid_list = models.JSONField(default=list, blank=True)
    r_inv_pmcid_list = models.JSONField(default=list, blank=True)
    pair_shared_pmcid_list = models.JSONField(default=list, blank=True)
    f_found_list = models.JSONField(default=list, blank=True)
    r_found_list = models.JSONField(default=list, blank=True)

    # FIX: Added default=0.0 to all FloatFields that could be empty
    f_evalue = models.FloatField(default=0.0)
    r_evalue = models.FloatField(default=0.0)
    f_Tm_C = models.FloatField(default=0.0)
    r_Tm_C = models.FloatField(default=0.0)
    f_GC_pct = models.FloatField(default=0.0)
    r_GC_pct = models.FloatField(default=0.0)
    f_self_comp = models.FloatField(default=0.0)
    r_self_comp = models.FloatField(default=0.0)
    pair_comp = models.FloatField(default=0.0)
    evidence_score = models.FloatField(default=0.0)
    biophysics_score = models.FloatField(default=0.0)
    synergy_score = models.FloatField(default=0.0)
    pickr_score = models.FloatField(default=0.0)
    percentile = models.FloatField(default=0.0)

    # FIX: Added default=0 to all IntegerFields that could be empty
    f_occurrence_count = models.IntegerField(default=0)
    r_occurrence_count = models.IntegerField(default=0)
    f_total_citations = models.IntegerField(default=0)
    r_total_citations = models.IntegerField(default=0)
    f_pmcid_count = models.IntegerField(default=0)
    r_pmcid_count = models.IntegerField(default=0)
    f_match_start = models.IntegerField(default=0)
    r_match_start = models.IntegerField(default=0)
    f_match_end = models.IntegerField(default=0)
    r_match_end = models.IntegerField(default=0)
    f_orientation = models.CharField(max_length=8, blank=True)
    r_orientation = models.CharField(max_length=8, blank=True)
    f_reg_pmcid_count = models.IntegerField(default=0)
    r_reg_pmcid_count = models.IntegerField(default=0)
    f_inv_pmcid_count = models.IntegerField(default=0)
    r_inv_pmcid_count = models.IntegerField(default=0)
    pair_shared_pmcid_count = models.IntegerField(default=0)
    f_found = models.IntegerField(default=0)
    r_found = models.IntegerField(default=0)

    # Cross Specificity Fields
    # FIX: Changed CharField to JSONField to correctly store list data.
    f_cross_specificity_0 = models.JSONField(default=list, blank=True)
    r_cross_specificity_0 = models.JSONField(default=list, blank=True)
    f_cross_specificity_0_seq = models.JSONField(default=list, blank=True)
    r_cross_specificity_0_seq = models.JSONField(default=list, blank=True)
    f_cross_specificity_1 = models.JSONField(default=list, blank=True)
    r_cross_specificity_1 = models.JSONField(default=list, blank=True)
    f_cross_specificity_1_seq = models.JSONField(default=list, blank=True)
    r_cross_specificity_1_seq = models.JSONField(default=list, blank=True)
    f_cross_specificity_2 = models.JSONField(default=list, blank=True)
    r_cross_specificity_2 = models.JSONField(default=list, blank=True)
    f_cross_specificity_2_seq = models.JSONField(default=list, blank=True)
    r_cross_specificity_2_seq = models.JSONField(default=list, blank=True)
    f_cross_specificity_3 = models.JSONField(default=list, blank=True)
    r_cross_specificity_3 = models.JSONField(default=list, blank=True)
    f_cross_specificity_3_seq = models.JSONField(default=list, blank=True)
    r_cross_specificity_3_seq = models.JSONField(default=list, blank=True)
    f_cross_specificity_4 = models.JSONField(default=list, blank=True)
    r_cross_specificity_4 = models.JSONField(default=list, blank=True)
    f_cross_specificity_4_seq = models.JSONField(default=list, blank=True)
    r_cross_specificity_4_seq = models.JSONField(default=list, blank=True)


    class Meta:
        unique_together = (('species', 'gene', 'f_sequence', 'r_sequence'),)
        ordering = ('-pickr_score',)

