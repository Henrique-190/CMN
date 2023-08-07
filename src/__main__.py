"""
Main - Module responsible for the main program. Parses the arguments and calls the other modules.
"""
__version__ = "2.0.0"

import argparse
from datetime import datetime

from src.colored_logger.colored_logger import ColoredLogger
from src.change_media_name.change_media_name import cmn
from src import get_filetypes, get_scan_files, name_formatter


def main():
    """Main function of the program"""
    logger = ColoredLogger()
    parser = argparse.ArgumentParser(
        description="Program to scan multimedia files and rename them to their creation date.")
    parser.add_argument("-i", "--input-files", nargs="+", required=True,
                        help="File(s) or folder(s) to scan")
    parser.add_argument("-v", "--verbose", action="store_true", default=False, help="Verbose mode")
    parser.add_argument("-r", "--recursive", action="store_true", default=False,
                        help="Scan folders recursively")
    parser.add_argument("-ni", "--ignored-paths", nargs="*", default=[],
                        help="Files or folders to be ignored")
    parser.add_argument("-nr", "--not-ignore-subfolders", action="store_false", default=True,
                        help="Choose to not ignore subfolders of the ignored paths")
    parser.add_argument("-t", "--file-types", nargs="*", default=[],
                        help="List of file types to consider")
    parser.add_argument("-nt", "--not-file-types", nargs="*", default=[],
                        help="List of file types to ignore")
    parser.add_argument("-oi", "--only-images", action="store_true",
                        help="Consider only images", default=False)
    parser.add_argument("-ov", "--only-videos", action="store_true",
                        help="Consider only videos", default=False)
    parser.add_argument("-cf", "--create-new-folders", action="store_true", default=False,
                        help="Create new folders according to the new image names")
    parser.add_argument("-fn", "--name-format", default="%Y%m%d_%H%M%S",
                        help="Format of the new names")
    parser.add_argument("-ff", "--name-folder-format", default="%Y - %m - %d",
                        help="Format of the new folder names")

    args = parser.parse_args()

    logger = ColoredLogger(args.verbose)
    initial_timer = datetime.now()
    logger.debug("Program started.")

    if (
            not name_formatter(args.name_format, "") or
            not name_formatter(args.name_folder_format, "folder ")
    ):
        return

    filetypes = get_filetypes(
        args.file_types, args.only_images, args.only_videos, args.not_file_types
    )
    files = get_scan_files(
        args.input_files, args.recursive, args.ignored_paths, args.not_ignore_subfolders, filetypes
    )

    n_changed, n_errors = cmn(
        logger, files, args.create_new_folders, args.name_format, args.name_folder_format
    )
    n_processed = len(files)
    end_timer = datetime.now()
    logger.info(f"Processed {n_processed} file"
                f"{'s' if n_processed != 1 else ''} in {end_timer - initial_timer}.")
    logger.info(f"Changed {n_changed} file{'s' if n_changed != 1 else ''}.")
    logger.info(f"Errors: {n_errors}.")
    logger.info("Program finished.")


if __name__ == "__main__":
    main()
