import unittest

from output_formatter import ImageRegularformatter, VideoRegularformatter, AVIformatter


class OutputFormatterTest(unittest.TestCase):
    def test_getDateTime(self):
        samples = [
            {
                "output": "Track Create Date               : 0000:00:00 00:00:00",
                "formatter": VideoRegularformatter,
                "expected": ()
            },
            {
                "output": "Track Create Date               : 0000:00:00 00:00:00",
                "formatter": AVIformatter,
                "expected": ()
            },
            {
                "output": "Track Create Date               : 0000:00:00 00:00:00",
                "formatter": ImageRegularformatter,
                "expected": ()
            },
            {
                "output": "Track Create Date               : 0000:00:00 00:00:00",
                "formatter": VideoRegularformatter,
                "expected": ()
            },
            {
                "output": "Track Create Date               : 0000:00:00 00:00:00",
                "formatter": AVIformatter,
                "expected": ()
            },
            {
                "output": "Track Create Date               : 0000:00:00 00:00:00",
                "formatter": ImageRegularformatter,
                "expected": ()
            },
            {
                "output": "Date/Time Original                    : 2023:07:16 17:13:57",
                "formatter": VideoRegularformatter,
                "expected": ()
            },
            {
                "output": "Date/Time Original                    : 2023:07:16 17:13:57",
                "formatter": AVIformatter,
                "expected": ()
            },
            {
                "output": "Date/Time Original                    : 2023:07:16 17:13:57",
                "formatter": ImageRegularformatter,
                "expected": ("2023", "07", "16", "17", "13", "57")
            },
        ]
        for i in range(0, len(samples)):
            actual = samples[i]["formatter"](samples[i]["output"]).getGroups()
            self.assertEqual(actual, samples[i]["expected"], f"Error in {samples[i]}")


if __name__ == '__main__':
    unittest.main()
