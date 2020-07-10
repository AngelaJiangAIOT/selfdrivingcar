# -*- coding: utf-8 -*-
import cv2
import numpy as np
class NeuralNetwork(object):

    def __init__(self):
        self.annmodel = cv2.ml.ANN_MLP_load('mlp_xml/mlp.xml')
 
    def predict(self, samples):
        ret, resp = self.annmodel.predict(samples)
        return resp.argmax(-1)  #find max