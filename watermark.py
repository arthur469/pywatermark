#!/usr/bin/env python3

import os
import logging
from PIL import Image, ImageDraw, ImageFont
from typing import Optional, Union, Tuple, List, Dict
from pathlib import Path
import math

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ImageWatermarker:
    """A class to add watermarks to images.
    
    This class provides functionality to add text watermarks to images while supporting
    various image formats and providing robust error handling.
    """
    
    DEFAULT_GRID_SIZE = (3, 3)  # Default rows, columns
    DEFAULT_ROTATION = -30  # Default rotation angle in degrees
    DEFAULT_SPACING = 1.5  # Default spacing factor between watermarks
    DEFAULT_FONT_SIZE = 36  # Default font size
    DEFAULT_FONT_COLOR = (255, 255, 255)  # Default RGB color (white)
    DEFAULT_OPACITY = 128  # Default opacity (0-255)
    DEFAULT_MIN_GRID = 2  # Minimum grid size
    DEFAULT_MAX_GRID = 4  # Maximum grid size
    DEFAULT_TARGET_SIZE_RATIO = 4  # Target watermark size ratio
    DEFAULT_INITIAL_SIZE_RATIO = 15  # Initial font size ratio
    
    def __init__(self):
        """Initialize the ImageWatermarker."""
        pass

    def _get_font(self, font_size: int, font_path: Optional[str] = None):
        """Helper method to get font with specified size.
        
        Args:
            font_size (int): Size of the font
            font_path (str, optional): Path to custom font file
        
        Returns:
            ImageFont: Font object to use for watermark
        """
        if font_path is None:
            try:
                # Try to find a system font that supports size changes
                try:
                    # Try to use Arial or a similar font on the system
                    system_font = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # Common on Linux
                    if os.path.exists(system_font):
                        return ImageFont.truetype(system_font, font_size)
                    else:
                        # On Windows, try Arial
                        return ImageFont.truetype("arial.ttf", font_size)
                except:
                    logger.warning("Could not load system font, falling back to default")
                    font = ImageFont.load_default()
                    logger.warning("Default font may not support size changes")
                    return font
            except Exception as e:
                logger.error(f"Could not load default font: {str(e)}")
                raise
        else:
            try:
                return ImageFont.truetype(font_path, font_size)
            except Exception as e:
                logger.error(f"Could not load font from {font_path}: {str(e)}")
                raise

    def _calculate_optimal_parameters(
        self,
        image_path: Union[str, Path],
        watermark_text: str,
        font_path: Optional[str] = None,
        min_grid: int = DEFAULT_MIN_GRID,
        max_grid: int = DEFAULT_MAX_GRID,
        target_size_ratio: int = DEFAULT_TARGET_SIZE_RATIO,
        initial_size_ratio: int = DEFAULT_INITIAL_SIZE_RATIO
    ) -> Dict[str, Union[Tuple[int, int], int, float]]:
        """Calculate optimal grid size, font size and spacing based on image dimensions.
        
        Args:
            image_path (str or Path): Path to the input image
            watermark_text (str): Text to use as watermark
            font_path (str, optional): Path to custom font file
            min_grid (int): Minimum number of rows/columns
            max_grid (int): Maximum number of rows/columns
            target_size_ratio (int): Target watermark size as fraction of image dimension
            initial_size_ratio (int): Initial font size as fraction of image dimension
            
        Returns:
            dict: Dictionary containing optimal parameters:
                - grid_size: Tuple of (rows, columns)
                - font_size: Optimal font size
                - spacing_factor: Optimal spacing between watermarks
        """
        # Get image dimensions
        with Image.open(image_path) as img:
            width, height = img.size
        
        # Calculate initial font size based on dimensions
        initial_font_size = min(width, height) // initial_size_ratio
        font = self._get_font(initial_font_size, font_path)
        
        # Get initial text size
        bbox = ImageDraw.Draw(Image.new('RGBA', (1, 1))).textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Calculate optimal font size based on image dimensions
        target_size = min(width, height) / target_size_ratio
        scale_factor = target_size / max(text_width, text_height)
        optimal_font_size = int(initial_font_size * scale_factor)
        
        # Recalculate text size with optimal font
        optimal_font = self._get_font(optimal_font_size, font_path)
        bbox = ImageDraw.Draw(Image.new('RGBA', (1, 1))).textbbox((0, 0), watermark_text, font=optimal_font)
        optimal_text_width = bbox[2] - bbox[0]
        optimal_text_height = bbox[3] - bbox[1]
        
        # Calculate grid dimensions with fewer cells
        cols = max(min_grid, int(width / (optimal_text_width * 2)))
        rows = max(min_grid, int(height / (optimal_text_height * 2.5)))
        
        # Limit maximum grid size
        rows = min(rows, max_grid)
        cols = min(cols, max_grid)
        
        # Calculate optimal spacing factor
        spacing_factor = 1.8 + (min(width, height) / max(width, height)) * 0.4
        
        return {
            'grid_size': (rows, cols),
            'font_size': optimal_font_size,
            'spacing_factor': spacing_factor
        }

    def add_watermark(
        self,
        image_path: Union[str, Path],
        watermark_text: str,
        output_path: Optional[Union[str, Path]] = None,
        grid_size: Tuple[int, int] = DEFAULT_GRID_SIZE,
        rotation_angle: int = DEFAULT_ROTATION,
        spacing_factor: float = DEFAULT_SPACING,
        font_size: int = DEFAULT_FONT_SIZE,
        font_color: Tuple[int, int, int] = DEFAULT_FONT_COLOR,
        opacity: int = DEFAULT_OPACITY,
        font_path: Optional[str] = None
    ) -> None:
        """Add a grid of watermarks to an image.
        
        Args:
            image_path (str or Path): Path to the input image
            watermark_text (str): Text to use as watermark
            output_path (str or Path, optional): Path for output image
            grid_size (tuple): Number of rows and columns in the grid
            rotation_angle (int): Angle to rotate watermarks in degrees
            spacing_factor (float): Factor to control spacing between watermarks
            font_size (int): Size of the watermark text
            font_color (tuple): RGB color tuple for watermark
            opacity (int): Opacity of watermark (0-255)
            font_path (str, optional): Path to custom font file
        """
        try:
            # Get font for this watermark
            font = self._get_font(font_size, font_path)

            # Convert paths to Path objects
            image_path = Path(image_path)
            if output_path is None:
                output_path = image_path
            else:
                output_path = Path(output_path)

            if not image_path.exists():
                raise ValueError(f"Input image not found: {image_path}")

            logger.info(f"Opening image: {image_path}")
            with Image.open(image_path) as img:
                # Convert to RGBA to support transparency
                img = img.convert('RGBA')
                
                # Create transparent overlay
                overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
                draw = ImageDraw.Draw(overlay)

                # Calculate watermark size
                bbox = draw.textbbox((0, 0), watermark_text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                # Calculate grid spacing
                rows, cols = grid_size
                cell_width = img.width / cols
                cell_height = img.height / rows

                # Adjust spacing based on text size and spacing factor
                x_spacing = max(cell_width, text_width * spacing_factor)
                y_spacing = max(cell_height, text_height * spacing_factor)

                # Create a new image for the rotated text
                txt_img = Image.new('RGBA', img.size, (0, 0, 0, 0))
                txt_draw = ImageDraw.Draw(txt_img)

                # Create RGBA color tuple with user-specified opacity
                font_color_rgba = (*font_color, opacity)

                # Draw watermarks in a grid pattern
                for row in range(rows):
                    for col in range(cols):
                        # Calculate center position for this grid cell
                        x = (col * x_spacing + x_spacing/2) % img.width
                        y = (row * y_spacing + y_spacing/2) % img.height
                        
                        # Create a new image for each rotated watermark
                        text_overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
                        text_draw = ImageDraw.Draw(text_overlay)
                        
                        # Draw the text
                        text_draw.text(
                            (x - text_width/2, y - text_height/2),
                            watermark_text,
                            font=font,
                            fill=font_color_rgba
                        )
                        
                        # Rotate the text
                        rotated_text = text_overlay.rotate(
                            rotation_angle,
                            expand=False,
                            center=(x, y)
                        )
                        
                        # Composite the rotated text onto the main overlay
                        overlay = Image.alpha_composite(overlay, rotated_text)

                # Combine original image with watermark overlay
                watermarked = Image.alpha_composite(img, overlay)

                # Convert back to RGB before saving as JPEG
                if output_path.suffix.lower() in ['.jpg', '.jpeg']:
                    watermarked = watermarked.convert('RGB')

                # Save the watermarked image
                logger.info(f"Saving watermarked image to: {output_path}")
                watermarked.save(output_path)

        except (ValueError, IOError) as e:
            logger.error(f"Error processing image: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise

    def process_directory(self, input_dir: Union[str, Path], watermark_text: str, output_dir: Optional[Union[str, Path]] = None, **kwargs) -> None:
        """Process all images in a directory and add watermarks using optimal parameters.
        
        Args:
            input_dir (Union[str, Path]): Directory containing input images
            watermark_text (str): Text to use as watermark
            output_dir (Optional[Union[str, Path]], optional): Output directory for watermarked images. 
                If None, will create 'watermarked' subdirectory in input_dir.
            **kwargs: Additional parameters to pass to add_watermark()
        
        Raises:
            ValueError: If input directory doesn't exist
            IOError: If there are issues processing images
        """
        input_dir = Path(input_dir)
        if not input_dir.exists():
            raise ValueError(f"Input directory does not exist: {input_dir}")
            
        if output_dir is None:
            output_dir = input_dir / 'watermarked'
        else:
            output_dir = Path(output_dir)
            
        output_dir.mkdir(exist_ok=True, parents=True)
        
        # Get all image files
        image_extensions = ['.jpg', '.jpeg', '.png']
        image_files = []
        for ext in image_extensions:
            image_files.extend(input_dir.glob(f'*{ext}'))
            image_files.extend(input_dir.glob(f'*{ext.upper()}'))
        
        if not image_files:
            logger.warning(f"No image files found in {input_dir}")
            return
            
        logger.info(f"Found {int(len(image_files)/2)} images to process")
        
        for img_path in image_files:
            try:
                output_path = output_dir / img_path.name
                
                # Calculate optimal parameters for each image
                optimal_params = self._calculate_optimal_parameters(
                    str(img_path),
                    watermark_text
                )
                
                # Update with any user-provided parameters
                optimal_params.update(kwargs)
                
                # Add watermark
                self.add_watermark(
                    str(img_path),
                    watermark_text,
                    str(output_path),
                    **optimal_params
                )
                
                logger.info(f"Successfully processed: {img_path.name}")
                
            except Exception as e:
                logger.error(f"Failed to process {img_path.name}: {str(e)}")
                continue

