import datetime
import logging
import typing

from tiktok_manager import enums, exceptions, utils
from tiktok_manager.integrations.clients.s3 import client as s3_client
from tiktok_manager.integrations.clients.s3 import exceptions as s3_client_exceptions
from tiktok_manager.integrations.clients.tiktok import client as tiktok_client
from tiktok_manager.integrations.clients.tiktok import (
    exceptions as tiktok_client_exceptions,
)

logger = logging.getLogger(__name__)


def get_account_ids(
    user_access_token: str, app_id: str, secret: str
) -> typing.List[str]:
    try:
        return tiktok_client.TiktokClient(
            user_access_token=user_access_token
        ).get_account_ids(app_id=app_id, secret=secret)
    except tiktok_client_exceptions.TiktokClientError as e:
        raise exceptions.ImporterException(utils.get_exception_message(exception=e))


def get_campaigns(
    user_access_token: str, app_id: str, secret: str, s3_path: str
) -> typing.Tuple[str, bool]:
    campaigns_details = []

    tiktok_integration_client = tiktok_client.TiktokClient(
        user_access_token=user_access_token
    )
    try:
        advertiser_ids = tiktok_integration_client.get_account_ids(
            app_id=app_id, secret=secret
        )
    except tiktok_client_exceptions.TiktokClientError as e:
        raise exceptions.ImporterException(utils.get_exception_message(exception=e))

    logger.warning("Fetched {} advertiser ids".format(len(advertiser_ids)))

    for advertiser_id in advertiser_ids:
        try:
            campaign_details = tiktok_integration_client.get_account_campaigns_details(
                advertiser_id=advertiser_id
            )
        except tiktok_client_exceptions.TiktokClientError as e:
            raise exceptions.ImporterException(utils.get_exception_message(exception=e))

        campaigns_details.extend(campaign_details)

    logger.warning("Fetched {} campaigns".format(len(campaigns_details)))

    try:
        uploaded_path = s3_client.TiktokS3Uploader(
            s3_path=s3_path
        ).upload_resource_details(
            resource_details=campaigns_details,
            resource_type=enums.ResourceType.CAMPAIGN,
            date_created=datetime.datetime.utcnow(),
        )
    except s3_client_exceptions.TiktokS3UploaderError as e:
        raise exceptions.ImporterException(utils.get_exception_message(exception=e))

    return uploaded_path, True


def get_adgroups(
    user_access_token: str, app_id: str, secret: str, s3_path: str
) -> typing.Tuple[str, bool]:
    adgroups_details = []

    tiktok_integration_client = tiktok_client.TiktokClient(
        user_access_token=user_access_token
    )
    try:
        advertiser_ids = tiktok_integration_client.get_account_ids(
            app_id=app_id, secret=secret
        )
    except tiktok_client_exceptions.TiktokClientError as e:
        raise exceptions.ImporterException(utils.get_exception_message(exception=e))

    logger.warning("Fetched {} advertiser ids".format(len(advertiser_ids)))

    for advertiser_id in advertiser_ids:
        try:
            adgroup_details = tiktok_integration_client.get_account_adgroups_details(
                advertiser_id=advertiser_id
            )
        except tiktok_client_exceptions.TiktokClientError as e:
            raise exceptions.ImporterException(utils.get_exception_message(exception=e))

        adgroups_details.extend(adgroup_details)

    logger.warning("Fetched {} adgroups".format(len(adgroups_details)))

    try:
        uploaded_path = s3_client.TiktokS3Uploader(
            s3_path=s3_path
        ).upload_resource_details(
            resource_details=adgroups_details,
            resource_type=enums.ResourceType.AD_GROUP,
            date_created=datetime.datetime.utcnow(),
        )
    except s3_client_exceptions.TiktokS3UploaderError as e:
        raise exceptions.ImporterException(utils.get_exception_message(exception=e))

    return uploaded_path, True


def get_ads(
    user_access_token: str, app_id: str, secret: str, s3_path: str
) -> typing.Tuple[str, bool]:
    ads_details = []

    tiktok_integration_client = tiktok_client.TiktokClient(
        user_access_token=user_access_token
    )
    try:
        advertiser_ids = tiktok_integration_client.get_account_ids(
            app_id=app_id, secret=secret
        )
    except tiktok_client_exceptions.TiktokClientError as e:
        raise exceptions.ImporterException(utils.get_exception_message(exception=e))

    logger.warning("Fetched {} advertiser ids".format(len(advertiser_ids)))

    for advertiser_id in advertiser_ids:
        try:
            ad_details = tiktok_integration_client.get_account_adgroups_details(
                advertiser_id=advertiser_id
            )
        except tiktok_client_exceptions.TiktokClientError as e:
            raise exceptions.ImporterException(utils.get_exception_message(exception=e))

        ads_details.extend(ad_details)

    logger.warning("Fetched {} ads".format(len(ads_details)))

    try:
        uploaded_path = s3_client.TiktokS3Uploader(
            s3_path=s3_path
        ).upload_resource_details(
            resource_details=ads_details,
            resource_type=enums.ResourceType.AD,
            date_created=datetime.datetime.utcnow(),
        )
    except s3_client_exceptions.TiktokS3UploaderError as e:
        raise exceptions.ImporterException(utils.get_exception_message(exception=e))

    return uploaded_path, True


