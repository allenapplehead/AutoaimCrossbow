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

# CONSTANTS (at 25.5 inches shooting distance)
webcamXOffset = 12 # in Pixels
webcamYOffset = 150 # in Pixels
ACC_THRESHOLD = 4 # in Pixels

# HELPER FUNCTIONS
def nextTarget(coords, crosshairX, crosshairY):
    """Find the closest target to the crosshair using euclidean distance"""
    nearestTgtId = -1
    minDist = 1e9
    i = 0
    for x in coords:
        print("CRD:", x)
        ed = math.sqrt((crosshairX - (int(x[1]) + (int(x[3]) - int(x[1])) / 2)) ** 2 + (crosshairY - (int(x[2]) + (int(x[4]) - int(x[2])) / 2)) ** 2)
        if ed < minDist:
            minDist = ed
            nearestTgtId = i
        i += 1
    if nearestTgtId != -1:
        print("TARGETTING:", coords[nearestTgtId][0])
        return (int(coords[nearestTgtId][1]) + (int(coords[nearestTgtId][3]) - int(coords[nearestTgtId][1])) // 2, int(coords[nearestTgtId][2]) + (int(coords[nearestTgtId][4]) - int(coords[nearestTgtId][2])) // 2) # Returns (x, y) coords of closest target
    return (-1, -1) # No targets found


# Load pipeline config and build a detection model
configs = config_util.get_configs_from_pipeline_file("detect_soldiers_v2/pipeline.config")
detection_model = model_builder.build(model_config=configs['model'], is_training=False)

# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join("detect_soldiers_v2", 'ckpt-3')).expect_partial()

@tf.function
def detect_fn(image):
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections

category_index = label_map_util.create_category_index_from_labelmap("detect_soldiers_v2/label_map.pbtxt")

cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

while cap.isOpened(): 
    ret, frame = cap.read()
    (h, w) = frame.shape[:2]
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
                min_score_thresh=.7,
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
        turnAndTiltPID(tgt[0] - crosshairX, -(tgt[1] - crosshairY))

        # Shoot if the target is aimed
        #print(abs(tgt[0] - crosshairX))
        if (abs(tgt[0] - crosshairX) <= ACC_THRESHOLD):
            moveShooter(1)
            print("SHOOT")

    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        cleanup_motors()
        break
