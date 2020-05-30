from rest_framework import serializers
from quickstart.affiliate.affiliate_model import Affiliate


class AffiliateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Affiliate
        fields = [
            'id',
            'website',
            'photo',
            'ready_to_link',
            'ordernum',
            'lat',
            'lon',
            'city',
            'name_search',
            'photo_version',
            'zip',
            'country_short_code',
            'bad_standing',
            'effective_date',
            'status',
            'address',
            'active',
            'state_code',
            'show_on_map',
            'kids',
            'name',
            'country',
            'org_type',
            'aid',
            'full_state',
            'continent'
        ]
