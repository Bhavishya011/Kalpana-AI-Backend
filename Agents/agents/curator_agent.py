# agents/curator_agent.py
"""
🎨 The Curator Agent (Fixed for SDK v1.111.0)
- Uses correct parameter names (base_image instead of image)
- Removed unsupported output_resolution
- Added optional upscaling method
- Fixed VertexImage loading issues
"""

import io
import os
import numpy as np
from google.cloud import vision
from PIL import Image
import cv2
import vertexai

# ONLY import what exists in your SDK
from vertexai.preview.vision_models import ImageGenerationModel
from vertexai.preview.vision_models import Image as VertexImage  # Correct wrapper


class CuratorAgent:
    def __init__(self):
        vertexai.init(project="nodal-fountain-470717-j1", location="us-central1")
        self.model = ImageGenerationModel.from_pretrained(
            "imagen-4.0-generate-001"
        )
        self.vision_client = vision.ImageAnnotatorClient()

    def detect_product(self, image_path: str):
        """Detect main product using Vision API"""
        with open(image_path, "rb") as f:
            content = f.read()
        image = vision.Image(content=content)
        response = self.vision_client.object_localization(image=image)
        objects = response.localized_object_annotations
        if not objects:
            raise ValueError("No product detected")
        return max(objects, key=lambda x: x.score)

    def create_mask(self, image_path: str, buffer: int = 3) -> Image.Image:
        """Create mask: BLACK = keep, WHITE = replace"""
        img = Image.open(image_path)
        width, height = img.size
        mask = np.ones((height, width), dtype=np.uint8) * 255  # White background

        product = self.detect_product(image_path)
        vertices = [
            (int(v.x * width), int(v.y * height))
            for v in product.bounding_poly.normalized_vertices
        ]
        cv2.fillPoly(mask, [np.array(vertices)], 0)  # Black fill

        kernel = np.ones((buffer, buffer), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=1)
        
        # Convert grayscale mask to RGB for compatibility
        mask_pil = Image.fromarray(mask)
        if mask_pil.mode != 'RGB':
            mask_rgb = Image.new('RGB', mask_pil.size)
            mask_rgb.paste(mask_pil)
            return mask_rgb
        return mask_pil

    def enhance(self, image_path: str, prompt: str, upscale: bool = False) -> Image.Image:
        """
        Enhance image with inpainting.
        - Uses base_image + mask
        - No output_resolution (not supported in v1.111.0)
        - Optional upscaling after generation
        """
        # Load original image and mask
        pil_image = Image.open(image_path)
        pil_mask = self.create_mask(image_path)

        # Save mask temporarily
        temp_mask_path = "temp_mask.png"
        pil_mask.save(temp_mask_path)

        # Load images using VertexImage.load_from_file (most reliable method)
        vertex_image = VertexImage.load_from_file(image_path)
        vertex_mask = VertexImage.load_from_file(temp_mask_path)

        # Call with correct params
        images = self.model.edit_image(
            prompt=prompt,
            base_image=vertex_image,
            mask=vertex_mask,
            edit_mode="inpainting-insert",
            output_mime_type="image/png",
            seed=42,
        )

        result = images[0]

        # Clean up temporary file
        try:
            os.remove(temp_mask_path)
        except:
            pass

        # Optional upscale
        if upscale:
            upscaled = self.model.upscale_image(
                image=result,
                new_size=4096,  # Adjust to desired size
                output_mime_type="image/png",
            )
            return upscaled[0]

        return result

    def create_studio_shot(self, image_path: str, upscale: bool = False) -> Image.Image:
        prompt = "Crisp and clean e-commerce product photo for a web catalog. Shot in a perfectly lit light box, ensuring even, shadowless illumination. The product is centered on a pure white (#FFFFFF) background. Optimized for digital display, vibrant colors, tack-sharp focus."
        return self.enhance(image_path, prompt, upscale=upscale)

    def create_lifestyle_mockup(self, image_path: str, upscale: bool = False) -> Image.Image:
        prompt = "Dramatic studio product photography. A single, powerful key light creates deep, elegant shadows, emphasizing the product's form and texture. Shot with a prime lens for exquisite detail and a shallow depth of field. The background is a sophisticated, non-reflective matte grey. Cinematic quality, ultra-detailed."
        return self.enhance(image_path, prompt, upscale=upscale)