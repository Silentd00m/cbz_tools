import zipfile


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
        return [x for x in _file.namelist() if str(x).lower().endswith(_filter)]

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
