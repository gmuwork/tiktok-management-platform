import logging
import typing

from tiktok_manager import exceptions, utils
from tiktok_manager.integrations.clients.tiktok import client as tiktok_client
from tiktok_manager.integrations.clients.tiktok import (
    exceptions as tiktok_client_exceptions,
)

logger = logging.getLogger(__name__)


def add_campaign(
    user_access_token: str,
    advertiser_id: str,
    campaign_details: typing.Dict,
) -> typing.Tuple[str, bool]:
    try:
        campaign_id = tiktok_client.TiktokClient(
            user_access_token=user_access_token
        ).create_campaign(
            advertiser_id=advertiser_id, campaign_details=campaign_details
        )
    except tiktok_client_exceptions.TiktokClientError as e:
        raise exceptions.ActionException(utils.get_exception_message(exception=e))

    logger.warning("Created campaign (id={})".format(campaign_id))

    return campaign_id, True


def update_campaign(
    user_access_token: str,
    advertiser_id: str,
    campaign_id: str,
    campaign_details: typing.Dict,
) -> bool:
    try:
        campaign_updated = tiktok_client.TiktokClient(
            user_access_token=user_access_token
        ).update_campaign(
            advertiser_id=advertiser_id,
            campaign_id=campaign_id,
            campaign_details=campaign_details,
        )
    except tiktok_client_exceptions.TiktokClientError as e:
        raise exceptions.ActionException(utils.get_exception_message(exception=e))

    logger.warning(
        "Updated campaign (id={}, success={})".format(campaign_id, campaign_updated)
    )

    return campaign_updated


def add_adgroup(
    user_access_token: str,
    advertiser_id: str,
    adgroup_details: typing.Dict,
) -> typing.Tuple[str, bool]:
    try:
        adgroup_id = tiktok_client.TiktokClient(
            user_access_token=user_access_token
        ).create_adgroup(advertiser_id=advertiser_id, adgroup_details=adgroup_details)
    except tiktok_client_exceptions.TiktokClientError as e:
        raise exceptions.ActionException(utils.get_exception_message(exception=e))

    logger.warning("Created adgroup (id={})".format(adgroup_id))

    return adgroup_id, True


def update_adgroup(
    user_access_token: str,
    advertiser_id: str,
    adgroup_id: str,
    adgroup_details: typing.Dict,
) -> bool:
    try:
        adgroup_updated = tiktok_client.TiktokClient(
            user_access_token=user_access_token
        ).update_adgroup(
            advertiser_id=advertiser_id,
            adgroup_id=adgroup_id,
            adgroup_details=adgroup_details,
        )
    except tiktok_client_exceptions.TiktokClientError as e:
        raise exceptions.ActionException(utils.get_exception_message(exception=e))

    logger.warning(
        "Updated adgroup (id={}, success={})".format(adgroup_id, adgroup_updated)
    )

    return adgroup_updated


def add_ads(
    user_access_token: str,
    advertiser_id: str,
    adgroup_id: str,
    ad_details: typing.Dict,
) -> typing.Tuple[typing.List[str], bool]:
    try:
        ad_ids = tiktok_client.TiktokClient(
            user_access_token=user_access_token
        ).create_ads(
            advertiser_id=advertiser_id, adgroup_id=adgroup_id, ad_details=ad_details
        )
    except tiktok_client_exceptions.TiktokClientError as e:
        raise exceptions.ActionException(utils.get_exception_message(exception=e))

    logger.warning("Created ads (ids={})".format(ad_ids))

    return ad_ids, True


def update_ads(
    user_access_token: str,
    advertiser_id: str,
    adgroup_id: str,
    ad_details: typing.Dict,
) -> bool:
    try:
        ad_updated = tiktok_client.TiktokClient(
            user_access_token=user_access_token
        ).update_ads(
            advertiser_id=advertiser_id, adgroup_id=adgroup_id, ad_details=ad_details
        )
    except tiktok_client_exceptions.TiktokClientError as e:
        raise exceptions.ActionException(utils.get_exception_message(exception=e))

    logger.warning("Updated ads (success={})".format(ad_updated))

    return ad_updated


def update_ads_status(
    user_access_token: str,
    advertiser_id: str,
    ads_status_details: typing.Dict,
) -> bool:
    try:
        updated_ads_status = tiktok_client.TiktokClient(
            user_access_token=user_access_token
        ).update_ads_status(
            advertiser_id=advertiser_id, ads_status_details=ads_status_details
        )
    except tiktok_client_exceptions.TiktokClientError as e:
        raise exceptions.ActionException(utils.get_exception_message(exception=e))

    logger.warning("Updated ad statuses (success={})".format(updated_ads_status))

    return updated_ads_status
