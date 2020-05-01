from django.db import models


class Affiliate(models.Model):
    website = models.TextField(blank=True)
    photo = models.TextField(blank=True)
    ready_to_link = models.TextField(blank=True)
    ordernum = models.TextField(blank=True)
    lat = models.TextField(blank=True)
    lon = models.TextField(blank=True)
    city = models.TextField(blank=True)
    name_search = models.TextField(blank=True)
    photo_version = models.TextField(blank=True)
    zip = models.TextField(blank=True)
    country_short_code = models.TextField(blank=True)
    bad_standing = models.TextField(blank=True)
    effective_date = models.TextField(blank=True)
    status = models.TextField(blank=True)
    address = models.TextField(blank=True)
    active = models.TextField(blank=True)
    state_code = models.TextField(blank=True)
    show_on_map = models.TextField(blank=True)
    kids = models.TextField(blank=True)
    name = models.TextField(blank=True)
    country = models.TextField(blank=True)
    org_type = models.TextField(blank=True)
    aid = models.TextField(blank=True)
    full_state = models.TextField(blank=True)

    def __str__(self):
        return self.name
