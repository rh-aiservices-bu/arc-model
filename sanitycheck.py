from typing import Dict
from prediction import find_objects_and_predict_discounts_testing
import tensorflow as tf
import numpy as np
import base64
from pickle import dump, load
import sklearn
from datetime import datetime
import json
import pickle


def sanity_check(filename):
    # pass photo to main prediction function
    # have to convert our dummy image to b64 encoded, then to dict
    preds = find_objects_and_predict_discounts_testing(filename)
    detections = preds["detections"]

    # pass predictions to our testing function
    return test_detections(detections)


def test_detections(detections):
    """
    function to sanity check the detections found in our dummy image
    """

    # if we didnt detect the clothing or
    # if we detected more things than the clothing
    if len(detections) != 1:
        return False

    # if we detected something other than clothing
    if detections[0]["class"] != "Clothing":
        return False

    discount_val = detections[0]["cValue"]
    discount_val = float(discount_val[:3])

    # ensure our discount is within our bounds.
    if 0 > discount_val:
        return False

    if discount_val > 41:
        return False

    return True


print(sanity_check("images/RHODS_cool_store.png"))
