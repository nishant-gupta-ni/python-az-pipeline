import logging
import zipfile

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())


def extract_files_and_folders_from_zip(
    rel_path_to_extract, remote_path, local_path
):
    """
    Extracts files and/or folders if remote_path is zip file.

    Args:
        rel_path_to_extract (list of str): Specifies the files and/or folders to extract. There
        are two cases here -
        1. ["*"] - Extract all files/folders from remote_path.
        2. ["filename", "foldername"] - Extract only the files/folders given in the list.

        remote_path (str): Specifies the zip file to extract files/folders from.
        local_path (str): Specifies the location where to extract files/folders from.

    *IMPORTANT CAUTION* - The ZipFile package used here only works if the size of the
    zip file being extracted is less then 4Gb & might throw exceptions for very
    large size zip file

    """
    if isinstance(rel_path_to_extract, list):
        if rel_path_to_extract[0] == "*":
            with zipfile.ZipFile(remote_path, "r") as zipobj:
                zipobj.extractall(local_path)
        else:
            with zipfile.ZipFile(remote_path, "r") as zipobj:
                zippedfiles = zipobj.namelist()
                for filename in rel_path_to_extract:
                    convert_filename_to_linux = filename.replace("\\", "/")
                    file_found = False
                    for zippedfile in zippedfiles:
                        if zippedfile.startswith(convert_filename_to_linux):
                            zipobj.extract(zippedfile, local_path)
                            file_found = True
                    if not file_found:
                        _logger.warning(
                            "Entity {0} not found in the zipped file {1}".format(
                                filename, remote_path
                            )
                        )

