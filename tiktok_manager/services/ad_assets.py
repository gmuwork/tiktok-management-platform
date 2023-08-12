import logging
import typing

from tiktok_manager import exceptions, utils
from tiktok_manager.integrations.clients.tiktok import client as tiktok_client
from tiktok_manager.integrations.clients.tiktok import (
    exceptions as tiktok_client_exceptions,
)

logger = logging.getLogger(__name__)


def add_image(
    user_access_token: str,
    advertiser_id: str,
    image_details: typing.Dict,
) -> typing.Tuple[str, bool]:
    try:
        image_id = tiktok_client.TiktokClient(
            user_access_token=user_access_token
        ).create_image(advertiser_id=advertiser_id, image_details=image_details)
    except tiktok_client_exceptions.TiktokClientError as e:
        raise exceptions.AdAssetsException(utils.get_exception_message(exception=e))

    logger.warning("Created image (id={})".format(image_id))

    return image_id, True


def update_image_name(
    user_access_token: str,
    advertiser_id: str,
    image_id: str,
    image_name: str,
) -> bool:
    try:
        image_updated = tiktok_client.TiktokClient(
            user_access_token=user_access_token
        ).update_image_name(
            advertiser_id=advertiser_id,
            image_id=image_id,
            image_name=image_name,
        )
    except tiktok_client_exceptions.TiktokClientError as e:
        raise exceptions.AdAssetsException(utils.get_exception_message(exception=e))

    logger.warning(
        "Updated image name (id={}, success={})".format(image_id, image_updated)
    )

    return image_updated


def get_images_info(
    user_access_token: str,
    advertiser_id: str,
    image_ids: typing.List[str],
) -> typing.List[typing.Dict]:
    try:
        images_info = tiktok_client.TiktokClient(
            user_access_token=user_access_token
        ).get_images_info(
            advertiser_id=advertiser_id,
            image_ids=image_ids,
        )
    except tiktok_client_exceptions.TiktokClientError as e:
        raise exceptions.AdAssetsException(utils.get_exception_message(exception=e))

    logger.warning(
        "Got info for images (id={}, image_ids={}, images_info={})".format(
            advertiser_id, image_ids, images_info
        )
    )

    return images_info


def add_video(
    user_access_token: str,
    advertiser_id: str,
    video_details: typing.Dict,
) -> typing.Tuple[str, bool]:
    try:
        video_id = tiktok_client.TiktokClient(
            user_access_token=user_access_token
        ).create_video(advertiser_id=advertiser_id, video_details=video_details)
    except tiktok_client_exceptions.TiktokClientError as e:
        raise exceptions.AdAssetsException(utils.get_exception_message(exception=e))

    logger.warning("Created video (id={})".format(video_id))

    return video_id, True


def update_video_name(
    user_access_token: str,
    advertiser_id: str,
    video_id: str,
    video_name: str,
) -> bool:
    try:
        video_updated = tiktok_client.TiktokClient(
            user_access_token=user_access_token
        ).update_video_name(
            advertiser_id=advertiser_id,
            video_id=video_id,
            video_name=video_name,
        )
    except tiktok_client_exceptions.TiktokClientError as e:
        raise exceptions.AdAssetsException(utils.get_exception_message(exception=e))

    logger.warning(
        "Updated video name (id={}, success={})".format(video_id, video_updated)
    )

    return video_updated


def get_videos_info(
    user_access_token: str,
    advertiser_id: str,
    video_ids: typing.List[str],
) -> typing.List[typing.Dict]:
    try:
        videos_info = tiktok_client.TiktokClient(
            user_access_token=user_access_token
        ).get_videos_info(
            advertiser_id=advertiser_id,
            video_ids=video_ids,
        )
    except tiktok_client_exceptions.TiktokClientError as e:
        raise exceptions.AdAssetsException(utils.get_exception_message(exception=e))

    logger.warning(
        "Got info for videos (id={}, video_ids={}, videos_info={})".format(
            advertiser_id, video_ids, videos_info
        )
    )

    return videos_info
