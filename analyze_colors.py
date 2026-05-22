from PIL import Image
import numpy as np

img = Image.open('extracted_palette.webp')
img = img.convert('RGB')
colors = np.array(img).reshape(-1, 3)
unique_colors, counts = np.unique(colors, axis=0, return_counts=True)

# Sort by count desc
sorted_indices = np.argsort(-counts)
print("Top colors:")
for idx in sorted_indices[:30]:
    color = unique_colors[idx]
    count = counts[idx]
    # Check if it looks green: G > R and G > B
    is_green = color[1] > color[0] and color[1] > color[2]
    tag = "[GREEN]" if is_green else ""
    print(f"RGB: {color} - Count: {count} {tag}")
