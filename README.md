# Image Watermarking Tool

A Python tool for adding watermarks to images in batch processing mode.

## Features

| Feature            | Description                                                                  |
|--------------------|------------------------------------------------------------------------------|
| Batch Processing   | Add text watermarks to single images or entire directories                   |
| Customization      | Customize watermark appearance including text, rotation, color, and opacity |
| Image Preservation | Original images are preserved with watermarked versions in a separate directory |
| Error Handling     | Robust error handling and detailed logging                                  |

## Requirements

| Package  | Version |
|----------|---------|
| Python   | >= 3.6  |
| Pillow   | >= 9.0.0 |
| pathlib  | >= 1.0.1 |

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Arthur469/pywatermark.git
cd image-watermarker
```
   
2. Create a virtual environment and activate it:

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix/MacOS
source venv/bin/activate
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

## Usage
### Basic Usage
To watermark all images in a directory:

```bash
python watermark.py --input "path/to/images" --output "path/to/output" --text "My Watermark"
```

### Advanced Options
```bash
python watermark.py --input "path/to/images" \
                    --output "path/to/output" \
                    --text "Copyright 2024" \
                    --angle 45 \
                    --opacity 0.4 \
                    --color "white"
```

### Command Line Arguments 
| Argument | Description | Default |
|-----------|---------------------------------------|-------------|
| --input | Input image or directory path | Required|
| --output | Output directory path | Required|
| --text | Watermark text content | Required|
| --angle | Rotation angle of watermark (degrees) | 0 |
| --opacity | Watermark opacity (0 to 255) | 128 |
| --color | Text color (hex code) | (255, 255, 255) |
| --font | Font file path | Arial.ttf |
| --size | Font size in pixels | 36 |

## Examples
1. Simple watermark on a single image:

```bash
python main.py --input "photo.jpg" --output "output" --text "© 2024"
```

2. Batch process with custom styling:

```bash
python watermark.py --input "photos" --output "watermarked" --text "CONFIDENTIAL" --angle 45 --color "red" --opacity 0.3
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
Built with Pillow for image processing.
Inspired by the need for simple, batch watermarking solutions.

This structured `README.md` includes installation steps, usage examples, command-line options, and additional information based on the provided data. Let me know if you’d like further adjustments!
