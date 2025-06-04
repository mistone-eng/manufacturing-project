import cv2

# image of tulips and a butterflu
image_path = 'C:/Users/Stella Barraza/Downloads/OpenCV/images/tulips.jpg.webp'  

# Load the image
img = cv2.imread(image_path)
if img is None:
    print(f"Error: Could not load image from {image_path}")
    exit()

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection
edges = cv2.Canny(gray, threshold1=100, threshold2=200)

# Show the original image
cv2.imshow('Original Image', img)

# Show the edges
cv2.imshow('Edge Detection', edges)

# Wait until a key is pressed
cv2.waitKey(0)

# Close all windows
cv2.destroyAllWindows()