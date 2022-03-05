# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 13:29:55 2022

@author: Dhruvin
"""
import cv2
import os
import numpy as np
from os.path import isfile,join

class process:
    
    def detect_edges(self, img):
        canny = cv2.Canny(img, 30, 170, 3)
        dilated = cv2.dilate(canny, (2,2), iterations = 3)
        return dilated

    def flood_and_extract(self, img):
        h, w = img.shape[:2]
        mask = np.zeros((h+2, w+2), np.uint8)
        xy = img.copy()
        cv2.floodFill(xy, mask, (0,0), 255.0)
        inverted_filled = cv2.bitwise_not(xy)
        final = inverted_filled | img
        return final

    def blurred(self, img):
        median_blurred = cv2.medianBlur(img, 3)
        gaussian_blurred = cv2.GaussianBlur(median_blurred, (0, 0), 1, 1)
        close_morphed = cv2.morphologyEx(gaussian_blurred, cv2.MORPH_CLOSE, kernel = (5,5))
        return close_morphed
    
    def biggest_contour(self, mask):
        c, h = cv2.findContours(image=mask, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)
        sort_contour = sorted(c, key = cv2.contourArea, reverse = True)
        return sort_contour[0]

    def draw_biggest_contour(self, img):
        ab = np.empty(img.shape)
        contour = self.biggest_contour(img)
        xy = cv2.drawContours(ab, contours = contour, contourIdx = -1, color = 1, thickness = -1)
        xy[xy<0.000001] = 0
        xy[xy > 0.999999] = 255.0
        xy = np.uint8(xy)
        return xy


    def video_gen(self, pathIn, pathOut):
        img_arr = []
        images = [img for img in os.listdir(pathIn) if isfile(join(pathIn, img))] 
        for i in range(len(images)):
            filename = pathIn+ "\\" + images[i]
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width,height)
            time = 10
            for j in range(time):
                img_arr.append(img)

        fps = 275

        anim = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(*"mp4v"), fps, size)

        for i in range(len(img_arr)):
            anim.write(img_arr[i])
        anim.release()
    
    def extraction(self, img, cimg):
        edge = self.detect_edges(img)
        flood1 = self.flood_and_extract(edge)
        blur = self.blurred(flood1)
        flood2 = self.flood_and_extract(blur)
        
        contour = self.draw_biggest_contour(flood2)
        flood3 = self.flood_and_extract(contour)
        
        segmented = cv2.bitwise_and(cimg, cimg, mask =  flood3)
        segmented[segmented < 35] = 255
        
        return segmented
        

    
    def final(self, rt, dirr):
        ex = os.path.join(rt, 'Extracted')
        if not os.path.exists(ex):
            os.mkdir(ex)
            
        final = os.path.join(ex, dirr.split('\\')[-1])
        if not os.path.exists(final):
            os.mkdir(final)
        
        for root, subdirectories, files in os.walk(dirr):    
            
            for subdirectory in subdirectories:
                temp = os.path.join(final, subdirectory)
                if not os.path.exists(temp):
                    os.mkdir(temp)
                    
            for i in range(len(files)):
                x = root.split('\\')[-1]
                os.chdir(os.path.join(final, x))
                im_path = root + '\\' + files[i]
            
                img = cv2.imread(im_path, 0)
                cimg = cv2.imread(im_path, 1)
                fimg = self.extraction(img, cimg)
                cv2.imwrite(files[i], fimg)
                
            if len(files) == 256:
                current = root.split('\\')[-1]
                path_to_extracted = os.path.join(final, x)
                os.chdir(path_to_extracted)
                video_path = os.path.join(path_to_extracted, 'video')
                if not os.path.exists(video_path):
                    os.mkdir(video_path)
                video_path = os.path.join(video_path, 'vid.avi')
                self.video_gen(path_to_extracted, video_path)

root = os.path.dirname(__file__)
data = os.path.join(root, 'Diamonds')
print(os.getcwd())
folders = ['Shape_1d_256i', 'Shape_5d_256i', 'Shape_10d_256i'] 
p = process()
for i in folders:
    x = os.path.join(data, i)
    p.final(root, x)