import streamlit as st
import numpy as np
from skimage import io
from numpy import asarray
from PIL import Image
import PIL
import os
from PIL import Image, ImageOps
import numpy as np
import cv2
from skimage import morphology, exposure

st.title("📷 Diamond Extractor 📷")

def load_image(image_file):
    img = Image.open(image_file)
    return img




def main():
    st.subheader("Dataset Credit: D360 Tech")
    #menu = ["Image","Dataset","DocumentFiles","About"]
    choice = "Image"
    if choice == "Image":
        st.subheader("Image")
        image_file = st.file_uploader("Upload Your Image", type=['jpg', 'png', 'jpeg'])
        if not image_file:
            return None

        original_image = Image.open(image_file)
        img = np.array(original_image)

        xy = cv2.Canny(img, 30, 170, 3)
        xy = cv2.dilate(xy, (2,2), iterations = 3)

        h, w = xy.shape[:2]
        mask = np.zeros((h+2, w+2), np.uint8)
        xyc = xy.copy()
        cv2.floodFill(xyc, mask, (0,0), 255.0)
        xyc = cv2.bitwise_not(xyc)

        xy = xy | xyc

        xy = cv2.medianBlur(xy, 3)
        xy = cv2.GaussianBlur(xy, (0, 0), 1, 1)
        xy = cv2.morphologyEx(xy, cv2.MORPH_CLOSE, kernel = (5,5))

        h, w = xy.shape[:2]
        mask = np.zeros((h+2, w+2), np.uint8)
        xyc = xy.copy()
        cv2.floodFill(xyc, mask, (0,0), 255.0)
        xyc = cv2.bitwise_not(xyc)

        xy = xy | xyc

        c, h = cv2.findContours(image=xy, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)
        sort_contour = sorted(c, key = cv2.contourArea, reverse = True)
        largest_contour = sort_contour[0]

        ab = np.empty(xy.shape)

        xy = cv2.drawContours(ab, contours = largest_contour, contourIdx = -1, color = 1, thickness = -1)
        xy[xy<0.000001] = 0
        xy[xy > 0.999999] = 255.0
        xy = np.uint8(xy)
        np.unique(xy)


        h, w = xy.shape[:2]
        mask = np.zeros((h+2, w+2), np.uint8)
        xyc = xy.copy()
        cv2.floodFill(xyc, mask, (0,0), 255.0)
        xyc = cv2.bitwise_not(xyc)
        xy = xy | xyc

        # img1 = io.imread(original_image, as_gray=True)
        #img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        seg_im = cv2.bitwise_and(img, img, mask =  xy)


        seg_im[seg_im < 35] = 255


        # xy = cv2.Canny(img, 30, 170, 3)
        # xy = cv2.dilate(xy, (2,2), iterations = 3)

        # h, w = xy.shape[:2]
        # mask = np.zeros((h+2, w+2), np.uint8)
        # xyc = xy.copy()
        # cv2.floodFill(xyc, mask, (0,0), 255.0)
        # xyc = cv2.bitwise_not(xyc)

        # xy = xy | xyc

        # xy = cv2.medianBlur(xy, 3)
        # xy = cv2.GaussianBlur(xy, (0, 0), 1, 1)
        # xy = cv2.morphologyEx(xy, cv2.MORPH_CLOSE, kernel = (5,5))

        # h, w = xy.shape[:2]
        # mask = np.zeros((h+2, w+2), np.uint8)
        # xyc = xy.copy()
        # cv2.floodFill(xyc, mask, (0,0), 255.0)
        # xyc = cv2.bitwise_not(xyc)

        # xy = xy | xyc
        # seg_im = cv2.bitwise_and(img, img, mask =  xy)


        # seg_im[seg_im < 35] = 255


        
        image = PIL.Image.fromarray(seg_im, "RGB")

        st.subheader("Original uploaded Image :")
        st.image(original_image,width=400)

        st.subheader("Output Image [with white background]:")
        st.image(image,width=400)
        #image = Image.open(image) #Image name
        #fig = plt.figure()
        #plt.imshow(image)
        #plt.axis("off")
        #st.pyplot(fig)

        # if image is not None:
        #     with open(os.path.join("tempDir",image.name),"wb") as f: 
        #         f.write(image.getbuffer())         
        #     st.success("Saved File")


        # with open(image_file.name, "rb") as file:
        #      btn = st.download_button(
        #      label="Download image",
        #      data=file,
        #      file_name=image.name,
        #      #mime="image/png"
        #    )
        # #st.image(load_image(mask))


if __name__ == '__main__':
    	main()



