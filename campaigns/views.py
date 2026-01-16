from django.shortcuts import render
from .models import (
    Platform,
    Brand,
    Niche,
    Campaign,
    Influencer,
    CampaignInfluencer,
    InfluencerPlatform,
)
from django.db.models import Count, Sum, Q

# Create your views here.


def index(request):
    total_brands = Brand.objects.count()
    active_campaigns = CampaignInfluencer.objects.count()
    # Brand Details
    brands = Brand.objects.annotate(campaign_count=Count("campaigns"))
    total_brands_spent = Campaign.objects.aggregate(
        total=Sum(
            "contracts__fee", filter=Q(contracts__status__in=["active", "completed"])
        )
    )["total"]
    brand_details = []
    for brand in brands:
        brands = {
            "name": brand.name,
            "budget": brand.budget,
            "campaign_count": brand.campaign_count,
            "total_spend": brand.campaigns.aggregate(
                total=Sum(
                    "contracts__fee",
                    filter=Q(contracts__status__in=["active", "completed"]),
                )
            )["total"],
        }
        brand_details.append(brands)

    return render(
        request,
        "campaigns/index.html",
        {
            "total_brands": total_brands,
            "active_campaigns": active_campaigns,
            "brand_details": brand_details,
            "total_brands_spent": total_brands_spent,
        },
    )


# Brand Overview


def brand_dashboard(request, brand):
    brand = Brand.objects.get(name=brand)

    total_budget = brand.budget
    total_spent = brand.campaigns.aggregate(
        total=Sum(
            "contracts__fee", filter=Q(contracts__status__in=["active", "completed"])
        )
    )["total"]
    balance_amount = total_budget - (total_spent or 0)
    total_campaigns = brand.campaigns.count()  # total number of campaigns
    total_influencers = brand.campaigns.aggregate(
        total=Count(
            "contracts__influencer_platform"  # total influencers associated with the brand
        )
    )["total"]
    total_platforms = brand.campaigns.aggregate(
        total=Count(
            "contracts__influencer_platform__platform",
            distinct=True,  # total platforms associated with this brand
        )
    )["total"]
    campaigns = brand.campaigns.annotate(
        influencer_count=Count(
            "contracts__influencer_platform__influencer",
            distint=True,  # Count Influencers associated with each campaign
        ),
        total_spent=Sum(
            "contracts__fee",
            filter=Q(
                contracts__status__in=[
                    "active",
                    "completed",
                ]  # total amount spent for each campaign
            ),
        ),
    )

    return render(
        request,
        "campaigns/brand_dashboard.html",
        {
            "total_budget": total_budget,
            "total_spent": total_spent,
            "balance_amount": balance_amount,
            "total_campaigns": total_campaigns,
            "brand": brand.name,
            "total_influencers": total_influencers,
            "total_platforms": total_platforms,
            "campaigns": campaigns,
        },
    )


# Campaign Dashboard
def campaign_dashboard(request, campaign):
    campaign = Campaign.objects.get(name=campaign)
    brand_name = campaign.brand.name
    proposed_contracts = campaign.contracts.filter(status="proposed")
    active_contracts = campaign.contracts.filter(status="active")
    completed_contracts = campaign.contracts.filter(status="completed")

    campaign_name = campaign.name

    influencer_count = campaign.contracts.aggregate(
        total=Count(
            "influencer_platform__influencer"
        )  # Total Influencers associated with each campaign
    )["total"]
    total_spent = campaign.contracts.aggregate(
        total=Sum(
            "fee", filter=Q(status__in=["active", "completed"])
        )  # total amount spend
    )["total"]

    return render(
        request,
        "campaigns/campaign_dashboard.html",
        {
            "influencer_count": influencer_count,
            "total_spent": total_spent,
            "campaign_name": campaign_name,
            "proposed_contracts": proposed_contracts,
            "active_contracts": active_contracts,
            "completed_contracts": completed_contracts,
            "brand_name": brand_name,
        },
    )
