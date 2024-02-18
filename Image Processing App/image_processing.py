import streamlit as st
import cv2
import numpy as np
import io

# Function to perform brightness adjustment
def adjust_brightness(image, brightness):
    adjusted_image = cv2.convertScaleAbs(image, alpha=1, beta=brightness)
    return adjusted_image

# Function to perform contrast adjustment
def adjust_contrast(image, contrast):
    adjusted_image = cv2.convertScaleAbs(image, alpha=contrast, beta=0)
    return adjusted_image

# Function to add annotations to the image
def add_annotations(image, annotation_type, position, color):
    annotated_image = image.copy()
    color = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))  # Convert hex to RGB tuple

    if annotation_type == 'Line':
        cv2.line(annotated_image, position[0], position[1], color, thickness=position[2], lineType=cv2.LINE_AA)
    elif annotation_type == 'Rectangle':
        cv2.rectangle(annotated_image, position[0], position[1], color, thickness=position[2], lineType=cv2.LINE_8)
    elif annotation_type == 'Circle':
        cv2.circle(annotated_image, position[0], position[1], color, thickness=position[2], lineType=cv2.LINE_AA)
    elif annotation_type == 'Text':
        font = cv2.FONT_HERSHEY_SIMPLEX  # Default font
        if position[4] == 'Arial':
            font = cv2.FONT_HERSHEY_SIMPLEX
        elif position[4] == 'Times New Roman':
            font = cv2.FONT_HERSHEY_TRIPLEX
        elif position[4] == 'Courier':
            font = cv2.FONT_HERSHEY_DUPLEX
        elif position[4] == 'Cursive':
            font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
        
        # Draw text with the selected color
        cv2.putText(annotated_image, position[0], position[1], font, position[3], color, position[2], cv2.LINE_AA)
    return annotated_image

