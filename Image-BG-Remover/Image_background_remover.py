import rembg
from PIL import Image
import io


def remove_background_with_rembg(input_path, output_path):
    with open(input_path, "rb") as input_file:
        input_data = input_file.read()

    output_data = rembg.remove(input_data)

    with Image.open(io.BytesIO(output_data)) as output_image:
        output_image.save(output_path, "PNG")


# Example usage
input_path = "WhatsApp Image 2023-10-13 at 4.43.21 PM.jpeg"
output_path = "result.png"
remove_background_with_rembg(input_path, output_path)
