#!/usr/bin/python3

import os
import lib.cbzlib
import argparse
import wand.image


def create_cbz(args):
    lib.cbzlib.create_cbz(
        args.input, args.output[0], args.format, args.colourspace, args.depth,
        args.resize, args.keep_aspect, args.quality, args.verbose)


def merge_cbzs(args):
    lib.cbzlib.create_cbz(
        args.input, args.output[0], args.format, args.colourspace, args.depth,
        args.resize, args.keep_aspect, args.quality, args.verbose)


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
