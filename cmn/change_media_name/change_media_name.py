"""
CMN - Common functions
"""
__version__ = "2.0.0"

import os
import subprocess
from datetime import datetime
from shutil import which

from cmn.colored_logger.colored_logger import ColoredLogger
from cmn.output_formatter.output_formatter import (
    ImageRegularformatter,
    VideoRegularformatter,
    AVIformatter
)

NewNameFile = '{year}{month}{day}_{hour}{minute}{second}{filetype}'
NewNameFolder = '{year}-{month}-{day}'

n_changed = 0
n_errors = 0
completed = 0.0

logger: ColoredLogger

formatters = {
    ".jpg": ImageRegularformatter,
    ".jpeg": ImageRegularformatter,
    ".png": ImageRegularformatter,
    ".mp4": VideoRegularformatter,
    ".avi": AVIformatter,
    ".mov": VideoRegularformatter,
    ".heic": ImageRegularformatter,
    ".webp": ImageRegularformatter,
}


def checkExiftool() -> bool:
    return which('exiftool') is not None


def getDateTime(file: str) -> tuple:
    global logger
    try:
        output = subprocess.check_output(
            ["exiftool", file],
            shell=True, text=True, stderr=subprocess.STDOUT
        )
        output = output.strip()
        return formatters[os.path.splitext(file)[1].lower()](output).getGroups()
    except (Exception,):
        logger.error(f"{completed:.2f}% - Error getting datetime for {file}")

    return ()


def createFolder(folderFormat: str, date: tuple[str]) -> str:
    global logger
    if len(date) == 7:
        datestr = datetime.strptime("".join(date), "%Y%m%d%H%M%S%f")
    else:
        datestr = datetime.strptime("".join(date), "%Y%m%d%H%M%S")

    folder = datestr.strftime(folderFormat)
    if not os.path.exists(folder):
        os.mkdir(folder)
        logger.info(f"{completed:.2f}% - Created folder {folder}")
    return folder


def changeFileName(
        oldPath: str, newPath: str, oldFile: str,
        nameFormat: str, date_tuple: tuple[str]
):
    global n_changed, n_errors, logger

    date_str = "".join(date_tuple)
    if len(date_tuple) == 7:
        date = datetime.strptime(date_str, "%Y%m%d%H%M%S%f")
    else:
        date = datetime.strptime(date_str, "%Y%m%d%H%M%S")

    new = date.strftime(nameFormat)
    new += os.path.splitext(oldFile)[1]

    counter = 1

    if new == oldFile:
        logger.warning(f"{completed:.2f}% - File {oldFile} already has the correct name.")
        return

    # Need to check if path exists AND if the file is the same. If it is the same, we don't need to change the name.
    while os.path.exists(os.path.join(newPath, new)):
        counter += 1

        new = date.strftime(nameFormat)
        new += '(' + str(counter) + ')'
        new += os.path.splitext(oldFile)[1]

    try:
        os.rename(os.path.join(oldPath, oldFile), os.path.join(newPath, new))
        logger.success(f"{completed:.2f}% - Changed {oldFile} to {new}")
        n_changed += 1
    except (Exception,) as e:
        logger.error(f"{completed:.2f}% - Error while changing name of {oldFile}: {e}")
        n_errors += 1


def cmn(coloredLog: ColoredLogger, files: list[str], newFolder: bool, nameFormat: str, folderFormat: str) -> \
        (int, int):
    global logger, n_errors, completed
    logger = coloredLog
    command = checkExiftool()
    percentage = max(100 / (2 * (len(files))), 100)
    completed = 0.00
    if not command:
        logger.critical("Exiftool program/Command missing. Please install it: https://exiftool.org/install.html")
        return 0, 1

    for file in files:
        completed += percentage
        logger.info(f"{completed:.2f}% - Processing {file}")
        completed += percentage
        try:
            date = getDateTime(file)
        except (Exception,):
            logger.error(f"{completed:.2f}% - Error while getting date from {file}.")
            continue

        if date == ():
            logger.warning(f"{completed:.2f}% - Couldn't get date from {file}.")
            continue

        folder = ""
        if newFolder:
            try:
                folder = createFolder(folderFormat, date)
            except (Exception,):
                logger.error(f"{completed:.2f}% - Error while creating folder for {file}.")
                continue

        try:
            oldpath = os.path.dirname(file)
            oldfile = os.path.basename(file)
            if folder:
                newpath = os.path.join(os.getcwd(), folder)
            else:
                newpath = oldpath
            changeFileName(oldpath, newpath, oldfile, nameFormat, date)
        except (Exception,):
            logger.error(f"{completed:.2f}% - Error getting new path of {file}.")
            n_errors += 1
            continue

    return n_changed, n_errors


if __name__ == "__main__":
    print("dont")
