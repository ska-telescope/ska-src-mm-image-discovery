from src.ska_src_mm_image_discovery_api.decorators.singleton import singleton


@singleton
class OciConfig:
    def __init__(self, oci_labels: dict, default_oci_resource: dict):
        self.__oci_labels = oci_labels
        self.__default_oci_resource = default_oci_resource

    @property
    def ANNOTATION_KEY(self) -> str:
        return self.__oci_labels["annotations"]

    @property
    def METADATA_KEY(self) -> str:
        return self.__oci_labels["metadata"]

    @property
    def DIGEST_KEY(self) -> str:
        return self.__oci_labels["digest"]

    @property
    def DEFAULT_OCI_RESOURCE(self) -> dict:
        return self.__default_oci_resource
