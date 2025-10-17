from django.db import models
from django.core.cache import cache
class informationSite(models.Model):
    nameE = models.CharField(max_length=100)
    nameF = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="images/logo/")
    text = models.TextField()    
    message = models.TextField(default="")
    class Meta:
        verbose_name = "اطلاعات سایت"
        verbose_name_plural = "اطلاعات سایت"

    def __str__(self):
        return self.nameF
    @classmethod
    def get_cached(cls):
        return cache.get_or_set('site_information', lambda: cls.objects.get(pk=1), 3600)
