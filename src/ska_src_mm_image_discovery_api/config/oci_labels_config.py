from src.ska_src_mm_image_discovery_api.decorators.singleton import singleton


@singleton
class OciLabelsConfig:
    def __init__(self, oci_labels: dict):
        self.__oci_labels = oci_labels

    @property
    def ANNOTATION(self) -> str:
        return self.__oci_labels["annotations"]

    @property
    def METADATA(self) -> str:
        return self.__oci_labels["metadata"]

    @property
    def DIGEST(self) -> str:
        return self.__oci_labels["digest"]
