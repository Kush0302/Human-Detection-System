import cv2

#Load an image
image=cv2.imread("people.jpg")

#Resize image for better speed 
image=cv2.resize(image, (640,480))

# Initialize HOG (Histogram of Oriented Gradients) descriptor/person detector
hog=cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Detect people (returns bounding boxes and weights)
boxes, weights=hog.detectMultiScale(image,winStride=(8,8))

# Draw bounding boxes
for (x, y, w, h) in boxes:
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

#Opens a new window and displays the image with rectangles drawn
cv2.imshow("Human Detection", image)

#Waits indefinitely until you press a key
#Without this the window would close instantly
cv2.waitKey(0)

#Closes all opencv windows opened with cv2.imshow()
cv2.destroyAllWindows()