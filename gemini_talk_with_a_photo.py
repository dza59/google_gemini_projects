import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv
import io
from PIL import Image

def ask_and_get_answer(prompt, img):
    # set the GenerativeModel to use Gemini-Pro-Vision model
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([prompt, img])
    return response.text

def st_image_to_pil(st_image):

    # read imagee BytesIO object then convert into a PIL Image object
    image_data = st_image.read()
    pil_image = Image.open(io.BytesIO(image_data))
    return pil_image


if __name__ == '__main__':

    # configuration
    load_dotenv(find_dotenv(), override=True)
    genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

    # set titles on 
    st.cache_data.clear()
    st.title('ThereWeGo')
    st.subheader('Talking With an Image ✨')

    # creating a file upload widget for the user to select an image
    img = st.file_uploader('Select an Image: ', type=['jpg', 'jpeg', 'png', 'gif'])

    if img:
        st.image(img, caption='Talk with this image.')

        prompt = st.text_area('Ask a question about this image: ')

        # if the user has entered a question, make the Gemini API call get response
        if prompt:
            pil_image = st_image_to_pil(img)

            # creating a spinner
            with st.spinner('Running ...'):
                answer = ask_and_get_answer(prompt, pil_image)
                st.text_area('Gemini Answer: ', value=answer)

            # add a divider to separate the current answers from history
            st.divider()

            # creating a key in the session state
            if 'history' not in st.session_state:
                st.session_state.history = ''

            value = f'Q: {prompt} \n\n A: {answer}'
            st.session_state.history = f'{value} \n\n {"-" * 100} \n\n {st.session_state.history}'

            # saving the chat history
            h = st.session_state.history

            # display chat history
            st.text_area(label='Chat History', value=h, height=400, key='history')

    
# Run the app: streamlit run ./gemini_talk_with_a_photo.py