# Main function
def main():    
    # st.set_page_config(page_title="Image Processing App", page_icon=":camera:", layout="wide", initial_sidebar_state="expanded")
    st.set_page_config(page_title="Image Processing App", page_icon="https://img.freepik.com/premium-photo/flat-color-camera-logo-ai-generated_860599-6247.jpg", layout="wide", initial_sidebar_state="expanded")

    
    # logo_url = r"C:\Users\mgmoh\Desktop\flat-color-camera-logo-ai-generated_860599-6247.jpg"
    # logo_url = "https://img.freepik.com/premium-photo/flat-color-camera-logo-ai-generated_860599-6247.jpg"
    # st.image(logo_url, width=100)

    # Displaying the image centered
    st.write("""
        <div style="display: flex; justify-content: center;">
            <img src="https://img.freepik.com/premium-photo/flat-color-camera-logo-ai-generated_860599-6247.jpg" alt="Your Image" width="300">
        </div>
    """, unsafe_allow_html=True)

    st.write( "\n \n \n")
    
    st.title("Image Processing App")

    # CSS Styling
    st.markdown(
        """
        <style>
        body {
            background-color: #f4f4f4;
            color: #333;
        }
        h1 {
            color: #0066cc;
            text-align: center;
        }
        .stButton > button {
            background-color: #0066cc;
            color: #fff;
            border-radius: 5px;
        }
        .widget-slider-container .stSlider {
            width: 90%;
        }
        .stImage > img {
            max-width: 100%;
            height: auto;
        }
        .imageCaption {
            font-size: 14px;
            color: #666;
        }
        .css-1lh52fc {
            background-color: #fff;
            box-shadow: 0px 0px 5px #888888;
            padding: 10px;
            border-radius: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Upload image
    uploaded_file = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        original_image = cv2.imdecode(file_bytes, 1)

        # Get image height and width
        height, width, _ = original_image.shape

        st.markdown(f"### Image Dimensions:")
        st.markdown(f"- Height Scale: 0 - {height}")
        st.markdown(f"- Width Scale: 0 - {width}")

        st.write( "\n")
        st.write( "\n")
        
        # Image processing options
        option = st.sidebar.selectbox("Select an image processing option",
                              ["Original", "RGB", "Grayscale", "Binary", "Brightness", "Contrast", "Annotation"])

        if option == "Original":
            st.balloons()
            st.image(original_image, channels="BGR", caption="Original Image")

        elif option == "RGB":
            st.balloons()
            rgb_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
            st.image(rgb_image, caption="RGB Image")
            download_button(rgb_image, "RGB Image")

        elif option == "Grayscale":
            st.balloons()
            gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
            st.image(gray_image, caption="Grayscale Image")
            download_button(gray_image, "Grayscale Image")

        elif option == "Binary":
            st.balloons()
            _, binary_image = cv2.threshold(cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)
            st.image(binary_image, caption="Binary Image")
            download_button(binary_image, "Binary Image")

        elif option == "Brightness":
            brightness = st.sidebar.slider("Brightness", -100, 100, 0)
            adjusted_brightness_image = adjust_brightness(original_image, brightness)
            st.image(adjusted_brightness_image, channels="BGR", caption="Adjusted Image")
            download_button(adjusted_brightness_image, "Brightness Adjusted Image")

        elif option == "Contrast":
            contrast = st.sidebar.slider("Contrast", -100, 100, 0)
            adjusted_contrast_image = adjust_contrast(original_image, contrast/127.0 + 1)
            st.image(adjusted_contrast_image, channels="BGR", caption="Adjusted Image")
            download_button(adjusted_contrast_image, "Contrast Adjusted Image")

        elif option == "Annotation":
            annotation_type = st.sidebar.selectbox("Select annotation type", ["Line", "Rectangle", "Circle", "Text"])
            line_width = st.sidebar.slider("Line Width", 1, 10, 4)  # Adding line width slider
            if annotation_type != "Text":
                st.sidebar.write(f"Enter coordinates for {annotation_type} annotation.")
                if annotation_type == "Line":
                    point_1 = st.sidebar.text_input("Enter point 1 coordinates (x, y)", value=(int(width/8), int(height/8)))
                    point_2 = st.sidebar.text_input("Enter point 2 coordinates (x, y)", value=(int(7*width/8), int(7*height/8)))
                    position = (eval(point_1), eval(point_2), line_width)
                elif annotation_type == "Rectangle":
                    top_left = st.sidebar.text_input("Enter top-left coordinates (x, y)", value=(int(width/4), int(height/4)))
                    bottom_right = st.sidebar.text_input("Enter bottom-right coordinates (x, y)", value=(int(3*width/4), int(3*height/4)))
                    position = (eval(top_left), eval(bottom_right), line_width)
                elif annotation_type == "Circle":
                    center = st.sidebar.text_input("Enter center coordinates (x, y)", value=(int(width/2), int(height/2)))
                    radius = st.sidebar.number_input("Enter radius", value=200)
                    position = (eval(center), radius, line_width)
            else:
                text_scale = st.sidebar.slider("Text Scale", 0.1, 10.0, 3.0)  # Adding text scale slider
                font_face = st.sidebar.selectbox("Select font face", ["Arial", "Times New Roman", "Courier", "Cursive"])
                text = st.sidebar.text_input("Enter text","Mohit Gupta")
                coordinates = st.sidebar.text_input("Enter coordinates (x, y)", value=(int(width/4), int(height/2)))
                position = (text, eval(coordinates), line_width, text_scale, font_face)

            # Add a color picker widget to select the color
            color = st.sidebar.color_picker("Select annotation color", "#ff0000")  # Default: Red

            annotated_image = original_image.copy()
            if st.sidebar.button("Clear Annotations"):
                annotated_image = original_image.copy()
            st.image(annotated_image, channels="BGR", caption="Annotated Image")

            if st.sidebar.button("Apply Annotation"):
                try:
                    annotated_image = add_annotations(annotated_image, annotation_type, position, color)
                    st.image(annotated_image, channels="BGR", caption="Annotated Image")
                    download_button(annotated_image, "Annotated Image")
                except Exception as e:
                    st.error(f"Error applying annotation: {e}")


def download_button(image, caption):
    # Convert image to bytes
    image_bytes = cv2.imencode('.png', image)[1].tobytes()
    # Create a download button
    bio = io.BytesIO(image_bytes)
    st.download_button(label="Download " + caption, data=bio, file_name=caption+'.jpg', mime='image/jpg')

if __name__ == "__main__":
    main()
