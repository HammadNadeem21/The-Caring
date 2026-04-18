from PIL import Image
import numpy as np

# Load images
frame = Image.open('assets/images/index-banner-right-img.png').convert("RGBA")
# Convert to numpy array
frame_np = np.array(frame)

# Load user photo and resize to fill the frame
photo = Image.open('assets/images/new/TC_Images_ (7).png').convert("RGBA")

# Resize photo (keeping aspect ratio or crop) to match the frame size
# Crop the center of photo to match aspect ratio of frame
ph_w, ph_h = photo.size
fr_w, fr_h = frame.size
ph_aspect = ph_w / ph_h
fr_aspect = fr_w / fr_h

if ph_aspect > fr_aspect:
    # Photo is wider
    new_w = int(ph_h * fr_aspect)
    offset = (ph_w - new_w) // 2
    photo = photo.crop((offset, 0, offset + new_w, ph_h))
else:
    # Photo is taller
    new_h = int(ph_w / fr_aspect)
    offset = (ph_h - new_h) // 2
    photo = photo.crop((0, offset, ph_w, offset + new_h))

photo = photo.resize((fr_w, fr_h), Image.Resampling.LANCZOS)
photo_np = np.array(photo)

# Find the grey pixels. The exact color is around 219, 219, 219
# We'll allow a slight tolerance + check alpha is solid
r, g, b, a = frame_np[:,:,0], frame_np[:,:,1], frame_np[:,:,2], frame_np[:,:,3]
# Grey mask: pixels where R, G, B are between 210 and 230, and A is > 200
grey_mask = (r > 210) & (r < 240) & (g > 210) & (g < 240) & (b > 210) & (b < 240) & (a > 200)

# Replace the grey pixels in the frame with the photo's pixels
frame_np[grey_mask] = photo_np[grey_mask]

# Save the result
result = Image.fromarray(frame_np)
result.save('assets/images/new/banner-merged.png')
print('Merge completed.')
