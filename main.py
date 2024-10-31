from typing import Optional, Union
from pathlib import Path
from watermark import ImageWatermarker
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Example usage of watermark processing."""
    try:
        # Create watermarker instance
        watermarker = ImageWatermarker()
        
        # Process all images in a directory
        watermarker.process_directory(
            "input_images",
            "© My Company 2023",
            output_dir="output_images",
            rotation_angle=-30,
            font_color=(255, 255, 255),
            opacity=128
        )
        
        logger.info("Watermark processing completed successfully!")
        
    except Exception as e:
        logger.error(f"Failed to process directory: {str(e)}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main())
