# Apply a more subtle distortion that only affects the squiggly lines
from PIL import Image
import numpy as np
import cv2
import imageio

image_np = cv2.imread("bg.jpeg")
# Convert image to grayscale to detect the figure
gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

# Use thresholding to create a mask for the figure
_, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

# Expand mask slightly to ensure full coverage of the figure
kernel = np.ones((5,5), np.uint8)
mask = cv2.dilate(mask, kernel, iterations=2)

# Invert mask (figure in white, background in black)
mask_inv = cv2.bitwise_not(mask)

# Separate figure and background
figure = cv2.bitwise_and(image_np, image_np, mask=mask)  # Extract figure
background = cv2.bitwise_and(image_np, image_np, mask=mask_inv)  # Extract background


# Generate frames with minimal color shift, focusing on line movement
frames = []
num_frames = 20

for i in range(num_frames):
    # Create a very fine displacement map for subtle line wiggle effect
    shift = (3 * np.sin(2 * np.pi * i / num_frames)).astype(np.int32)  # Small oscillation
    
    # Apply distortion only to fine details
    distorted_background = np.copy(background)
    for row in range(distorted_background.shape[0]):
        if row % 2 == 0:  # Only shift certain rows to create a wavy effect
            distorted_background[row] = np.roll(distorted_background[row], shift, axis=0)

    # Merge figure and subtly distorted background
    combined = cv2.add(distorted_background, figure)

    # Convert back to image format
    frame = Image.fromarray(combined)
    frames.append(frame)

# Save as a looping GIF
gif_path_subtle = "animated_subtle.gif"
imageio.mimsave(gif_path_subtle, frames, duration=0.1, loop=0)  # Loop infinitely

gif_path_subtle
