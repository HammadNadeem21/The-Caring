from PIL import Image

# Load images
frame = Image.open('assets/images/index-banner-right-img.png').convert("RGBA")
photo = Image.open('assets/images/new/TC_Images_ (7).png').convert("RGBA")

# Resize photo (keeping aspect ratio or crop) to match the frame size
ph_w, ph_h = photo.size
fr_w, fr_h = frame.size
ph_aspect = ph_w / ph_h
fr_aspect = fr_w / fr_h

if ph_aspect > fr_aspect:
    new_w = int(ph_h * fr_aspect)
    offset = (ph_w - new_w) // 2
    photo = photo.crop((offset, 0, offset + new_w, ph_h))
else:
    new_h = int(ph_w / fr_aspect)
    offset = (ph_h - new_h) // 2
    photo = photo.crop((0, offset, ph_w, offset + new_h))

photo = photo.resize((fr_w, fr_h), Image.Resampling.LANCZOS)

frame_data = frame.load()
photo_data = photo.load()

# Find and replace grey pixels
for y in range(fr_h):
    for x in range(fr_w):
        r, g, b, a = frame_data[x, y]
        # Check if the pixel is gray (e.g. 210-230 range)
        if 210 < r < 230 and 210 < g < 230 and 210 < b < 230 and a > 200:
            frame_data[x, y] = photo_data[x, y]

frame.save('assets/images/new/banner-merged.png')
print('Merge completed successfully.')
