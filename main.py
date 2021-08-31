import os
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util
import cv2 
import numpy as np
from matplotlib import pyplot as plt
from move import *
import math
from imutils.video import VideoStream
from imutils.video import FPS

# CONSTANTS (at 25.5 inches shooting distance)
webcamXOffset = 12 # in Pixels
webcamYOffset = 150 # in Pixels
X_ACC_THRESHOLD = 4 # in Pixels
Y_ACC_THRESHOLD = 7 # in Pixels
impatience = 70
aimTime = 3

# CUSTOM OFFSETS FOR SOLDIERS TO AIM AT BODY
radiomanX = 18   # 18 pixels to the right
multiGunnerX = -1
machineGunnerX = 1

# HELPER FUNCTIONS
def nextTarget(coords, crosshairX, crosshairY):
    """Find the closest target to the crosshair using euclidean distance"""
    nearestTgtId = -1
    minDist = 1e9
    i = 0
    for x in coords:
        ed = math.sqrt((crosshairX - (int(x[1]) + (int(x[3]) - int(x[1])) / 2)) ** 2 + (crosshairY - (int(x[2]) + (int(x[4]) - int(x[2])) / 2)) ** 2)
        if ed < minDist:
            minDist = ed
            nearestTgtId = i
        i += 1
    if nearestTgtId != -1:
        #print("TARGETTING:", coords[nearestTgtId][0])
        return [int(coords[nearestTgtId][1]) + (int(coords[nearestTgtId][3]) - int(coords[nearestTgtId][1])) // 2, int(coords[nearestTgtId][2]) + (int(coords[nearestTgtId][4]) - int(coords[nearestTgtId][2])) // 2, coords[nearestTgtId][0][2:]] # Returns (x, y, id) coords of closest target
    return [-1, -1, -1]# No targets found


# Load pipeline config and build a detection model
configs = config_util.get_configs_from_pipeline_file("detect_soldiers_v5/pipeline.config")
detection_model = model_builder.build(model_config=configs['model'], is_training=False)

# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join("detect_soldiers_v5", 'ckpt-3')).expect_partial()

@tf.function
def detect_fn(image):
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections

category_index = label_map_util.create_category_index_from_labelmap("detect_soldiers_v5/label_map.pbtxt")

print("Starting video stream...")
cap = VideoStream(src = 0).start()
sleep(2)
fps = FPS().start()

aimed = 0

# Premove tilter a few degrees to account for slop
moveTilter(5, 40)

while True: 
    frame = cap.read()
    (h, w) = frame.shape[:2]
    width, height = w, h
    image_np = np.array(frame)
    
    input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
    detections = detect_fn(input_tensor)
    
    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy()
                  for key, value in detections.items()}
    detections['num_detections'] = num_detections

    # detection_classes should be ints.
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

    label_id_offset = 1
    image_np_with_detections = image_np.copy()

    coords = viz_utils.visualize_boxes_and_labels_on_image_array(
                image_np_with_detections,
                detections['detection_boxes'],
                detections['detection_classes']+label_id_offset,
                detections['detection_scores'],
                category_index,
                use_normalized_coordinates=True,
                max_boxes_to_draw=10,
                min_score_thresh=.49,
                agnostic_mode=False)
    
    #print(coords)

    # Draw crosshair
    crosshairX = w // 2 + int(webcamXOffset)
    crosshairY = h // 2 + int(webcamYOffset)
    cv2.circle(image_np_with_detections, (crosshairX, crosshairY), 5, (0xFF, 0xFF, 0xFF), 1)
    cv2.circle(image_np_with_detections, (crosshairX, crosshairY), 10, (0xFF, 0xFF, 0xFF), 2)

    cv2.imshow('object detection',  cv2.resize(image_np_with_detections, (800, 600)))
    
    # Find the closest target
    tgt = nextTarget(coords, crosshairX, crosshairY)
    #print("TARGET:", tgt)

    # Aim at closest target
    if (tgt[0] != -1):
        k = 1
        if abs(tgt[0] - crosshairX) > 75:
            k = 0
        
        # Make minor adjustments based on what type of soldier it is aiming at
        if (tgt[2] == "GreenRadioman"):
            tgt[0] += radiomanX
        elif (tgt[2] == "GreenMultiGunner"):
            tgt[0] += multiGunnerX
        elif (tgt[2] == "GreenMachineGunner"):
            tgt[0] += machineGunnerX
        print("Targetting:", tgt[2])

        turnAndTilt(tgt[0] - crosshairX, k * -(tgt[1] - crosshairY))

        # Shoot if the target is aimed
        if (aimed >= aimTime and abs(tgt[0] - crosshairX) <= X_ACC_THRESHOLD and abs(tgt[1] - crosshairY) <= Y_ACC_THRESHOLD):
            # Wait for wobbling to stop
            moveShooter(1)
            print("SHOOT")
            aimed = 0
        elif abs(tgt[0] - crosshairX) <= X_ACC_THRESHOLD and abs(tgt[1] - crosshairY) <= Y_ACC_THRESHOLD:
            aimed += 1
            print("AIMING:", aimed, "/", aimTime)
        else:
            aimed = 0
    else:
        impatience -= 1
        if impatience < 0:
            # move tilter back down to check if we missed any soldiers
            impatience = 70
            moveTilter(5, 10)
            setLastAng(tilterMotor.position)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        cleanup_motors()
        break

    # update fps counter
    fps.update()

fps.stop()
print ('[INFO] elapsed time: {:.2f}'.format(fps.elapsed()))
print ('[INFO] approx. FPS: {:.2f}'.format(fps.fps()))