# import cv2

# url = "http://192.168.0.101:4747/video"  # Replace with your phone’s IP
# cap = cv2.VideoCapture(url)

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("Failed to grab frame")
#         break
#     cv2.imshow("DroidCam Feed", frame)

    
#     if cv2.waitKey(1) & 0xFF == ord('c'):
#         cv2.imwrite("captured_image.jpg", frame)
#         print("Image Captured!")

#         # Show the captured image
#         cv2.imshow("Captured Image", frame)
#         cv2.waitKey(0)
#         break

# cap.release()
# cv2.destroyAllWindows()


# VERICAL

# import cv2

# url = "http://192.168.0.101:4747/video"  # Replace with your phone’s IP
# cap = cv2.VideoCapture(url)

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("Failed to grab frame")
#         break

#     # Rotate the frame 90 degrees counterclockwise
#     frame_rotated = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

#     # Display the rotated frame
#     cv2.imshow("DroidCam Feed", frame_rotated)

#     if cv2.waitKey(1) & 0xFF == ord('c'):
#         cv2.imwrite("captured_image.jpg", frame_rotated)
#         print("Image Captured!")
#         break

# cap.release()
# cv2.destroyAllWindows()


import cv2

url = "http://192.168.0.101:4747/video"  # Replace with your phone’s IP
cap = cv2.VideoCapture(url)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Rotate the frame 90 degrees clockwise for portrait mode
    frame_rotated = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    # Display the rotated frame
    cv2.imshow("DroidCam Feed", frame_rotated)

    if cv2.waitKey(1) & 0xFF == ord('c'):
        cv2.imwrite("captured_image.jpg", frame_rotated)
        print("Image Captured!")

        # Allow user to select a region to crop
        roi = cv2.selectROI("Select Region", frame_rotated, fromCenter=False, showCrosshair=True)
        if roi != (0, 0, 0, 0):  # Check if selection is valid
            x, y, w, h = roi
            cropped_image = frame_rotated[y:y+h, x:x+w]
            cv2.imwrite("cropped_image.jpg", cropped_image)
            print("Cropped Image Saved!")

            # Show the cropped image
            cv2.imshow("Cropped Image", cropped_image)
            cv2.waitKey(0)

        break

cap.release()
cv2.destroyAllWindows()
