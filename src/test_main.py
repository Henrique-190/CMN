import unittest

from cmn import *


class MainTest(unittest.TestCase):
    def test_nameFormatter(self):
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
            result = nameFormatter(sample["nf"], sample["aux"])
            self.assertEqual(result, sample["expected"], f"Error in {sample['nf']}")

    def test_recursiveSearch(self):
        files = recursiveSearch("./src")
        newfiles = [x for x in files if "pycache" not in x and "pytest" not in x]

        self.assertSetEqual(set(newfiles),
                            {'./src/test_main.py', './src/cmn/__init__.py', './src/cmn/__main__.py', './src/ChangeMediaName/ChangeMediaName.py',
                             './src/ColoredLogger/ColoredLogger.py', './src/OutputFormatter/test_OutputFormatter.py',
                             './src/OutputFormatter/OutputFormatter.py'},
                            "Error in recursiveSearch_test"
                            )

    def test_notRecursiveSearch(self):
        result = notRecursiveSearch("./src")

        self.assertSetEqual(set(result),
                            {'./src/test_main.py'},
                            "Error in notRecursiveSearch_test"
                            )

    def test_getFiles(self):
        samples = [
            {
                "paths": ["./src"],
                "recursive": True,
                "expected": {
                    './src/test_main.py',
                    './src/cmn/__init__.py',
                    './src/cmn/__main__.py',
                    './src/ChangeMediaName/ChangeMediaName.py',
                    './src/ColoredLogger/ColoredLogger.py',
                    './src/OutputFormatter/test_OutputFormatter.py',
                    './src/OutputFormatter/OutputFormatter.py'
                }
            },
            {
                "paths": ["./src"],
                "recursive": False,
                "expected": {'./src/test_main.py'}
            }
        ]

        for sample in samples:
            files = getFiles(sample["paths"], sample["recursive"])
            newfiles = [x for x in files if "pycache" not in x and "pytest" not in x]

            self.assertSetEqual(set(newfiles), sample["expected"], f"Error in {sample['paths']}")

    def test_getFiletypes(self):
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

        for i in range(0, len(samples)):
            sample = samples[i]
            result = getFiletypes(sample["filetypes"], sample["only_images"], sample["only_videos"],
                                  sample["not_filetypes"])
            self.assertSetEqual(sample["expected"], set(result), f"Error in {i} sample")

    def test_getScanFiles(self):
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
                        './src/cmn/__init__.py',
                        './src/cmn/__main__.py',
                        './src/ChangeMediaName/ChangeMediaName.py',
                        './src/ColoredLogger/ColoredLogger.py',
                        './src/OutputFormatter/test_OutputFormatter.py',
                        './src/OutputFormatter/OutputFormatter.py'
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
                "ignored_paths": ["./src/ChangeMediaName"],
                "not_ignore_subfolders": True,
                "filetypes": [".py"],
                "expected": {
                    './src/test_main.py',
                    './src/cmn/__init__.py',
                    './src/cmn/__main__.py',
                    './src/ColoredLogger/ColoredLogger.py',
                    './src/OutputFormatter/test_OutputFormatter.py',
                    './src/OutputFormatter/OutputFormatter.py'
                }
            },
            {
                "input_files": ["./src"],
                "recursive": True,
                "ignored_paths": ["./src/ColoredLogger"],
                "not_ignore_subfolders": False,
                "filetypes": [],
                "expected": set()
            }
        ]

        for sample in samples:
            result = getScanFiles(sample["input_files"], sample["recursive"], sample["ignored_paths"],
                                  sample["not_ignore_subfolders"], sample["filetypes"])
            self.assertSetEqual(sample["expected"], set(result), f"Error in {sample['input_files']}")


if __name__ == '__main__':
    unittest.main()
