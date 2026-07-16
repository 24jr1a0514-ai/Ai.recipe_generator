from PIL import Image
import io
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class ImageProcessor:
    MAX_SIZE = (1024, 1024)
    SUPPORTED_FORMATS = {'PNG', 'JPG', 'JPEG', 'WEBP', 'GIF'}
    
    @staticmethod
    def validate_image(uploaded_file) -> bool:
        """Validate uploaded image"""
        try:
            if uploaded_file is None:
                return False
            
            if uploaded_file.type.split('/')[-1].upper() not in ImageProcessor.SUPPORTED_FORMATS:
                return False
            
            img = Image.open(uploaded_file)
            img.verify()
            return True
        except Exception as e:
            logger.error(f"Image validation error: {str(e)}")
            return False
    
    @staticmethod
    def resize_image(uploaded_file, max_size: tuple = MAX_SIZE) -> Image.Image:
        """Resize image to max size"""
        try:
            img = Image.open(uploaded_file)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            return img
        except Exception as e:
            logger.error(f"Image resize error: {str(e)}")
            raise
    
    @staticmethod
    def convert_to_bytes(image: Image.Image, format: str = "PNG") -> bytes:
        """Convert PIL image to bytes"""
        try:
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format=format)
            img_byte_arr.seek(0)
            return img_byte_arr.getvalue()
        except Exception as e:
            logger.error(f"Image conversion error: {str(e)}")
            raise
    
    @staticmethod
    def get_image_info(uploaded_file) -> dict:
        """Get image information"""
        try:
            img = Image.open(uploaded_file)
            return {
                "format": img.format,
                "size": img.size,
                "mode": img.mode,
                "width": img.width,
                "height": img.height
            }
        except Exception as e:
            logger.error(f"Error getting image info: {str(e)}")
            return {}