from django.db import models

class PrimerPair(models.Model):
    # NEW: Add a field to store the species
    species = models.CharField(max_length=50, default='human', db_index=True)

    gene = models.CharField(max_length=32, db_index=True)
    f_sequence = models.CharField(max_length=255)
    r_sequence = models.CharField(max_length=255)
    f_gene = models.CharField(max_length=40)
    r_gene = models.CharField(max_length=40)

    # Use JSONField for list storage (compatible with SQLite and Postgres)
    f_author_gene_list = models.JSONField(default=list, blank=True)
    r_author_gene_list = models.JSONField(default=list, blank=True)
    f_pmcid_list = models.JSONField(default=list, blank=True)
    r_pmcid_list = models.JSONField(default=list, blank=True)

    # Fields for storing PMCID lists based on orientation
    f_reg_pmcid_list = models.JSONField(default=list, blank=True)
    r_reg_pmcid_list = models.JSONField(default=list, blank=True)
    f_inv_pmcid_list = models.JSONField(default=list, blank=True)
    r_inv_pmcid_list = models.JSONField(default=list, blank=True)

    # Adding this one back for the shared citations feature
    pair_shared_pmcid_list = models.JSONField(default=list, blank=True)


    f_evalue = models.FloatField()
    r_evalue = models.FloatField()
    f_occurrence_count = models.IntegerField()
    r_occurrence_count = models.IntegerField()
    f_total_citations = models.IntegerField()
    r_total_citations = models.IntegerField()
    f_pmcid_count = models.IntegerField()
    r_pmcid_count = models.IntegerField()
    f_Tm_C = models.FloatField()
    r_Tm_C = models.FloatField()
    f_GC_pct = models.FloatField()
    r_GC_pct = models.FloatField()
    f_match_start = models.IntegerField()
    r_match_start = models.IntegerField()
    f_match_end = models.IntegerField()
    r_match_end = models.IntegerField()
    f_orientation = models.CharField(max_length=8)
    r_orientation = models.CharField(max_length=8)
    f_self_comp = models.FloatField()
    r_self_comp = models.FloatField()
    pair_comp = models.FloatField()
    evidence_score = models.FloatField()
    biophysics_score = models.FloatField()
    synergy_score = models.FloatField()
    pickr_score = models.FloatField()

    f_reg_pmcid_count = models.IntegerField(default=0)
    r_reg_pmcid_count = models.IntegerField(default=0)
    f_inv_pmcid_count = models.IntegerField(default=0)
    r_inv_pmcid_count = models.IntegerField(default=0)
    pair_shared_pmcid_count = models.IntegerField(default=0)

    class Meta:
        # Update unique_together to include species
        unique_together = (('species', 'gene', 'f_sequence', 'r_sequence'),)
        ordering = ('-pickr_score',)
