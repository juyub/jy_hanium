import cv2
import numpy as np

# 비디오 파일 명으로 변경합니다
video_input_file = 'video/in.mp4'

def get_output_layers(net):
    layer_names = net.getLayerNames()
    
    output_layers_indices = net.getUnconnectedOutLayers()
    if output_layers_indices.ndim == 1:
        output_layers = [layer_names[i - 1] for i in output_layers_indices]
    else:
        output_layers = [layer_names[i[0] - 1] for i in output_layers_indices]

    return output_layers

net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = get_output_layers(net)

accumulated_count_left = 0
accumulated_count_right = 0

with open("coco.names", "rt") as f:
    classes = f.read().rstrip('\n').split('\n')

cap = cv2.VideoCapture(video_input_file)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
accumulated_count = 0
prev_count_left = 0
prev_count_right = 0

accumulated_count_left = 0
accumulated_count_right = 0

frame_skip = 5
frame_count = 0

while True:
    ret, frame = cap.read()
    count_left = 0
    count_right = 0
    if not ret:
        break
    
    if frame_count % frame_skip == 0: 
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and class_id == 0:
                center_x, center_y, width, height = (detection[0:4] * [frame_width, frame_height, frame_width, frame_height]).astype(int)
                x = int(center_x - width // 2)
                y = int(center_y - height // 2)
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    for i in range(len(boxes)):
        if i not in indices:
            continue
        box = boxes[i]
        (x, y, w, h) = box[:4]
        center_x = x + w // 2   # 객체 중심점 추가

        if center_x < frame_width / 2:
            count_left += 1
        else:
            count_right += 1
        label = f"Person: {confidences[i]:.2f}"
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    
    # 누적값 계산
    if count_left > prev_count_left:
        accumulated_count_left += count_left - prev_count_left
    
    if count_right > prev_count_right:
        accumulated_count_right += count_right - prev_count_right
    
    accumulated_count = accumulated_count_right + accumulated_count_left
    
    # draw line and put text...
    
    prev_count_left = count_left
    prev_count_right = count_right 
    
    start = (int(frame_width // 2), 0)
    end = (int(frame_width // 2), frame_height)
    cv2.line(frame, start, end, (255, 0, 0), 2)
    
    cv2.putText(frame, f"Left: {count_left}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv2.putText(frame, f"Right: {count_right}", (frame_width - 150, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv2.putText(frame, f"Accumulated: {accumulated_count}", (10, frame_height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    prev_count_left = count_left
    prev_count_right = count_right

    cv2.imshow('Object Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
