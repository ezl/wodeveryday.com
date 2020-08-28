from django.db import models


class Gym(models.Model):
    website = models.TextField(blank=True, null=True)
    photo = models.TextField(blank=True, null=True)
    ready_to_link = models.TextField(blank=True, null=True)
    ordernum = models.TextField(blank=True, null=True)
    lat = models.TextField(blank=True, null=True)
    lon = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    name_search = models.TextField(blank=True, null=True)
    photo_version = models.TextField(blank=True, null=True)
    zip = models.TextField(blank=True, null=True)
    country_short_code = models.TextField(blank=True, null=True)
    bad_standing = models.TextField(blank=True, null=True)
    effective_date = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    active = models.TextField(blank=True, null=True)
    state_code = models.TextField(blank=True, null=True)
    show_on_map = models.TextField(blank=True, null=True)
    kids = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    org_type = models.TextField(blank=True, null=True)
    aid = models.TextField(blank=True, null=True)
    full_state = models.TextField(blank=True, null=True)
    continent = models.TextField(blank=True, null=True)
    name_slug = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'core_gym'
