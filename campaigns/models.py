from django.db import models


# Create your models here.


# Brand Class
class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.name


# Niches
class Niche(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# Platforms
class Platform(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# Influencers
class Influencer(models.Model):
    name = models.CharField(max_length=255)
    niches = models.ManyToManyField(Niche, related_name="influencers")

    def __str__(self):
        return self.name


# InfluencerPlatform
class InfluencerPlatform(models.Model):
    influencer = models.ForeignKey(
        Influencer, on_delete=models.CASCADE, related_name="platform_profiles"
    )
    platform = models.ForeignKey(
        Platform, on_delete=models.Case, related_name="influencer_profiles"
    )
    followers = models.PositiveBigIntegerField()

    class Meta:
        unique_together = ("influencer", "platform")

    def __str__(self):
        return f"{self.influencer.name} on {self.platform.name}"


# Campaign
class Campaign(models.Model):
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="campaigns")
    niches = models.ManyToManyField(Niche, related_name="campaigns")
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.brand.name})"


# Campaign Influencer
class CampaignInfluencer(models.Model):
    STATUS_CHOICES = [
        ("proposed", "Proposed"),
        ("active", "Active"),
        ("completed", "Completed"),
    ]
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name="contracts"
    )
    influencer_platform = models.ForeignKey(
        InfluencerPlatform, on_delete=models.CASCADE, related_name="contracts"
    )
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="proposed")
    deliverables = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("campaign", "influencer_platform")

    def __str__(self):
        return f"{self.campaign.name} × {self.influencer_platform}"
