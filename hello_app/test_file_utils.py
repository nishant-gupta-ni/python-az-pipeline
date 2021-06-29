import logging
import pytest
from pytest_mock import mocker

from . import file_utils 

LOGGER = logging.getLogger(__name__)

@pytest.mark.parametrize(
    "rel_path_to_extract, remote_path, local_path",
    [
        (
            ["*"],
            "/path/to/remote.zip",
            "/path/to/local",
        ),
    ],
)
def test_extract_files_and_folders_from_zip_extract_all(mocker, rel_path_to_extract, remote_path, local_path):
    mock_ZipFile = mocker.patch("zipfile.ZipFile")
    file_utils.extract_files_and_folders_from_zip(rel_path_to_extract, remote_path, local_path)
    mock_ZipFile.return_value.__enter__.return_value.extractall.assert_called_once_with(local_path)

@pytest.mark.parametrize(
    "rel_path_to_extract, remote_path, local_path",
    [
        (
            ["filename1", "foldername1"],
            "/path/to/remote.zip",
            "/path/to/local",
        ),
    ],
)
def test_extract_files_and_folders_from_zip_extract_partial(mocker, rel_path_to_extract, remote_path, local_path):
    mock_ZipFile = mocker.patch("zipfile.ZipFile")
    mock_ZipFile.return_value.__enter__.return_value.namelist.return_value = ["filename1", "foldername1", "filename2", "foldername2"]
    file_utils.extract_files_and_folders_from_zip(rel_path_to_extract, remote_path, local_path)
    assert len(mock_ZipFile.return_value.__enter__.return_value.extract.mock_calls) == 2
    mock_ZipFile.return_value.__enter__.return_value.namelist.assert_called_once()

@pytest.mark.parametrize(
    "rel_path_to_extract, remote_path, local_path",
    [
        (
            ["filenotpresent", "foldernotpresent"],
            "/path/to/remote.zip",
            "/path/to/local",
        ),
    ],
)
def test_extract_files_and_folders_from_zip_extract_partial_file_not_found(mocker, rel_path_to_extract, remote_path, local_path, caplog):
    mock_ZipFile = mocker.patch("zipfile.ZipFile")
    entities_present = ["filename1", "foldername1"]
    mock_ZipFile.return_value.__enter__.return_value.namelist.return_value = entities_present
    file_utils.extract_files_and_folders_from_zip(rel_path_to_extract, remote_path, local_path)
    mock_ZipFile.return_value.__enter__.return_value.extract.assert_not_called()
    mock_ZipFile.return_value.__enter__.return_value.namelist.assert_called_once()
    assert 'Entity {0} not found in the zipped file {1}'.format(
        rel_path_to_extract[0], remote_path) in caplog.text
    assert 'Entity {0} not found in the zipped file {1}'.format(
        rel_path_to_extract[1], remote_path) in caplog.text