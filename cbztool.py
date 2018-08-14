#!/usr/bin/python3

import os
import cbzlib
import argparse
import wand.image


def modify_image(input_data: str, colourspace: str = "rgb", depth: int = 8,
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


def merge_cbzs(args):
    counter = 1

    with cbzlib.cbz_file(args.output[0], "w") as of:
        for cbz in input_files:
            with cbzlib.cbz_file(cbz, "r") as _if:
                for image in _if.list_contents():
                    filename = (str(counter).zfill(4) + "." +
                                image.split(".")[-1])

                    if args.verbose:
                        print("Adding file '" + cbz + "/" + image + "' as '" +
                              filename + "'")

                    if (args.depth or args.quality or args.resize or
                            args.colourspace or args.format):
                        of.add_bytes_as_file(filename, modify_image(
                            _if.read(image), colourspace=args.colourspace,
                            depth=args.depth, resize=args.resize,
                            keep_aspect=args.keep_aspect,
                            compression_quality=args.quality))
                    else:
                        of_add_bytes_as_file(_if.read(image))

                    counter = counter + 1


def create_cbz(args):
    counter = 1

    with cbzlib.cbz_file(args.output[0], "w") as of:
        for path in args.input:
            if os.path.isdir(path):
                for image in [f for f in sorted(os.listdir(path))
                              if (os.path.isfile(os.path.join(path, f)) and
                                  str(f).lower().endswith(tuple([".png", ".jpg",
                                                                 ".jpeg"])))]:
                    with open(os.path.join(path, image)) as _if:
                        if (args.depth or args.quality or args.resize or
                                args.colourspace or args.format):
                            of.add_bytes_as_file(
                                str(counter).zfill(4) +
                                "." + args.format, modify_image(
                                    open(os.path.join(
                                        path, image)).read(),
                                    colourspace=args.colourspace,
                                    depth=args.depth,
                                    resize=args.resize,
                                    keep_aspect=args.keep_aspect,
                                    compression_quality=args.quality))
                        else:
                            of.add_bytes_as_file(_if.read(image),
                                                 str(counter).zfill(4) +
                                                 "." + image.split(".")[-1])

                    if args.verbose:
                        print("Adding file '" + path + "' as '" +
                              str(counter).zfill(4) + "." + ext + "'")

                    counter = counter + 1
            elif (os.path.isfile(path) and
                  str(path).lower().endswith(tuple([".png", ".jpg", ".jpeg"]))):
                if (args.depth or args.quality or args.resize or
                        args.colourspace or args.format):
                    of.add_bytes_as_file(
                        str(counter).zfill(4) +
                        "." + args.format, modify_image(
                            open(path, "rb").read(),
                            colourspace=args.colourspace,
                            depth=args.depth,
                            resize=args.resize,
                            keep_aspect=args.keep_aspect,
                            compression_quality=args.quality))

                else:
                    ext = path.split(".")[-1]

                    of.add_file(path, str(counter) + "." + ext)

                counter = counter + 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Tool for generating and manipulating CBZ files.")
    parser.add_argument("-v", "--verbose", action="store_true")

    subparsers = parser.add_subparsers(
        title="command", dest="command", help="Sub-command help")

    create_parser = subparsers.add_parser("create", help="Create CBZ files")
    create_parser.add_argument(
        "-f", "--format", choices=["png", "jpg"],
        help="The image format to store the images inside the CBZ as.")
    create_parser.add_argument(
        "-c", "--colourspace", choices=["rgb", "grey"],
        help="Defines the colourspace of the image.")
    create_parser.add_argument("-d", "--depth", type=int,
                               help="Bit-depth per channel.")
    create_parser.add_argument("-q", "--quality", type=int, help="Set the image"
                               " quality. 100 = perfect, 0 = 90s website image.")
    create_parser.add_argument(
        "-r", "--resize",
        help=("Resize the image to the defined size. (WIDTHxHEIGHT)\n"
              "If -k is active, The image will be resized so it is smaller than"
              " both given width and height."))
    create_parser.add_argument(
        "-k", "--keep-aspect", action="store_true",
        help="Keep the aspect ratio of the images.")
    create_parser.add_argument("input", metavar="input", type=str, nargs="+",
                               help=("The input to create the .cbz from. May be"
                                     " folders or files."))
    create_parser.add_argument("output", metavar="output", type=str, nargs=1,
                               help="The output filename.")

    merge_parser = subparsers.add_parser("merge", help="Merge CBZ files")
    merge_parser.add_argument(
        "-f", "--format", choices=["png", "jpg"],
        help="The image format to store the images inside the CBZ as.")
    merge_parser.add_argument(
        "-c", "--colourspace", choices=["rgb", "grey"],
        help="Defines the colourspace of the image.")
    merge_parser.add_argument("-d", "--depth", type=int,
                              help="Bit-depth per channel.")
    merge_parser.add_argument("-q", "--quality", type=int, help="Set the image "
                              "quality. 100 = perfect, 0 = 90s website image.")
    merge_parser.add_argument(
        "-r", "--resize",
        help=("Resize the image to the defined size. (WIDTHxHEIGHT)\n"
              "If -k is active, The image will be resized so it is smaller than"
              " both given width and height."))
    merge_parser.add_argument(
        "-k", "--keep-aspect", action="store_true",
        help="Keep the aspect ratio of the images.")
    merge_parser.add_argument("input", metavar="input", type=str, nargs="+",
                              help="A list of .cbz-Files to combine.")
    merge_parser.add_argument("output", metavar="output", type=str, nargs=1,
                              help="The output filename.")

    args = parser.parse_args()

    if args.command == "create":
        create_cbz(args)
    elif args.command == "merge":
        merge_cbzs(args)
