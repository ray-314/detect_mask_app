"""Application to determine whether or not a mask is worn
"""

# Import libraries
import streamlit as st
import numpy as np
import os, sys, json, cv2
from typing import Tuple
from PIL.ImageFont import FreeTypeFont
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vision.computer_vision import ComputerVisionClient
from vision.authentication import CognitiveServicesCredentials

# Key and Endpoint settings
with open('../setting/secret.json') as f:
    secret = json.load(f)
ENDPOINT = secret['ENDPOINT']
KEY = secret['KEY']

# Create functions
@st.cache_data # Save cash
def reduce_imagesize(size: int, reduction_rate: int = 2,) -> Tuple[int, int]:
    """Calculate the reduced size of an image.

    Args:
        size (int): Base image size.
        reduction_rate (int, optional): Reduction ratio. Defaults to 2.

    Returns:
        Tuple[int, int]: Calculated image width and height.
    """
    while True:
        if ((image.width // reduction_rate)<size) or ((image.height // reduction_rate)<size): break
        else: reduction_rate += 1
    width, height = image.width // reduction_rate, image.height // reduction_rate
    return width, height

@st.cache_data # Save cash
def detect_mask(image_array: np.array) -> json:
    """Detect people and determine if they are wearing a mask.

    This function uses the API for mask detection. It also stores a cache to alleviate delays in sending and receiving data to and from the API server.

    Args:
        image_array (np.array): Image data to be sent to API server.

    Returns:
        json: Response data sent from the API server.
    """
    return computervision_client.detect_mask(image_array.tolist())

def get_textsize(caption: str, font: FreeTypeFont) -> Tuple[int, int]:
    """Measuring text size.

    Args:
        caption (str): Text to display.
        font (FreeTypeFont): Font to be used for the text to be displayed.

    Returns:
        Tuple[int, int]: Width and height of text to be displayed.
    """
    text_bbox: Tuple[int, int, int, int] = draw.textbbox(xy=(0,0), text=caption, font=font)
    text_w, text_h = text_bbox[2]-text_bbox[0], text_bbox[3]-text_bbox[1]+5
    return text_w, text_h

# Application summary
st.title('マスク検知アプリ')

st.write('### 画像の選択')
uploaded_file = st.file_uploader('マスク検出を試みたい画像を選択してください。', type=['jpg','png'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    # Resize uploaded image to display image
    if (image.width>500) or (image.height>500):
        width, height = reduce_imagesize(size=400, reduction_rate=2)
        image_resized = image.resize((width, height))
    else:
        image_resized = image
    # Display image
    st.image(image_resized)

    # Processing of mask detection
    if st.button(label='マスク検知開始'):
        # Authentication and instantiation
        computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(KEY).authenticate())
        # Detect people wearing masks
        image_array = np.array(image)
        res = detect_mask(image_array)

        # Processing when response is successful
        if res.status_code == 200:
            st.success('検知完了')
            res = res.json()

            # Detect faces and display face images
            st.write('### 顔検知結果')
            col1, col2, col3, col4 = st.columns(4)
            for i,rectangle in enumerate(res['rectangles']):
                exec('col{}.write("Person {} : ")'.format((i%4)+1, i+1))
                face_image = image_array[rectangle['top']:rectangle['bottom'], rectangle['left']:rectangle['right']]
                exec('col{}.image(cv2.resize(face_image, (80, 80)))'.format((i%4)+1))
                exec('col{}.write("{}")'.format((i%4)+1, res['tags'][i]))
            
            # Detect and discriminate between people wearing and not wearing masks
            st.write('### マスク検知結果')
            draw = ImageDraw.Draw(image)
            font_1 = ImageFont.truetype(font='../font/Helvetica 400.ttf', size=25)
            font_2 = ImageFont.truetype(font='../font/Helvetica 400.ttf', size=20)
            for i,rectangle in enumerate(res['rectangles']):
                caption_1 = 'Person{}'.format(i+1)
                caption_2 = res['tags'][i]
                if caption_2=='Without Mask': color = 'red'
                else: color = 'green'
                text1_w, text1_h = get_textsize(caption_1, font_1)
                text2_w, text2_h = get_textsize(caption_2, font_2)
                draw.rectangle([(rectangle['left'], rectangle['top']), (rectangle['right'], rectangle['bottom'])], fill=None, outline=color, width=4)
                draw.rectangle([(rectangle['left'], rectangle['top']-text1_h), (rectangle['left']+text1_w, rectangle['top'])], fill=color)
                draw.rectangle([(rectangle['left'], rectangle['bottom']), (rectangle['left']+text2_w, rectangle['bottom']+text2_h)], fill=color)
                draw.text((rectangle['left'], rectangle['top']-text1_h), caption_1, fill='white', font=font_1)
                draw.text((rectangle['left'], rectangle['bottom']), caption_2, fill='white', font=font_2)
            
            # Display image
            width, height = reduce_imagesize(size=600, reduction_rate=1)
            st.image(image.resize((width, height)))
        
        # For development (confirmation screen)
        st.sidebar.write('### 開発用（確認画面）')
        st.sidebar.write('レスポンス結果')
        st.sidebar.write(res)