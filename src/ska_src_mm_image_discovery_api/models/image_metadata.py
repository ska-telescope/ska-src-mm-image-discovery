class ImageMetadata:

    def __init__(self, image_id: str, author_name: str, types: list[str], digest: str, tag: str, *args, **kwargs):
        self.image_id = image_id
        self.author_name = author_name
        self.types = types
        self.digest = digest
        self.tag = tag

    def to_dict(self):
        return {
            'image_id': self.image_id,
            'author_name': self.author_name,
            'types': self.types,
            'digest': self.digest,
            'tag': self.tag
        }
