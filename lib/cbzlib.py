import os
import zipfile
import importlib
import lib.imagelib as imagelib


class cbz_file:
    """
    """
    _file: zipfile.ZipFile = None

    def __init__(self, filename: str, mode: str = "r",
                 compression: int = zipfile.ZIP_STORED):
        self._file = zipfile.ZipFile(filename, mode=mode)

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self._file.close()

    def list_contents(self, ext_filter: tuple = tuple(['.jpg',
                                                       '.png',
                                                       '.jpeg'])) -> list:
        """
        List the contents (files inside) of the archive.

        @param[in] ext_filter A string or tuple used to filter the returned file
        list. (default: .jpg, .png, .jpeg)
        """
        return sorted([x for x in self._file.namelist()
                       if str(x).lower().endswith(ext_filter)])

    def read_file(self, filename: str) -> bytes:
        """
        Read the contents of a file inside the archive.

        @param[in] filename The path of the file inside the archive to read.
        """
        return self._file.read(filename)

    def extract_file(self, filename: str, output_path: str):
        """
        Extract a file from the archive.

        @param[in] filename The path of the file inside the archive to extract.
        @param[in] output_path The path to extract the file to, including the
        filename.
        """
        self._file.extract(filename, output_path)

    def add_file(self, path: str, archive_path: str):
        """
        Add a file to the archive.

        @param[in] path The path of the file to add.
        @param[in] archive_path The where to store the file inside the archive,
        including the filename.
        """
        self._file.write(path, archive_path)

    def add_bytes_as_file(self, filename: str, data: bytes):
        """
        Add a file to the archive with the provided contents.

        @param[in] filename The where to store the file inside the archive,
        including the filename.
        @param[in] data The bytes to write into the file.
        """
        self._file.writestr(filename, data)


def create_cbz(input_files: list, output: str, _format: str = None,
               colourspace: int = None, depth: int = None, resize: str = False,
               keep_aspect: bool = False, quality: int = None,
               verbose: bool = False):
    counter = 1

    with cbz_file(output, "w") as of:
        for path in input_files:
            if os.path.isdir(path):
                for image in [f for f in sorted(os.listdir(path))
                              if (os.path.isfile(os.path.join(path, f)) and
                                  str(f).lower().endswith(tuple([".png", ".jpg",
                                                                 ".jpeg"])))]:
                    with open(os.path.join(path, image)) as _if:
                        if depth or quality or resize or colourspace or _format:
                            __format = None

                            if _format is None:
                                __format = image.split(".")[-1]
                            else:
                                __format = _format

                            of.add_bytes_as_file(
                                str(counter).zfill(4) +
                                "." + _format, imagelib.convert(
                                    open(os.path.join(
                                        path, image)).read(),
                                    output_format=__format,
                                    colourspace=colourspace,
                                    depth=depth,
                                    resize=resize,
                                    keep_aspect=keep_aspect,
                                    compression_quality=quality))
                        else:
                            of.add_bytes_as_file(_if.read(image),
                                                 str(counter).zfill(4) +
                                                 "." + image.split(".")[-1])

                    if verbose:
                        print("Adding file '" + path + "' as '" +
                              str(counter).zfill(4) + "." + ext + "'")

                    counter = counter + 1
            elif (os.path.isfile(path) and
                  str(path).lower().endswith(tuple([".png", ".jpg", ".jpeg"]))):
                if (depth or quality or resize or
                        colourspace or _format):
                    __format = None

                    if _format is None:
                        __format = image.split(".")[-1]
                    else:
                        __format = _format

                    of.add_bytes_as_file(
                        str(counter).zfill(4) +
                        "." + _format, imagelib.convert(
                            open(path, "rb").read(),
                            output_format=__format,
                            colourspace=colourspace,
                            depth=depth,
                            resize=resize,
                            keep_aspect=keep_aspect,
                            compression_quality=quality))

                else:
                    ext = path.split(".")[-1]

                    of.add_file(path, str(counter) + "." + ext)

                counter = counter + 1


def merge_cbzs(input_files: list, output: str, _format: str = None,
               colourspace: int = None, depth: int = None, resize: str = False,
               keep_aspect: bool = False, quality: int = None,
               verbose: bool = False):
    counter = 1

    with cbz_file(output, "w") as of:
        for cbz in input_files:
            with cbz_file(cbz, "r") as _if:
                for image in _if.list_contents():
                    if _format is None:
                        __format = image.split(".")[-1]
                    else:
                        __format = _format

                    filename = (str(counter).zfill(4) + "." +
                                __format)

                    if verbose:
                        print("Adding file '" + cbz + "/" + image + "' as '" +
                              filename + "'")

                    if depth or quality or resize or colourspace or _format:
                        of.add_bytes_as_file(filename, imagelib.convert(
                            _if.read_file(image), colourspace=colourspace,
                            depth=depth, resize=resize,
                            keep_aspect=keep_aspect,
                            compression_quality=quality))
                    else:
                        of.add_bytes_as_file(filename, _if.read_file(image))

                    counter = counter + 1


def modify_cbz(input_file: str, output: str, _format: str = None,
               colourspace: int = None, depth: int = None, resize: str = False,
               keep_aspect: bool = False, quality: int = None,
               verbose: bool = False):
    with cbz_file(output, "w") as of:
        with cbz_file(input_file, "r") as _if:
            for image in _if.list_contents():
                if _format is None:
                    __format = image.split(".")[-1]
                else:
                    __format = _format

                filename = (str(counter).zfill(4) + "." +
                            __format)

                if verbose:
                    print("Adding file '" + input_file + "/" + image + "' as '" +
                          filename + "'")

                if depth or quality or resize or colourspace or _format:
                    of.add_bytes_as_file(filename, imagelib.convert(
                        _if.read_file(image), colourspace=colourspace,
                        depth=depth, resize=resize,
                        keep_aspect=keep_aspect,
                        compression_quality=quality))
                else:
                    of.add_bytes_as_file(filename, _if.read_file(image))
