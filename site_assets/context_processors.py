from .models import SiteAsset

def site_assets(request):
    assets = SiteAsset.objects.all()
    
    platform_logo = assets.filter(asset_type=SiteAsset.AssetType.HEADER_LOGO_PLATFORM).first()
    gov_logo = assets.filter(asset_type=SiteAsset.AssetType.HEADER_LOGO_GOV).first()
    partner_logos = assets.filter(asset_type=SiteAsset.AssetType.PARTNER_LOGO)
    
    return {
        'platform_logo': platform_logo,
        'gov_logo': gov_logo,
        'partner_logos': partner_logos,
    }
