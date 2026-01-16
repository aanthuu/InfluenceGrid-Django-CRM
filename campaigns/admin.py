from django.contrib import admin
from .models import (
    Platform,
    Brand,
    Niche,
    Campaign,
    Influencer,
    CampaignInfluencer,
    InfluencerPlatform,
)

# Register your models here.
admin.site.register(Brand)
admin.site.register(Platform)
admin.site.register(Niche)
admin.site.register(Campaign)
admin.site.register(Influencer)
admin.site.register(CampaignInfluencer)
admin.site.register(InfluencerPlatform)
