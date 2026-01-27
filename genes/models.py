from django.db import models

# Create your models here.
class Gene(models.Model):
    hgnc_id = models.CharField(max_length=255, unique=True)
    symbol = models.CharField(max_length=255, db_index=True, unique=True)
    name = models.TextField(null=True, blank=True)
    locus_group = models.CharField(max_length=255, null=True, blank=True)
    locus_type = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    alias_symbol = models.TextField(null=True, blank=True)
    prev_symbol = models.TextField(null=True, blank=True)
    gene_group = models.TextField(null=True, blank=True)
    entrez_id = models.CharField(max_length=255, null=True, blank=True)
    ensembl_gene_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.symbol} ({self.name})"