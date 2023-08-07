"""
Main test file
"""
import unittest

from src import (
    recursive_search, not_recursive_search, name_formatter,
    get_files, get_scan_files, get_filetypes
)


class MainTest(unittest.TestCase):
    """Main test class"""
    def test_name_formatter(self):
        """Test name_formatter function"""
        samples = [
            {
                "nf": "%Y%m%d_%H%M%S",
                "aux": "",
                "expected": True
            },
            {
                "nf": "hihihi",
                "aux": "",
                "expected": False
            },
            {
                "nf": "%Y%m%d_ç",
                "aux": "folder",
                "expected": True
            },
            {
                "nf": "%Y%m%d_º^?*",
                "aux": "folder",
                "expected": False
            },
            {
                "nf": "%Y/%m/%d_º^?*",
                "aux": "",
                "expected": False
            }
        ]

        for sample in samples:
            result = name_formatter(sample["nf"], sample["aux"])
            self.assertEqual(sample["expected"], result, f"Error in {sample['nf']}")

    def test_recursive_search(self):
        """Test recursive_search function"""
        files = recursive_search("./src")
        newfiles = [x for x in files if "pycache" not in x and "pytest" not in x]

        self.assertSetEqual(
            {
                './src/test_main.py', './src/__init__.py',
                './src/__main__.py',
                './src/change_media_name/change_media_name.py',
                './src/colored_logger/colored_logger.py',
                './src/output_formatter/test_output_formatter.py',
                './src/output_formatter/output_formatter.py'
            },
            set(newfiles),
            "Error in recursive_search_test"
        )

    def test_not_recursive_search(self):
        """Test not_recursive_search function"""
        result = not_recursive_search("./src")

        self.assertSetEqual(
            {
                './src/test_main.py',
                './src/__init__.py',
                './src/__main__.py'
            },
            set(result),
            "Error in not_recursive_search_test"
        )

    def test_get_files(self):
        """Test get_files function"""
        samples = [
            {
                "paths": ["./src"],
                "recursive": True,
                "expected": {
                    './src/test_main.py',
                    './src/__init__.py',
                    './src/__main__.py',
                    './src/change_media_name/change_media_name.py',
                    './src/colored_logger/colored_logger.py',
                    './src/output_formatter/test_output_formatter.py',
                    './src/output_formatter/output_formatter.py'
                }
            },
            {
                "paths": ["./src"],
                "recursive": False,
                "expected": {
                    './src/test_main.py',
                    './src/__init__.py',
                    './src/__main__.py'
                }
            }
        ]

        for i, sample in enumerate(samples):
            files = get_files(sample["paths"], sample["recursive"])
            newfiles = [x for x in files if "pycache" not in x and "pytest" not in x]

            self.assertSetEqual(
                sample["expected"], set(newfiles), f"Error in {i}"
            )

    def test_get_filetypes(self):
        """Test get_filetypes function"""
        samples = [
            {
                "filetypes": [".jpg", ".png"],
                "only_images": False,
                "only_videos": False,
                "not_filetypes": [],
                "expected": {".jpg", ".png"}
            },
            {
                "filetypes": [".py"],
                "only_images": False,
                "only_videos": False,
                "not_filetypes": [],
                "expected": set()
            },
            {
                "filetypes": [],
                "only_images": True,
                "only_videos": False,
                "not_filetypes": [],
                "expected": {".jpg", ".jpeg", ".png", ".heic", ".webp"}
            },
            {
                "filetypes": [],
                "only_images": False,
                "only_videos": True,
                "not_filetypes": [],
                "expected": {".mp4", ".avi", ".mov"}
            },
            {
                "filetypes": [],
                "only_images": False,
                "only_videos": False,
                "not_filetypes": [],
                "expected": {".jpg", ".jpeg", ".png", ".heic", ".webp", '.mp4', '.avi', '.mov'}
            },
            {
                "filetypes": [".jpg", "png"],
                "only_images": False,
                "only_videos": False,
                "not_filetypes": [],
                "expected": {".jpg"}
            }
        ]

        for i, sample in enumerate(samples):
            result = get_filetypes(
                sample["filetypes"], sample["only_images"],
                sample["only_videos"], sample["not_filetypes"]
            )
            self.assertSetEqual(sample["expected"], set(result), f"Error in {i} sample")

    def test_get_scan_files(self):
        """Test get_scan_files function"""
        samples = [
            {
                "input_files": ["./src"],
                "recursive": True,
                "ignored_paths": [],
                "not_ignore_subfolders": False,
                "filetypes": [".py"],
                "expected":
                    {
                        './src/test_main.py',
                        './src/__init__.py',
                        './src/__main__.py',
                        './src/change_media_name/change_media_name.py',
                        './src/colored_logger/colored_logger.py',
                        './src/output_formatter/test_output_formatter.py',
                        './src/output_formatter/output_formatter.py'
                    }
            },
            {
                "input_files": ["./src"],
                "recursive": False,
                "ignored_paths": ["."],
                "not_ignore_subfolders": False,
                "filetypes": [],
                "expected": set()
            },
            {
                "input_files": ["./src"],
                "recursive": True,
                "ignored_paths": ["./src/change_media_name"],
                "not_ignore_subfolders": True,
                "filetypes": [".py"],
                "expected": {
                    './src/test_main.py',
                    './src/__init__.py',
                    './src/__main__.py',
                    './src/colored_logger/colored_logger.py',
                    './src/output_formatter/test_output_formatter.py',
                    './src/output_formatter/output_formatter.py'
                }
            },
            {
                "input_files": ["./src"],
                "recursive": True,
                "ignored_paths": ["./src/colored_logger"],
                "not_ignore_subfolders": False,
                "filetypes": [],
                "expected": set()
            }
        ]

        for i, sample in enumerate(samples):
            result = get_scan_files(
                sample["input_files"], sample["recursive"], sample["ignored_paths"],
                sample["not_ignore_subfolders"], sample["filetypes"]
            )
            self.assertSetEqual(sample["expected"], set(result), f"Error in {i}")


if __name__ == '__main__':
    unittest.main()
