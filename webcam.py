# import the opencv library
import cv2

# CONSTANTS
webcamXOffset = 12
webcamYOffset = 150

# define a video capture object
vid = cv2.VideoCapture(0)
  
while(True):
    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    # Get dimensions of video feed (640 by 480)
    (h, w) = frame.shape[:2]
    # print("Width:", w, "Height:", h)
    
    # Draw crosshair
    cv2.circle(frame, (w // 2 + webcamXOffset, h // 2 + webcamYOffset), 5, (255, 255, 255), 1)
    cv2.circle(frame, (w // 2 + webcamXOffset, h // 2 + webcamYOffset), 10, (255, 255, 255), 2)
    
    # Display the resulting frame
    cv2.imshow('frame', frame)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
