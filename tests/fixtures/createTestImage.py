from PIL import Image

filename = "tests/fixtures/assets/image.png"

# Image settings
width, height = 100, 100
color = (255, 0, 0)  # Red

# Create image
img = Image.new("RGB", (width, height), color)
img.save(filename)

print(f"Image saved as {filename}")
