import wand.image
import photohash


def convert(input_data: str, colourspace: str = "rgb", depth: int = 8,
            output_format: str = "png", resize=False, keep_aspect=False,
            resize_filter: wand.image.FILTER_TYPES='lanczos2sharp',
            compression_quality: int = None):
    with wand.image.Image(blob=input_data) as image:
        image.format = output_format

        if colourspace == "grey":
            image.type = 'grayscale'

        image.depth = depth

        if resize and keep_aspect:
            image.transform(resize + ">")
        elif resize:
            width, height = resize.split("x")

            image.resize(int(width), int(height))

        if compression_quality:
            image.compression_quality = compression_quality

        return image.make_blob()


def find_duplicates(images: list):
    pass
