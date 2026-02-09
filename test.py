import cv2
from pyzbar.pyzbar import decode

# Access the camera
cap = cv2.VideoCapture(0) # 0 indicates the default camera

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Decode QR codes in the frame
    decoded_objects = decode(frame)

    # Print data from detected QR codes
    for obj in decoded_objects:
        print("Data:", obj.data.decode('utf-8'))
        # Draw a rectangle around the QR code (optional)
        (x, y, w, h) = obj.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the frame
    cv2.imshow("QR Code Scanner", frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and destroy windows
cap.release()
cv2.destroyAllWindows()
