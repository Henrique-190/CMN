"""
Main - Module responsible for the main program. Parses the arguments and calls the other modules.
"""
__version__ = "1.9.0"

import argparse
from datetime import datetime

from src.ColoredLogger.ColoredLogger import ColoredLogger
from src.ChangeMediaName import ChangeMediaName
from src.cmn import getFiletypes, getScanFiles, nameFormatter

logger = ColoredLogger()


def main():
    global logger
    parser = argparse.ArgumentParser(
        description="Program to scan multimedia files and rename them to their creation date.")
    parser.add_argument("-i", "--input-files", nargs="+", required=True, help="File(s) or folder(s) to scan")
    parser.add_argument("-v", "--verbose", action="store_true", default=False, help="Verbose mode")
    parser.add_argument("-r", "--recursive", action="store_true", help="Scan folders recursively", default=False)
    parser.add_argument("-ni", "--ignored-paths", nargs="*", help="Files or folders to be ignored", default=[])
    parser.add_argument("-nr", "--not-ignore-subfolders", action="store_false", default=True,
                        help="Choose to not ignore subfolders of the ignored paths")
    parser.add_argument("-t", "--file-types", nargs="*", default=[], help="List of file types to consider")
    parser.add_argument("-nt", "--not-file-types", nargs="*", default=[], help="List of file types to ignore")
    parser.add_argument("-oi", "--only-images", action="store_true", help="Consider only images", default=False)
    parser.add_argument("-ov", "--only-videos", action="store_true", help="Consider only videos", default=False)
    parser.add_argument("-cf", "--create-new-folders", action="store_true", default=False,
                        help="Create new folders according to the new image names")
    parser.add_argument("-fn", "--name-format", default="%Y%m%d_%H%M%S", help="Format of the new names")
    parser.add_argument("-ff", "--name-folder-format", default="%Y - %m - %d", help="Format of the new folder names")

    args = parser.parse_args()

    logger = ColoredLogger(args.verbose)
    initialTimer = datetime.now()
    logger.debug("Program started.")

    if not nameFormatter(args.name_format, "") or not nameFormatter(args.name_folder_format, "folder "):
        return

    filetypes = getFiletypes(args.file_types, args.only_images, args.only_videos, args.not_file_types)
    files = getScanFiles(args.input_files, args.recursive, args.ignored_paths, args.not_ignore_subfolders, filetypes)

    nChanged, nErrors = ChangeMediaName.cmn(logger, files, args.create_new_folders, args.name_format,
                                            args.name_folder_format)
    nProcessed = len(files)
    endTimer = datetime.now()
    logger.info(f"Processed {nProcessed} file{'s' if nProcessed != 1 else ''} in {endTimer - initialTimer}.")
    logger.info(f"Changed {nChanged} file{'s' if nChanged != 1 else ''}.")
    logger.info(f"Errors: {nErrors}.")
    logger.info("Program finished.")


if __name__ == "__main__":
    main()
