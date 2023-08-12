class TiktokS3UploaderError(Exception):
    pass


class S3PathIsNotValidError(TiktokS3UploaderError):
    pass


class S3ClientError(TiktokS3UploaderError):
    pass
