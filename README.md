# Tiktok Ads Manager

## Description 
Tiktok Ads Manager serves as the extended SDK around TikTok API with additional services to import resource details and insight reports to AWS S3 storage.
The Ads Manager consists of services divided into three groups:
- **Manager** - in charge of obtaining resource details and insight reports and saving those to AWS S3.
- **Actions**  - in charge of creating and updating resources.
- **Ad assets**  - in charge of managing ad assets.

Services cover following resources:
- Campaigns
- AdGroups
- Ads
- Images
- Videos

## Setup

To install the package, add the following dependency to your requirements.txt file:
```bash
tiktok_manager @ file://<ABSOLUTE_PATH_TO_CODE>

# for example:
tiktok_manager @ file:///home/marko/code/gmuwork/tiktok_manager
```

To use the package just import it in your code:

```python
import tiktok_manager.services.importer as importer_services
import tiktok_manager.services.actions as action_services
import tiktok_manager.services.ad_assets as ad_assets_services
```

## Usage and description

The `importer` service contains all the functions to get the resource details and resource performance and save it to AWS S3.
Resource details functions:
```python
import tiktok_manager.services.importer as importer_services
# Campaigns documentation: https://ads.tiktok.com/marketing_api/docs?id=1739315828649986 
importer_services.get_campaigns(
    user_access_token='<TAG>',  # User access token.
    app_id='<TAG>',  # The App id applied by the developer. This is needed in order to fetch all advertiser ids. 
    secret='<TAG>',  # The private key of the developer's application. This is needed in order to fetch all advertiser ids.
    s3_path='<TAG>', # Path to S3 bucket where to save details.
)

# Ad Groups documentation: https://ads.tiktok.com/marketing_api/docs?id=1739314558673922 
importer_services.get_adgroups(
    user_access_token='<TAG>',  # User access token.
    app_id='<TAG>',  # The App id applied by the developer. This is needed in order to fetch all advertiser ids. 
    secret='<TAG>',  # The private key of the developer's application. This is needed in order to fetch all advertiser ids.
    s3_path='<TAG>', # Path to S3 bucket where to save details.
)

# Ads documentation: https://ads.tiktok.com/marketing_api/docs?id=1735735588640770 
importer_services.get_ads(
    user_access_token='<TAG>',  # User access token.
    app_id='<TAG>',  # The App id applied by the developer. This is needed in order to fetch all advertiser ids. 
    secret='<TAG>',  # The private key of the developer's application. This is needed in order to fetch all advertiser ids.
    s3_path='<TAG>', # Path to S3 bucket where to save details.
)
```

Insights report functions:

** All of the functions extract the insights for all available resources to which the corresponding TikTok app has access to  
```python
import tiktok_manager.services.importer as importer_services

importer_services.get_campaign_insights(
    user_access_token='<TAG>',# User access token.
    app_id='<TAG>',     # The App id applied by the developer. This is needed in order to fetch all advertiser ids. 
    secret='<TAG>',     # The private key of the developer's application. This is needed in order to fetch all advertiser ids.
    s3_path='<TAG>',    # Path to S3 bucket where to save insights.
    date_from='<TAG>',  # The time range from which the data should be included.
    date_to='<TAG>',    # The time range to which the data should be included.
)

importer_services.get_adgroup_insights(
    user_access_token='<TAG>',# User access token.
    app_id='<TAG>',     # The App id applied by the developer. This is needed in order to fetch all advertiser ids. 
    secret='<TAG>',     # The private key of the developer's application. This is needed in order to fetch all advertiser ids.
    s3_path='<TAG>',    # Path to S3 bucket where to save insights.
    date_from='<TAG>',  # The time range from which the data should be included.
    date_to='<TAG>',    # The time range to which the data should be included.
)

importer_services.get_ad_insights(
    user_access_token='<TAG>',# User access token.
    app_id='<TAG>',     # The App id applied by the developer. This is needed in order to fetch all advertiser ids. 
    secret='<TAG>',     # The private key of the developer's application. This is needed in order to fetch all advertiser ids.
    s3_path='<TAG>',    # Path to S3 bucket where to save insights.
    date_from='<TAG>',  # The time range from which the data should be included. 
    date_to='<TAG>',    # The time range to which the data should be included.
)
```

