import tensorflow as tf
import numpy as np
import base64
from pickle import dump, load
import sklearn
from datetime import datetime

saved_model_dir = "models/openimages_v4_ssd_mobilenet_v2_1"
saved_model = tf.saved_model.load(saved_model_dir)
detector = saved_model.signatures["default"]


# the list of categories of items and their max stock
categories = {"Bottle": 100, "Pen": 1000, "Footwear": 50, "Drink": 100, "Clothing": 500}


def load_discount_model():
    """
    load the models necessary to predict discounts.
    """
    discounts_path = "5_discount_models"
    model = load(open(discounts_path + "/knn-model_0.pkl", "rb"))
    sc = load(open(discounts_path + "/scaler_0.pkl", "rb"))
    enc = load(open(discounts_path + "/label-encoder_0.pkl", "rb"))
    return model, sc, enc


# load our discount model into memory
discount_model, scaler, encoder = load_discount_model()


def find_objects_and_predict_discounts(message):
    """
    our main function, called from the webapp.
    takes in the message containing the image,
    uses object detection model to find objects,
    then calls our discount calculating model to return objects and discounts.
    """
    base64img = message.get("image")
    img_bytes = base64.decodebytes(base64img.encode())

    detected_ojects = detect_objects(img_bytes)
    cleaned_objects = clean_up_detections(detected_ojects)

    discounts = predict_discounts(cleaned_objects)

    return {"detections": discounts}


def predict_discounts(cleaned_objects):
    """
    predict discounts for each item
    based on 'current stock'
    """
    # get current stock, convert to np array
    current_stock = find_stock()
    list_stock = list(current_stock.items())
    stock_array = np.asarray(list_stock)

    # store both columns of np array
    orig_labels = stock_array[:, 0]
    stock = stock_array[:, 1]

    # encode labels, apply scaler
    labels = encoder.transform(orig_labels)
    stock_array = np.column_stack((labels, stock))
    stock_array = scaler.transform(stock_array)

    # make model predictions on scaled data
    discount_predictions = discount_model.predict(stock_array)
    # print(predictions)

    labels_preds = dict(zip(orig_labels, discount_predictions))
    # print(labels_preds)

    for detected_object in cleaned_objects:
        detected_discount = labels_preds[detected_object["class"]] * 100
        rounded_discount = int(detected_discount)
        detected_object["cValue"] = str(rounded_discount) + "% off"
        print(
            "detected: "
            + str(detected_object["class"])
            + " confidence: "
            + str(detected_object["score"])
            + " discount is: "
            + str(detected_object["cValue"])
        )

    return cleaned_objects


def find_stock():
    """
    find the current stock of items
    based on the current time of day
    """
    # ref for calc of seconds_since_midnight: https://stackoverflow.com/a/15971505
    now = datetime.now()
    seconds_since_midnight = (
        now - now.replace(hour=0, minute=0, second=0, microsecond=0)
    ).total_seconds()
    portion_of_day = seconds_since_midnight / 86400  # fraction of day at this time.
    print(now)

    # multiply all categories max stock by the portion of the daytime
    stock_items = categories.copy()
    stock_items.update((x, int((y * portion_of_day))) for x, y in stock_items.items())

    return stock_items


def detect_objects(img):
    """
    finds the objects in a given image
    using our pretrained CV model
    """
    image = tf.image.decode_jpeg(img, channels=3)
    converted_img = tf.image.convert_image_dtype(image, tf.float32)[tf.newaxis, ...]
    result = detector(converted_img)
    num_detections = len(result["detection_scores"])

    output_dict = {key: value.numpy().tolist() for key, value in result.items()}
    output_dict["num_detections"] = num_detections

    return output_dict


def clean_up_detections(detections):
    """
    'cleans up' the detected objects list
    only keeps objects of certain classes with solid confidence scores
    """
    cleaned = []
    max_boxes = 10
    num_detections = min(detections["num_detections"], max_boxes)

    # only include detected classes in our list.
    for i in range(0, num_detections):
        d = {
            "box": {
                "yMin": detections["detection_boxes"][i][0],
                "xMin": detections["detection_boxes"][i][1],
                "yMax": detections["detection_boxes"][i][2],
                "xMax": detections["detection_boxes"][i][3],
            },
            "class": detections["detection_class_entities"][i].decode("utf-8"),
            "cValue": " ",
            "label": detections["detection_class_entities"][i].decode("utf-8"),
            "score": detections["detection_scores"][i],
        }
        if d.get("class") in categories.keys() and d.get("score") >= 0.15:
            cleaned.append(d)

    return cleaned


def find_objects_and_predict_discounts_testing(img_path):
    """
    modified main function, called outside the webapp for testing.
    takes in the image path
    uses object detection model to find objects,
    then calls our discount calculating model to return objects and discounts.
    """
    img_bytes = tf.io.read_file(img_path)
    detected_ojects = detect_objects(img_bytes)
    cleaned_objects = clean_up_detections(detected_ojects)

    discs = predict_discounts(cleaned_objects)

    return {"detections": discs}


def preload_model():
    """
    This is to 'warm up' the model.
    """
    blank_jpg = tf.io.read_file("images/blank.jpeg")
    blank_img = tf.image.decode_jpeg(blank_jpg, channels=3)
    detector(tf.image.convert_image_dtype(blank_img, tf.float32)[tf.newaxis, ...])


preload_model()
