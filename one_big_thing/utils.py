from whitenoise.storage import CompressedManifestStaticFilesStorage


class CompressedManifestStaticFilesStorage(CompressedManifestStaticFilesStorage):

    def url(self, name, force=True):
        """
        Override .url to use hashed url in development
        """
        return super().url(name, True)
