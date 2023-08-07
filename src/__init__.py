"""
Main - Module responsible for the main program. Parses the arguments and calls the other modules.
"""
__version__ = "2.0.0"

import os
import re
from datetime import datetime

from src.colored_logger.colored_logger import ColoredLogger

logger = ColoredLogger()

images_supported = [".jpg", ".jpeg", ".png", ".heic", ".webp"]
videos_supported = ['.mp4', '.avi', '.mov']


def name_formatter(name_f: str, aux: str) -> bool:
    """Checks if the name format is valid"""
    logger.debug(f"Parsing {aux}name format")
    now = datetime.now().strftime(name_f)
    nowdate = datetime.strptime(now, name_f)

    if nowdate.year == 1900 and nowdate.month == 1 and nowdate.day == 1:
        logger.critical(f"The {aux}name format is not valid for a date.")
        return False

    if aux == "":
        invalid_characters = re.compile(r'[^\w\-.]')
        if invalid_characters.search(now):
            logger.critical(f"The {aux}name format is not valid for a file name.")
            return False
    else:
        invalid_characters = re.compile(r'[/<>:\"\\|?*]')
        if invalid_characters.search(now):
            logger.critical(f"The {aux}name format is not valid for a folder name.")
            return False

    logger.info(f"Example of {aux}name format: {now}")
    return True


def recursive_search(path: str) -> list[str]:
    """Gets the files from the path searching subfolders"""
    files: list[str] = []
    for root, _, filelist in os.walk(path):
        for file in filelist:
            files.append(os.path.join(root, file))
    return [x.replace("\\", "/") for x in files]


def not_recursive_search(path: str) -> list[str]:
    """Gets the files from the path without searching subfolders"""
    return [
        os.path.join(path, x)
        .replace("\\", "/") for x in os.listdir(path) if os.path.isfile(os.path.join(path, x))
    ]


def get_files(paths: list[str], recursive: bool) -> list[str]:
    """Gets the files from the paths"""
    files: list[str] = []
    for path in paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"The path '{path}' does not exist.")

        if os.path.isfile(path):
            files.append(path)
        else:
            if recursive:
                files += recursive_search(path)
            else:
                files += not_recursive_search(path)
    return files


def get_scan_files(
        input_files: list[str], recursive: bool, ignored_paths: list[str],
        not_ignore_subfolders: bool, filetypes: list[str]
) -> list[str]:
    """Gets the files to scan based on the arguments"""
    logger.debug("Getting files to scan")

    files = get_files(input_files, recursive)
    ignored = get_files(ignored_paths, not_ignore_subfolders)

    files = [x for x in files if x not in ignored and os.path.splitext(x)[1].lower() in filetypes]
    length = len(files)

    logger.info(f"{length} file{'s' if length != 1 else ''} to scan")

    return files


def get_filetypes(
        file_types: list[str], only_images: bool,
        only_videos: bool, not_file_types: list[str]
) -> list[str]:
    """Gets the file types to scan based on the arguments"""
    logger.debug("Getting file types to scan")
    supported = images_supported + videos_supported
    filetypes = []
    if file_types:
        for file_type in file_types:
            if file_type not in supported:
                logger.warning(f"File type '{file_type}' is not supported.")
                continue
            filetypes.append(file_type)
    else:
        if only_images:
            filetypes = images_supported
        elif only_videos:
            filetypes = videos_supported

        if not_file_types:
            if filetypes:
                filetypes = [x for x in filetypes if x not in not_file_types]
            else:
                filetypes = [x for x in supported if x not in not_file_types]

        if not filetypes:
            filetypes = supported
    logger.info(f"{len(filetypes)} file types to scan: {filetypes}")
    return filetypes
