import cv2
import numpy as np

# Load image
image = cv2.imread('C:/Users/Stella Barraza/Downloads/OpenCV/images/tulips.jpg.webp')
if image is None:
    print("Error: Could not load image")
    exit()

# Convert to HSV color space for color filtering
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define color range to detect (example: red objects)
lower_color = np.array([0, 100, 100])
upper_color = np.array([10, 255, 255])
mask = cv2.inRange(hsv, lower_color, upper_color)

# Find contours in the mask
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    # Compute bounding box
    x, y, w, h = cv2.boundingRect(cnt)

    # Compute center
    center_x = x + w // 2
    center_y = y + h // 2

    # Draw rectangle and center point
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.circle(image, (center_x, center_y), 5, (255, 0, 0), -1)

    # Print object position in image frame
    print(f"Object center: (X: {center_x}, Y: {center_y})")

# Show the result
cv2.imshow("Detected Object", image)
cv2.waitKey(0)
cv2.destroyAllWindows()