def get_campaign_insights(
    user_access_token: str,
    app_id: str,
    secret: str,
    s3_path: str,
    date_from: datetime.datetime,
    date_to: datetime.datetime,
) -> typing.Tuple[typing.List[str], bool]:
    campaigns_insights = []
    tiktok_integration_client = tiktok_client.TiktokClient(
        user_access_token=user_access_token
    )
    try:
        advertiser_ids = tiktok_integration_client.get_account_ids(
            app_id=app_id, secret=secret
        )
    except tiktok_client_exceptions.TiktokClientError as e:
        raise exceptions.ImporterException(utils.get_exception_message(exception=e))

    for advertiser_id in advertiser_ids:
        try:
            campaign_insights = tiktok_integration_client.get_insights(
                advertiser_id=advertiser_id,
                resource_type=enums.ResourceType.CAMPAIGN,
                from_datetime=date_from,
                to_datetime=date_to,
            )
        except tiktok_client_exceptions.TiktokClientError as e:
            raise exceptions.ImporterException(utils.get_exception_message(exception=e))

        campaigns_insights.extend(campaign_insights)

    try:
        uploaded_paths = s3_client.TiktokS3Uploader(
            s3_path=s3_path
        ).upload_resource_performance(
            resource_performance=campaigns_insights,
            resource_type=enums.ResourceType.CAMPAIGN,
            date_created=datetime.datetime.utcnow(),
        )
    except s3_client_exceptions.TiktokS3UploaderError as e:
        raise exceptions.ImporterException(utils.get_exception_message(exception=e))

    return uploaded_paths, True


def get_adgroup_insights(
    user_access_token: str,
    app_id: str,
    secret: str,
    s3_path: str,
    date_from: datetime.datetime,
    date_to: datetime.datetime,
) -> typing.Tuple[typing.List[str], bool]:
    adgroups_insights = []
    tiktok_integration_client = tiktok_client.TiktokClient(
        user_access_token=user_access_token
    )
    try:
        advertiser_ids = tiktok_integration_client.get_account_ids(
            app_id=app_id, secret=secret
        )
    except tiktok_client_exceptions.TiktokClientError as e:
        raise exceptions.ImporterException(utils.get_exception_message(exception=e))

    for advertiser_id in advertiser_ids:
        try:
            adgroup_insights = tiktok_integration_client.get_insights(
                advertiser_id=advertiser_id,
                resource_type=enums.ResourceType.AD_GROUP,
                from_datetime=date_from,
                to_datetime=date_to,
            )
        except tiktok_client_exceptions.TiktokClientError as e:
            raise exceptions.ImporterException(utils.get_exception_message(exception=e))

        adgroups_insights.extend(adgroup_insights)

    try:
        uploaded_paths = s3_client.TiktokS3Uploader(
            s3_path=s3_path
        ).upload_resource_performance(
            resource_performance=adgroups_insights,
            resource_type=enums.ResourceType.AD_GROUP,
            date_created=datetime.datetime.utcnow(),
        )
    except s3_client_exceptions.TiktokS3UploaderError as e:
        raise exceptions.ImporterException(utils.get_exception_message(exception=e))

    return uploaded_paths, True


def get_ad_insights(
    user_access_token: str,
    app_id: str,
    secret: str,
    s3_path: str,
    date_from: datetime.datetime,
    date_to: datetime.datetime,
) -> typing.Tuple[typing.List[str], bool]:
    ads_insights = []
    tiktok_integration_client = tiktok_client.TiktokClient(
        user_access_token=user_access_token
    )
    try:
        advertiser_ids = tiktok_integration_client.get_account_ids(
            app_id=app_id, secret=secret
        )
    except tiktok_client_exceptions.TiktokClientError as e:
        raise exceptions.ImporterException(utils.get_exception_message(exception=e))

    for advertiser_id in advertiser_ids:
        try:
            ad_insights = tiktok_integration_client.get_insights(
                advertiser_id=advertiser_id,
                resource_type=enums.ResourceType.AD,
                from_datetime=date_from,
                to_datetime=date_to,
            )
        except tiktok_client_exceptions.TiktokClientError as e:
            raise exceptions.ImporterException(utils.get_exception_message(exception=e))

        ads_insights.extend(ad_insights)

    try:
        uploaded_paths = s3_client.TiktokS3Uploader(
            s3_path=s3_path
        ).upload_resource_performance(
            resource_performance=ads_insights,
            resource_type=enums.ResourceType.AD,
            date_created=datetime.datetime.utcnow(),
        )
    except s3_client_exceptions.TiktokS3UploaderError as e:
        raise exceptions.ImporterException(utils.get_exception_message(exception=e))

    return uploaded_paths, True
