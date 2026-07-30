from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file  

import streamlit as st
import os
from PIL import Image
from google import genai


client = genai.Client(api_key="AQ.Ab8RN6IrwgI0KqlxnfDkP7Ms90MhQRv832ipAOlURWbSeoY9Lg")



def get_gemini_response(input_prompt, image, user_prompt):
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=[
            input_prompt,
            {
                "inline_data": {
                    "mime_type": image[0]["mime_type"],
                    "data": image[0]["data"],
                }
            },
            user_prompt,
        ],
    )

    return response.text



# def get_gemini_response(input,image,user_prompt):
#     response = model.generate_content([input,image[0],user_prompt])
#     return response.text  # Return the generated text from the response

## img to byte convert and focus on data and mimetype
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # read the file into byte   
        image_bytes = uploaded_file.getvalue()

        image_parts= [
            {
                "mime_type": uploaded_file.type,    
                "data": image_bytes
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded. Please upload an image of the invoice.")


## initilize the streamlit app
st.set_page_config(page_title="Multilanguage Invoice Extractor")

st.header("Multilanguage Invoice Extractor")
input=st.text_input("input prompt: ",key="input")
upload_file= st.file_uploader("choose an image of invoice", type=["jpg", "jpeg", "png"], key="image")

submit=st.button("Tell me about the invoice")

input_prompt="""
You are an expert in understanding invoices. We will upload an image as invoice
and you will have to answer any questions based on the uploaded invoice immage.
"""

## if submit button is clicked
if submit:
    image_data=input_image_details(upload_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("the response is:")
    st.write(response)