The `actions` service contains all the functions to create and update resources.
Create resource functions:
```python
import tiktok_manager.services.actions as action_services
action_services.add_campaign(
    user_access_token='<TAG>',  # User access token.
    advertiser_id='<TAG>',  # Advertiser id.
    campaign_details='<TAG>',  # Details of the campaign to be created - fields defined in https://ads.tiktok.com/marketing_api/docs?id=1739318962329602.
)

action_services.add_adgroup(
    user_access_token='<TAG>',  # User access token.
    advertiser_id='<TAG>',  # Advertiser id.
    adgroup_details='<TAG>',  # Details of the adgroup to be created - fields defined in https://ads.tiktok.com/marketing_api/docs?id=1739499616346114.
)

action_services.add_ads(
    user_access_token='<TAG>',  # User access token.
    advertiser_id='<TAG>',  # Advertiser id.
    adgroup_details='<TAG>',  # Details of the ads to be created - fields defined in https://ads.tiktok.com/marketing_api/docs?id=1739953377508354.
)
```

Update resource functions:
```python
import tiktok_manager.services.actions as action_services
action_services.update_campaign(
    user_access_token='<TAG>',  # User access token.
    advertiser_id='<TAG>',  # Advertiser id.
    campaign_id='<TAG>',  # Campaign id to be updated.
    campaign_details='<TAG>',  # Details of the campaign to be updated - fields defined in https://ads.tiktok.com/marketing_api/docs?id=1739318962329602.
)

action_services.update_adgroup(
    user_access_token='<TAG>',  # User access token
    advertiser_id='<TAG>',  # Advertiser id
    adgroup_id='<TAG>',  # Adgroup id to be updated  
    adgroup_details='<TAG>',  # Details of the adgroup to be updated - fields defined in https://ads.tiktok.com/marketing_api/docs?id=1739499616346114
)

action_services.update_ads(
    user_access_token='<TAG>',  # User access token.
    advertiser_id='<TAG>',  # Advertiser id.
    adgroup_id='<TAG>',  # Adgroup id to which ads belong .
    adgroup_details='<TAG>',  # Details of the ads to be created - fields defined in https://ads.tiktok.com/marketing_api/docs?id=1739953377508354.
)
```

The `ad_assets` service contains all the functions to manage (create/update/read) the ad assets.

```python
import tiktok_manager.services.ad_assets as ad_assets_services

ad_assets_services.add_image(
    user_access_token='<TAG>',  # User access token.
    advertiser_id='<TAG>',  # Advertiser id.
    image_details='<TAG>',
    # Details of the image to be created - fields defined in https://ads.tiktok.com/marketing_api/docs?id=1739067433456642.
)

ad_assets_services.update_image_name(
    user_access_token='<TAG>',  # User access token.
    advertiser_id='<TAG>',  # Advertiser id.
    image_id='<TAG>',  # ID of the image to be updated.
    image_name='<TAG>',  # Name of the image to be updated.
)

ad_assets_services.get_images_info(
    user_access_token='<TAG>',  # User access token.
    advertiser_id='<TAG>',  # Advertiser id.
    image_ids='<TAG>',  # Image ids for which to obtain image info.
)

ad_assets_services.add_video(
    user_access_token='<TAG>',  # User access token.
    advertiser_id='<TAG>',  # Advertiser id.
    video_details='<TAG>',  # Details of the video to be created - fields defined in https://ads.tiktok.com/marketing_api/docs?id=1737587322856449.
)

ad_assets_services.update_video_name(
    user_access_token='<TAG>',  # User access token.
    advertiser_id='<TAG>',  # Advertiser id.
    video_id='<TAG>',  # ID of the video to be updated.
    video_name='<TAG>',  # Name of the video to be updated.
)

ad_assets_services.get_videos_info(
    user_access_token='<TAG>',  # User access token.
    advertiser_id='<TAG>',  # Advertiser id.
    video_ids='<TAG>',  # Image ids for which to obtain image info.
)
```