from django.db import models
from datetime import date

class Licitacao(models.Model):
    orgao = models.CharField(max_length=300)
    uasg_orgao = models.PositiveIntegerField()
    no_arp = models.CharField(max_length=300)
    data = models.DateField(default=date.today)

    def __str__(self):
        return self.orgao + " - " + self.no_arp

    class Meta:
        ordering = ['-data']
