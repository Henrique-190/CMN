# ChangeMediaName
Tool that changes media files to its creation date.

## Usage
```
python3 ChangeMediaName.py -i <paths>
```

## Options

| Option 1 | Option 2              | Description                                                           |
|----------|-----------------------|-----------------------------------------------------------------------|
| h        | help                  | Show this help message and exit                                       |
| i        | input-files           | **Required**. File(s) or folder(s) to scan                            |
| v        | verbose               | Default: `False`. Verbose mode                                        |
| r        | recursive             | Default: `False`. Scan folders recursively                            |
| ni       | ignored-paths         | Default: `None`. Files or folders to be ignored                       |
| nr       | not-ignore-subfolders | Default: `True`. Choose to not ignore subfolders of the ignored paths |
| t        | file-types            | Default: `None`. List of file types to consider                       |
| nt       | not-file-types        | Default: `None`. List of file types to ignore                         |
| of       | only-images           | Default: `False`. Consider only images                                |
| ov       | only-videos           | Default: `False`. Consider only videos                                |
| cf       | create-new-folders    | Default: `False`. Create new folders according to the new image names |
| fn       | name-format           | Default:`%Y%m%d_%H%M%S` Format of the new names                       |
| ff       | name-folder-format    | Default:`%Y - %m - %d`. Format of the new folder names                |


## Supported file types
| Type  | Extension | Name                                         |
|-------|-----------|----------------------------------------------|
| Image | HEIC      | High Efficiency Image File Format            |
| Image | JPEG      | Joint Photographic Experts Group File Format |
| Image | JPG       | Joint Photographic Group File Format         |
| Image | PNG       | Portable Network Graphics File Format        |
| Image | WEBP      | WebP Image File Format                       |
| Video | AVI       | Audio Video Interleave                       |
| Video | AVI       | Audio Video Interleave                       |
| Video | MP4       | MPEG-4 Part 14                               |

## Requirements
- Install `exiftool` command from https://exiftool.org/. Credits to Phil Harvey.

## Made by me :)
