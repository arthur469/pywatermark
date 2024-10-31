
# Image Watermarking Tool

A Python tool for adding customizable text watermarks to images with optimal positioning, sizing, and styling. This tool preserves the original images by saving watermarked versions in a separate directory and includes robust error handling and logging.

## Features

- **Batch Processing**: Apply watermarks to a single image or an entire directory.
- **Customizable Watermarks**: Configure text, color, rotation angle, spacing, font size, and opacity.
- **Adaptive Sizing**: Automatically calculates the optimal grid and font size based on each image's dimensions.
- **Error Handling and Logging**: Detailed logging and robust error handling for a reliable experience.

## Requirements

| Package | Version |
|---------|---------|
| Python  | >= 3.6  |
| Pillow  | >= 9.0.0 |
| pathlib | >= 1.0.1 |

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/arthur469/pywatermark.git
   cd image-watermarker
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Unix/MacOS
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

To watermark all images in a directory, modify the `main.py` script or use the following command format:

```python
python main.py
```

This script will watermark images found in the `input_images` directory with the text "© My Company 2023" and save the watermarked versions to `output_images`.

### Customization Options

Use the `ImageWatermarker` class in `watermark.py` to configure advanced settings, such as:

- `rotation_angle`: Rotate watermarks to a custom angle.
- `font_color`: Set text color (RGB tuple).
- `opacity`: Control watermark transparency (0-255).
- `grid_size`: Adjust the number of watermark repetitions across the image.

### Example Usage

```python
from watermark import ImageWatermarker

watermarker = ImageWatermarker()
watermarker.process_directory(
    input_dir="input_images",
    watermark_text="© 2023",
    output_dir="output_images",
    rotation_angle=-30,
    font_color=(255, 255, 255),
    opacity=128
)
```

## Contributing

Contributions are welcome! Please submit a pull request with your suggested improvements or fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments

- Built with [Pillow](https://python-pillow.org/) for image manipulation.
- Inspired by the need for efficient and customizable watermarking solutions.
