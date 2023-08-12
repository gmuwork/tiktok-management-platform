import datetime
import typing

from tiktok_manager import enums, utils
from tiktok_manager.integrations.clients.tiktok import (
    constants as tiktok_client_constants,
)
from tiktok_manager.integrations.clients.tiktok import enums as tiktok_client_enums
from tiktok_manager.integrations.clients.tiktok import (
    exceptions as tiktok_client_exceptions,
)
from tiktok_manager.integrations.clients.tiktok import schemas as tiktok_client_schemas
from tiktok_manager.integrations.gateways.tiktok import client as tiktok_api_client
from tiktok_manager.integrations.gateways.tiktok import (
    exceptions as tiktok_api_client_exceptions,
)


class TiktokClient(object):
    def __init__(self, user_access_token: str) -> None:
        self._user_access_token = user_access_token
        self._rest_api_client = None

    def get_rest_api_client(self) -> tiktok_api_client.TikTokApiClient:
        if not self._rest_api_client:
            self._rest_api_client = tiktok_api_client.TikTokApiClient(
                user_access_token=self._user_access_token
            )

        return self._rest_api_client

    def get_account_ids(self, app_id: str, secret: str) -> typing.List[str]:
        try:
            response = self.get_rest_api_client().get_ad_accounts(
                app_id=app_id, secret=secret
            )
        except tiktok_api_client_exceptions.TikTokAPIClientError as e:
            raise tiktok_client_exceptions.TiktokClientProviderError(
                "Unable to fetch account ids through provider (user_access_token={}, app_id={}). Error: {}".format(
                    self._user_access_token,
                    app_id,
                    utils.get_exception_message(exception=e),
                )
            )

        validated_data = utils.validate_marshmallow_schema(
            data=response, schema=tiktok_client_schemas.AdAccounts()
        )
        if not validated_data:
            raise tiktok_client_exceptions.ResponseDataNotValidError(
                "Account data fetched from provider (user_access_token={}, app_id={}, response_data={}) is not valid".format(
                    self._user_access_token, app_id, response
                )
            )

        return [data["advertiser_id"] for data in validated_data["ad_accounts"]]

    def get_account_campaigns_details(
        self, advertiser_id: str
    ) -> typing.List[typing.Dict]:
        try:
            response = self.get_rest_api_client().get_advertiser_campaigns(
                advertiser_id=advertiser_id,
                fields=tiktok_client_constants.TIKTOK_RESOURCE_DETAILS_FIELDS[
                    enums.ResourceType.CAMPAIGN
                ],
            )
        except tiktok_api_client_exceptions.TikTokAPIClientError as e:
            raise tiktok_client_exceptions.TiktokClientProviderError(
                "Unable to fetch campaign details (user_access_token={}, advertiser_id={}) through provider. Error: {}".format(
                    self._user_access_token,
                    advertiser_id,
                    utils.get_exception_message(exception=e),
                )
            )

        validated_data = utils.validate_marshmallow_schema(
            data=response, schema=tiktok_client_schemas.CampaignsDetails()
        )
        if not validated_data:
            raise tiktok_client_exceptions.ResponseDataNotValidError(
                "Campaign details data fetched from provider (user_access_token={}, advertiser_id={}, response_data={}) is not valid".format(
                    self._user_access_token, advertiser_id, response
                )
            )

        return validated_data["campaigns_details"]

    def get_account_adgroups_details(
        self, advertiser_id: str
    ) -> typing.List[typing.Dict]:
        try:
            response = self.get_rest_api_client().get_advertiser_adgroups(
                advertiser_id=advertiser_id,
                fields=tiktok_client_constants.TIKTOK_RESOURCE_DETAILS_FIELDS[
                    enums.ResourceType.AD_GROUP
                ],
            )
        except tiktok_api_client_exceptions.TikTokAPIClientError as e:
            raise tiktok_client_exceptions.TiktokClientProviderError(
                "Unable to fetch adgroup details (user_access_token={}, advertiser_id={}) through provider. Error: {}".format(
                    self._user_access_token,
                    advertiser_id,
                    utils.get_exception_message(exception=e),
                )
            )

        validated_data = utils.validate_marshmallow_schema(
            data=response, schema=tiktok_client_schemas.AdGroupsDetails()
        )
        if not validated_data:
            raise tiktok_client_exceptions.ResponseDataNotValidError(
                "Adgroup details data fetched from provider (user_access_token={}, advertiser_id={}, response_data={}) is not valid".format(
                    self._user_access_token, advertiser_id, response
                )
            )

        return validated_data["adgroups_details"]

    def get_account_ads_details(self, advertiser_id: str) -> typing.List[typing.Dict]:
        try:
            response = self.get_rest_api_client().get_advertiser_ads(
                advertiser_id=advertiser_id,
                fields=tiktok_client_constants.TIKTOK_RESOURCE_DETAILS_FIELDS[
                    enums.ResourceType.AD
                ],
            )
        except tiktok_api_client_exceptions.TikTokAPIClientError as e:
            raise tiktok_client_exceptions.TiktokClientProviderError(
                "Unable to fetch ad details (user_access_token={}, advertiser_id={}) through provider. Error: {}".format(
                    self._user_access_token,
                    advertiser_id,
                    utils.get_exception_message(exception=e),
                )
            )

        validated_data = utils.validate_marshmallow_schema(
            data=response, schema=tiktok_client_schemas.AdsDetails()
        )
        if not validated_data:
            raise tiktok_client_exceptions.ResponseDataNotValidError(
                "Ad details data fetched from provider (user_access_token={}, advertiser_id={}, response_data={}) is not valid".format(
                    self._user_access_token, advertiser_id, response
                )
            )

        return validated_data["ads_details"]

    def create_ads(
        self, advertiser_id: str, adgroup_id: str, ad_details: typing.Dict
    ) -> typing.List[str]:
        ad_details["advertiser_id"] = advertiser_id
        ad_details["adgroup_id"] = adgroup_id
        validated_ad_details = utils.validate_marshmallow_schema(
            data=ad_details, schema=tiktok_client_schemas.AdCreate()
        )
        if not validated_ad_details:
            raise tiktok_client_exceptions.ResponseDataNotValidError(
                "Failed to validate ad details (user_access_token={}. advertiser_id={}, adgroup_id={} ad_details={})".format(
                    self._user_access_token, advertiser_id, adgroup_id, ad_details
                )
            )

        try:
            created_ad = self.get_rest_api_client().create_ads(
                ad_params=validated_ad_details
            )
        except tiktok_api_client_exceptions.TikTokAPIClientError as e:
            raise tiktok_client_exceptions.TiktokClientProviderError(
                "Unable to create ads (user_access_token={}, advertiser_id={}, adgroup_id={}, ad_details={}). Error: {}".format(
                    self._user_access_token,
                    advertiser_id,
                    adgroup_id,
                    validated_ad_details,
                    utils.get_exception_message(exception=e),
                )
            )

        return created_ad["ad_ids"]

    def update_ads(
        self, advertiser_id: str, adgroup_id: str, ad_details: typing.Dict
    ) -> bool:
        ad_details.update({"advertiser_id": advertiser_id, "adgroup_id": adgroup_id})
        validated_ad_details = utils.validate_marshmallow_schema(
            data=ad_details, schema=tiktok_client_schemas.AdUpdate()
        )
        if not validated_ad_details:
            raise tiktok_client_exceptions.ResponseDataNotValidError(
                "Failed to validate ad details (user_access_token={}. advertiser_id={}, adgroup_id={}, ad_details={})".format(
                    self._user_access_token,
                    advertiser_id,
                    adgroup_id,
                    ad_details,
                )
            )

        try:
            updated_ads = self.get_rest_api_client().update_ads(
                ad_params=validated_ad_details
            )
        except tiktok_api_client_exceptions.TikTokAPIClientError as e:
            raise tiktok_client_exceptions.TiktokClientProviderError(
                "Unable to update ad (user_access_token={}, advertiser_id={}, adgroup_id={}, ad_details={}). Error: {}".format(
                    self._user_access_token,
                    advertiser_id,
                    adgroup_id,
                    validated_ad_details,
                    utils.get_exception_message(exception=e),
                )
            )

        return bool(updated_ads)

    def update_ads_status(
        self, advertiser_id: str, ads_status_details: typing.Dict
    ) -> bool:
        ads_status_details["advertiser_id"] = advertiser_id
        validated_ads_status_details = utils.validate_marshmallow_schema(
            data=ads_status_details, schema=tiktok_client_schemas.AdStatusUpdate()
        )
        if not validated_ads_status_details:
            raise tiktok_client_exceptions.ResponseDataNotValidError(
                "Failed to validate ads status details (user_access_token={}. advertiser_id={}, ads_status_details={})".format(
                    self._user_access_token, advertiser_id, ads_status_details
                )
            )

        try:
            updated_ads = self.get_rest_api_client().update_ads_status(
                ads_status_params=validated_ads_status_details
            )
        except tiktok_api_client_exceptions.TikTokAPIClientError as e:
            raise tiktok_client_exceptions.TiktokClientProviderError(
                "Unable to update ads status details (user_access_token={}, advertiser_id={}, ads_status_details={}). Error: {}".format(
                    self._user_access_token,
                    advertiser_id,
                    validated_ads_status_details,
                    utils.get_exception_message(exception=e),
                )
            )

        return bool(updated_ads["ad_ids"])

    def create_campaign(self, advertiser_id: str, campaign_details: typing.Dict) -> str:
        campaign_details["advertiser_id"] = advertiser_id
        validated_campaign_details = utils.validate_marshmallow_schema(
            data=campaign_details, schema=tiktok_client_schemas.CampaignCreate()
        )
        if not validated_campaign_details:
            raise tiktok_client_exceptions.ResponseDataNotValidError(
                "Failed to validate campaign details (user_access_token={}. advertiser_id={}, campaign_details={})".format(
                    self._user_access_token, advertiser_id, campaign_details
                )
            )

        try:
            created_campaign = self.get_rest_api_client().create_campaign(
                campaign_params=validated_campaign_details
            )
        except tiktok_api_client_exceptions.TikTokAPIClientError as e:
            raise tiktok_client_exceptions.TiktokClientProviderError(
                "Unable to create campaign (user_access_token={}, advertiser_id={}, campaign_details={}). Error: {}".format(
                    self._user_access_token,
                    advertiser_id,
                    validated_campaign_details,
                    utils.get_exception_message(exception=e),
                )
            )

        return created_campaign["campaign_id"]

    def update_campaign(
        self, advertiser_id: str, campaign_id: str, campaign_details: typing.Dict
    ) -> bool:
        campaign_details.update(
            {"advertiser_id": advertiser_id, "campaign_id": campaign_id}
        )
        validated_campaign_details = utils.validate_marshmallow_schema(
            data=campaign_details, schema=tiktok_client_schemas.CampaignUpdate()
        )
        if not validated_campaign_details:
            raise tiktok_client_exceptions.ResponseDataNotValidError(
                "Failed to validate campaign details (user_access_token={}. advertiser_id={}, campaign_id={}, campaign_details={})".format(
                    self._user_access_token,
                    advertiser_id,
                    campaign_id,
                    campaign_details,
                )
            )

        try:
            updated_campaign = self.get_rest_api_client().update_campaign(
                campaign_params=validated_campaign_details
            )
        except tiktok_api_client_exceptions.TikTokAPIClientError as e:
            raise tiktok_client_exceptions.TiktokClientProviderError(
                "Unable to update campaign (user_access_token={}, advertiser_id={}, campaign_id={}, campaign_details={}). Error: {}".format(
                    self._user_access_token,
                    advertiser_id,
                    campaign_id,
                    validated_campaign_details,
                    utils.get_exception_message(exception=e),
                )
            )

        return bool(updated_campaign)

    def create_adgroup(self, advertiser_id: str, adgroup_details: typing.Dict) -> str:
        adgroup_details["advertiser_id"] = advertiser_id
        validated_adgroup_details = utils.validate_marshmallow_schema(
            data=adgroup_details, schema=tiktok_client_schemas.AdGroupCreate()
        )
        if not validated_adgroup_details:
            raise tiktok_client_exceptions.ResponseDataNotValidError(
                "Failed to validate adgroup details (user_access_token={}. advertiser_id={}, adgroup_details={})".format(
                    self._user_access_token, advertiser_id, adgroup_details
                )
            )

        try:
            created_adgroup = self.get_rest_api_client().create_adgroup(
                adgroup_params=validated_adgroup_details
            )
        except tiktok_api_client_exceptions.TikTokAPIClientError as e:
            raise tiktok_client_exceptions.TiktokClientProviderError(
                "Unable to create adgroup (user_access_token={}, advertiser_id={}, adgroup_details={}). Error: {}".format(
                    self._user_access_token,
                    advertiser_id,
                    validated_adgroup_details,
                    utils.get_exception_message(exception=e),
                )
            )

        return created_adgroup["adgroup_id"]

    def update_adgroup(
        self, advertiser_id: str, adgroup_id: str, adgroup_details: typing.Dict
    ) -> bool:
        adgroup_details.update(
            {"advertiser_id": advertiser_id, "adgroup_id": adgroup_id}
        )
        validated_adgroup_details = utils.validate_marshmallow_schema(
            data=adgroup_details, schema=tiktok_client_schemas.AdGroupUpdate()
        )
        if not validated_adgroup_details:
            raise tiktok_client_exceptions.ResponseDataNotValidError(
                "Failed to validate adgroup details (user_access_token={}. advertiser_id={}, adgroup_id={}, adgroup_details={})".format(
                    self._user_access_token,
                    advertiser_id,
                    adgroup_id,
                    adgroup_details,
                )
            )

        try:
            updated_adgroup = self.get_rest_api_client().update_adgroup(
                adgroup_params=validated_adgroup_details
            )
        except tiktok_api_client_exceptions.TikTokAPIClientError as e:
            raise tiktok_client_exceptions.TiktokClientProviderError(
                "Unable to update adgroup (user_access_token={}, advertiser_id={}, adgroup_id={}, adgroup_details={}). Error: {}".format(
                    self._user_access_token,
                    advertiser_id,
                    adgroup_id,
                    validated_adgroup_details,
                    utils.get_exception_message(exception=e),
                )
            )

        return bool(updated_adgroup)

    def create_image(self, advertiser_id: str, image_details: typing.Dict) -> str:
        image_details["advertiser_id"] = advertiser_id
        validated_image_details = utils.validate_marshmallow_schema(
            data=image_details, schema=tiktok_client_schemas.ImageCreate()
        )
        if not validated_image_details:
            raise tiktok_client_exceptions.ResponseDataNotValidError(
                "Failed to validate image details (user_access_token={}. advertiser_id={}, image_details={})".format(
                    self._user_access_token, advertiser_id, image_details
                )
            )

        try:
            created_image = self.get_rest_api_client().upload_image(
                image_params=validated_image_details
            )
        except tiktok_api_client_exceptions.TikTokAPIClientError as e:
            raise tiktok_client_exceptions.TiktokClientProviderError(
                "Unable to create image (user_access_token={}, advertiser_id={}, image_details={}). Error: {}".format(
                    self._user_access_token,
                    advertiser_id,
                    validated_image_details,
                    utils.get_exception_message(exception=e),
                )
            )

        return created_image["image_id"]

    def update_image_name(
        self, advertiser_id: str, image_id: str, image_name: str
    ) -> bool:
        image_details = {
            "advertiser_id": advertiser_id,
            "image_id": image_id,
            "file_name": image_name,
        }

        validated_image_details = utils.validate_marshmallow_schema(
            data=image_details, schema=tiktok_client_schemas.ImageUpdate()
        )
        if not validated_image_details:
            raise tiktok_client_exceptions.ResponseDataNotValidError(
                "Failed to validate image details (user_access_token={}. advertiser_id={}, image_id={}, image_name={})".format(
                    self._user_access_token,
                    advertiser_id,
                    image_id,
                    image_name,
                )
            )

        try:
            updated_image = self.get_rest_api_client().update_image_name(
                image_params=validated_image_details
            )
        except tiktok_api_client_exceptions.TikTokAPIClientError as e:
            raise tiktok_client_exceptions.TiktokClientProviderError(
                "Unable to update image (user_access_token={}, advertiser_id={}, image_id={}, image_name={}). Error: {}".format(
                    self._user_access_token,
                    advertiser_id,
                    image_id,
                    image_name,
                    utils.get_exception_message(exception=e),
                )
            )

        return bool(updated_image)

    def get_images_info(
        self, advertiser_id: str, image_ids: typing.List[str]
    ) -> typing.List[typing.Dict]:
        image_params = {
            "advertiser_id": advertiser_id,
            "image_ids": image_ids,
        }

        validated_image_params = utils.validate_marshmallow_schema(
            data=image_params, schema=tiktok_client_schemas.ImageInfoParams()
        )

        if not validated_image_params:
            raise tiktok_client_exceptions.ResponseDataNotValidError(
                "Failed to validate image details (user_access_token={}. advertiser_id={}, image_ids={})".format(
                    self._user_access_token,
                    advertiser_id,
                    image_ids,
                )
            )

        try:
            images_info_details = self.get_rest_api_client().get_images_info(
                image_params=validated_image_params
            )
        except tiktok_api_client_exceptions.TikTokAPIClientError as e:
            raise tiktok_client_exceptions.TiktokClientProviderError(
                "Unable to get images info details (user_access_token={}, advertiser_id={}, image_ids={}). Error: {}".format(
                    self._user_access_token,
                    advertiser_id,
                    image_ids,
                    utils.get_exception_message(exception=e),
                )
            )

        validated_image_details = utils.validate_marshmallow_schema(
            data=images_info_details,
            schema=tiktok_client_schemas.ImageDetailsResponse(),
        )
        if not validated_image_details:
            raise tiktok_client_exceptions.ResponseDataNotValidError(
                "Failed to validate image details (user_access_token={}. advertiser_id={}, image_ids={})".format(
                    self._user_access_token,
                    advertiser_id,
                    image_ids,
                )
            )

        return validated_image_details["image_details"]

    def create_video(self, advertiser_id: str, video_details: typing.Dict) -> str:
        video_details["advertiser_id"] = advertiser_id
        validated_video_params = utils.validate_marshmallow_schema(
            data=video_details, schema=tiktok_client_schemas.VideoCreate()
        )
        if not validated_video_params:
            raise tiktok_client_exceptions.ResponseDataNotValidError(
                "Failed to validate video details (user_access_token={}. advertiser_id={}, video_details={})".format(
                    self._user_access_token, advertiser_id, video_details
                )
            )

        try:
            created_video = self.get_rest_api_client().upload_video(
                video_params=validated_video_params
            )
        except tiktok_api_client_exceptions.TikTokAPIClientError as e:
            raise tiktok_client_exceptions.TiktokClientProviderError(
                "Unable to create video (user_access_token={}, advertiser_id={}, video_details={}). Error: {}".format(
                    self._user_access_token,
                    advertiser_id,
                    validated_video_params,
                    utils.get_exception_message(exception=e),
                )
            )

        return created_video["video_id"]

    def update_video_name(
        self, advertiser_id: str, video_id: str, video_name: str
    ) -> bool:
        video_details = {
            "advertiser_id": advertiser_id,
            "video_id": video_id,
            "file_name": video_name,
        }

        validated_video_params = utils.validate_marshmallow_schema(
            data=video_details, schema=tiktok_client_schemas.VideoUpdate()
        )
        if not validated_video_params:
            raise tiktok_client_exceptions.ResponseDataNotValidError(
                "Failed to validate video details (user_access_token={}. advertiser_id={}, video_id={}, video_name={})".format(
                    self._user_access_token,
                    advertiser_id,
                    video_id,
                    video_name,
                )
            )

        try:
            updated_video = self.get_rest_api_client().update_video_name(
                video_params=validated_video_params
            )
        except tiktok_api_client_exceptions.TikTokAPIClientError as e:
            raise tiktok_client_exceptions.TiktokClientProviderError(
                "Unable to update video (user_access_token={}, advertiser_id={}, video_id={}, video_name={}). Error: {}".format(
                    self._user_access_token,
                    advertiser_id,
                    video_id,
                    video_name,
                    utils.get_exception_message(exception=e),
                )
            )

        return bool(updated_video)

    def get_videos_info(
        self, advertiser_id: str, video_ids: typing.List[str]
    ) -> typing.List[typing.Dict]:
        video_params = {
            "advertiser_id": advertiser_id,
            "video_ids": video_ids,
        }

        validated_video_params = utils.validate_marshmallow_schema(
            data=video_params, schema=tiktok_client_schemas.VideoInfoParams()
        )
        if not validated_video_params:
            raise tiktok_client_exceptions.ResponseDataNotValidError(
                "Failed to validate video info params (user_access_token={}. advertiser_id={}, video_ids={})".format(
                    self._user_access_token,
                    advertiser_id,
                    video_ids,
                )
            )

        try:
            video_details = self.get_rest_api_client().get_videos_info(
                video_params=validated_video_params
            )
        except tiktok_api_client_exceptions.TikTokAPIClientError as e:
            raise tiktok_client_exceptions.TiktokClientProviderError(
                "Unable to get video details (user_access_token={}, advertiser_id={}, video_ids={}). Error: {}".format(
                    self._user_access_token,
                    advertiser_id,
                    video_ids,
                    utils.get_exception_message(exception=e),
                )
            )

        validated_video_details = utils.validate_marshmallow_schema(
            data=video_details, schema=tiktok_client_schemas.VideoDetailsResponse()
        )
        if not validated_video_details:
            raise tiktok_client_exceptions.ResponseDataNotValidError(
                "Failed to validate video details (user_access_token={}. advertiser_id={}, video_ids={})".format(
                    self._user_access_token,
                    advertiser_id,
                    video_ids,
                )
            )

        return validated_video_details["video_details"]

    def get_insights(
        self,
        advertiser_id: str,
        resource_type: enums.ResourceType,
        from_datetime: datetime.datetime,
        to_datetime: datetime.datetime,
    ) -> typing.List:
        try:
            insights_report = self.get_rest_api_client().get_insights_report(
                advertiser_id=advertiser_id,
                service_type=tiktok_client_enums.ServiceType.AUCTION.value,
                report_type=tiktok_client_enums.ReportType.BASIC.value,
                data_level=tiktok_client_enums.DataLevel.from_service_and_resource_type(
                    service_type=tiktok_client_enums.ServiceType.AUCTION,
                    resource_type=resource_type,
                ).value,
                dimensions=tiktok_client_constants.TIKTOK_INSIGHTS_DETAILS_FIELDS[
                    resource_type
                ]["dimensions"],
                metrics=tiktok_client_constants.TIKTOK_INSIGHTS_DETAILS_FIELDS[
                    resource_type
                ]["metrics"],
                from_datetime=from_datetime,
                to_datetime=to_datetime,
            )
        except tiktok_api_client_exceptions.TikTokAPIClientError as e:
            raise tiktok_client_exceptions.TiktokClientError(
                "Unable to get insights report (user_access_token={}, advertiser_id={}, resource_type={}, from_datetime={}, to_datetime={}). Error: {}".format(
                    self._user_access_token,
                    advertiser_id,
                    resource_type.name,
                    from_datetime,
                    to_datetime,
                    utils.get_exception_message(exception=e),
                )
            )

        validated_insights_report = utils.validate_marshmallow_schema(
            data=insights_report,
            schema=tiktok_client_constants.TIKTOK_INSIGHTS_SCHEMAS[resource_type](
                advertiser_id=advertiser_id
            ),
        )
        if not validated_insights_report:
            raise tiktok_client_exceptions.ResponseDataNotValidError(
                "Resource insights data fetched from provider (user_access_token={}, advertiser_id={}, resource_type={}, from_datetime={}, to_datetime={}, insights_report={}) is not valid".format(
                    self._user_access_token,
                    advertiser_id,
                    resource_type.name,
                    from_datetime,
                    to_datetime,
                    insights_report,
                )
            )

        return validated_insights_report["resource_insights"]
