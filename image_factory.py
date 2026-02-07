"""
Image Factory - 4K Cover Image Generation & LSB Steganography
Fully Offline - No API Required
"""

import io
import os
import random
from PIL import Image
from stegano import lsb


class ImageFactory:
    """
    Offline image generation and steganography engine.
    Resolution: 4K (3840x2160) for maximum capacity.
    Capacity: ~2.5-3 MB depending on compression.
    """
    
    # 4K resolution stock image service (offline fallback available)
    STOCK_URL_TEMPLATE = "https://picsum.photos/seed/{}/3840/2160"
    
    # Fallback: Local gradient generation
    GRADIENT_COLORS = [
        ("#0a0a0a", "#1a4d2e"),  # Dark green
        ("#0f0f23", "#1e3a8a"),  # Dark blue
        ("#1a1a2e", "#16213e"),  # Navy
        ("#0d1117", "#1f2937"),  # GitHub dark
        ("#000000", "#2d3748"),  # Charcoal
    ]

    def generate_cover_image(self) -> Image.Image:
        """
        Generate a 4K cover image for steganography.
        Priority: Online stock photo > Offline gradient
        """
        # Try online first (for better aesthetics)
        try:
            import requests
            seed = random.randint(1, 999999)
            print(f"Downloading 4K stock image (seed: {seed})...")
            
            response = requests.get(
                self.STOCK_URL_TEMPLATE.format(seed),
                timeout=30
            )
            response.raise_for_status()
            return Image.open(io.BytesIO(response.content))
            
        except Exception as e:
            print(f"Online source unavailable: {e}")
            print("Generating offline gradient image...")
            return self._generate_gradient_image()
    
    def _generate_gradient_image(self) -> Image.Image:
        """Generate a gradient image offline (fallback)."""
        width, height = 3840, 2160
        img = Image.new('RGB', (width, height))
        pixels = img.load()
        
        # Random color scheme
        start_color, end_color = random.choice(self.GRADIENT_COLORS)
        
        # Parse hex colors
        r1, g1, b1 = self._hex_to_rgb(start_color)
        r2, g2, b2 = self._hex_to_rgb(end_color)
        
        # Create vertical gradient
        for y in range(height):
            ratio = y / height
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            
            for x in range(width):
                # Add subtle noise for better steganography
                noise = random.randint(-5, 5)
                pixels[x, y] = (
                    max(0, min(255, r + noise)),
                    max(0, min(255, g + noise)),
                    max(0, min(255, b + noise))
                )
        
        return img
    
    @staticmethod
    def _hex_to_rgb(hex_color: str) -> tuple:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    @staticmethod
    def embed_data(image: Image.Image, secret_data: bytes) -> Image.Image:
        """
        Embed encrypted data into image using LSB steganography.
        
        Args:
            image: Cover image
            secret_data: Data to hide
            
        Returns:
            Image with embedded data
        """
        hex_data = secret_data.hex()
        
        # Capacity check
        max_capacity_chars = image.width * image.height
        current_chars = len(hex_data)
        
        print(f"Data size: {current_chars:,} chars | Capacity: {max_capacity_chars:,} pixels")
        
        if current_chars > max_capacity_chars:
            size_mb = len(secret_data) / (1024 * 1024)
            raise ValueError(
                f"FILE TOO LARGE!\n"
                f"Size: {size_mb:.2f} MB\n"
                f"Maximum: ~2.5 MB\n"
                f"Please use a smaller file or compress it first."
            )
        
        # Embed data
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        
        return lsb.hide(buffer, hex_data)

    @staticmethod
    def extract_data(image_path: str) -> bytes:
        """
        Extract hidden data from steganography image.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Extracted data as bytes
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        hex_data = lsb.reveal(image_path)
        
        if not hex_data:
            raise ValueError("No hidden data found in this image.")
        
        return bytes.fromhex(hex_data)
