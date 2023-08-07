import re

months = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12"
}


class OutputFormatter:
    def __init__(self, output: str, expressions: list[str]):
        self.output = output
        self.expressions = expressions

    def format(self) -> tuple:
        for expression in self.expressions:
            match = re.search(expression, self.output)
            if match:
                groups = match.groups()
                if (1957 <= int(groups[0]) and 1 <= int(groups[1]) <= 12 and 1 <= int(groups[2]) <= 31 and
                        0 <= int(groups[3]) <= 23 and 0 <= int(groups[4]) <= 59 and 0 <= int(groups[5]) <= 59):
                    return groups
        return ()

    def refactor(self, groups: tuple) -> tuple:
        return groups

    def getGroups(self):
        return self.refactor(self.format())


class AVIformatter(OutputFormatter):
    def __init__(self, output: str):
        super().__init__(output, [
            r"Date\s*Time\s*\d\s*:\s*\w{3}\s*(\w{3})\s*(\d{1,2})\s*(\d{2}):(\d{2}):(\d{2})\s*(\d{4})",
        ])

    def format(self) -> tuple:
        for expression in self.expressions:
            match = re.search(expression, self.output)
            if match:
                groups = match.groups()
                if groups[0] in months.keys() and 1 <= int(groups[1]) <= 31 and 0 <= int(groups[2]) <= 23 and \
                        0 <= int(groups[3]) <= 59 and 0 <= int(groups[4]) <= 59 and 1957 <= int(groups[5]):
                    return groups
        return ()

    def refactor(self, groups: tuple) -> tuple:
        if groups:
            return groups[5], months[groups[0]], groups[1], groups[2], groups[3], groups[4]
        return ()

    def getGroups(self):
        return self.refactor(self.format())


class ImageRegularformatter(OutputFormatter):
    def __init__(self, output: str):
        super().__init__(output, [
            r"Date/Time Original\s*:\s*(\d{4}):(\d{2}):(\d{2})\s*(\d{2}):(\d{2}):(\d{2})\.(\d{3})",
            r"Create Date\s+:\s(\d{4}):(\d{2}):(\d{2})\s*(\d{2}):(\d{2}):(\d{2})\.(\d{3})",
            r"Date/Time Original\s*:\s*(\d{4}):(\d{2}):(\d{2})\s*(\d{2}):(\d{2}):(\d{2})",
            r"Create Date\s+:\s(\d{4}):(\d{2}):(\d{2})\s*(\d{2}):(\d{2}):(\d{2})"
        ])


class VideoRegularformatter(OutputFormatter):
    def __init__(self, output: str):
        super().__init__(output, [
            r"Media Create Date\s+:\s(\d{4}):(\d{2}):(\d{2})\s*(\d{2}):(\d{2}):(\d{2})\.(\d{3})",
            r"Media Create Date\s+:\s(\d{4}):(\d{2}):(\d{2})\s*(\d{2}):(\d{2}):(\d{2})"
        ])
