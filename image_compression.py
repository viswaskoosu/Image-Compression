import streamlit as st
from io import BytesIO , StringIO
import base64

import numpy
from PIL import Image

from streamlit_option_menu import option_menu

def seperateColors(img):
    input_img = Image.open(img)
    matrix = numpy.array(input_img)

    Blue = matrix[:,:,2]
    Green = matrix[:,:,1]
    Red = matrix[:,:,0]

    return [input_img , Red , Green , Blue]

def compressImage(color , N):
    U , Sigma , V = numpy.linalg.svd(color)
    color_compress = numpy.zeros((color.shape[0] , color.shape[1]))
    Singular = numpy.diag(Sigma)[0:N ,0:N]
    left = numpy.matmul(U[:,0:N] , Singular)
    right = numpy.matmul(left , V[0:N , :])
    color_compress = right.astype('uint8')
    return color_compress

# originalImage , aRed , aGreen , aBlue = seperateColors('imggg.jpg')

# imageWidth = 512
# imageHeight = 512

# singularValuesLimit = 50

# Red = compressImage(aRed, singularValuesLimit)
# Blue = compressImage(aBlue, singularValuesLimit)
# Green= compressImage(aGreen, singularValuesLimit)

# imr = Image.fromarray(Red, mode=None)
# imb = Image.fromarray(Blue, mode=None)
# img = Image.fromarray(Green, mode=None)

# newImage = Image.merge("RGB", (imr, img, imb))


def compress_image(img , singularValuesLimit):
    ori , red , green , blue = seperateColors(img)
    redc = compressImage(numpy.array(red) , singularValuesLimit)
    greenc = compressImage(green , singularValuesLimit)
    bluec = compressImage(blue , singularValuesLimit)

    imr = Image.fromarray(redc, mode=None)
    imb = Image.fromarray(bluec, mode=None)
    img = Image.fromarray(greenc, mode=None)
    newImage = Image.merge("RGB", (imr, img, imb))
    return newImage

# originalImage.show()
# newImage.show()

@st.cache_data
def load_image(file):
    return Image.open(file)


def main():

    st.title("Image Compression")

    with st.form("Upload Image"):
        menu = ["10" , "25" , "50" , "100"]
        singularValuesLimit = int(st.selectbox(" Select Number of singular values , more the number , higher the clarity " , menu))
        file = st.file_uploader("Upload Image" , type = ['png' , 'jpg'])

        submit = st.form_submit_button()

        if submit and file is not None : 
            left , right = st.columns(2)
            with left : 
                st.title("Orignal")
                st.image(load_image(file))
            with right : 
                st.title("Compressed")
                img_compress = compress_image(file , singularValuesLimit)
                st.image(img_compress)
                st.write("### To download image \n Right click and click on \n \"Save Image as\" ")
        

            # with open(img_compress , "rb") as output : 
            #     btn = st.download_button(label = 'Compress'+'.jpg' , data = img_compress , file_name = 'Compress,jpg' , mime = 'image/png')
            #     buf = BytesIO()
            #     img_compress.save(buf , format = "JPG")
            #     byte_im = buf.getvalue()

            # st.download_button(label = 'Download' , data = newImage)    
        else : 
            st.warning("Upload Image to compress")

# Running the web
def creators():
    st.title("Creators")
    left , right = st.columns(2)
    with left : 
        st.write("#### Viswas Koosu")
        st.image('viswas.jpg' , use_column_width= True , caption= "Mechanical Engineering , IIT Dharwad") 
    with right :
        st.write("#### Sankalp Nagaonkar")
        st.image('sanklap.jpg' , use_column_width=True ,caption= "Electrical Engineering , IIT Dharwad")
    
    l , r = st.columns(2)
    with l : 
        st.write("### Tejas Mhaiskar")
    with r : 
        st.write("### Ashis Pradhan")
    st.image("us.jpg")

def model_description():
    st.title("Singular Value Decomposion")
    for i in range(5):
        st.image("report/report_page-000{}.jpg".format(i+1))
    

tab = option_menu(
    menu_title=None ,
    options = ["Compress" , "Model" , "Creators"],
    icons = ["image-fill" ,  "activity" ,"person-fill"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)

if tab == "Compress":
    main()
elif tab == "Creators":
    creators()
else :
    model_description()
# main()
