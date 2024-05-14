##The streamlit app wil live here
import os 
import json 
import traceback 
import pandas as pd 
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging 

##if for some reason "module does not exist" in terminal, run pip install -r requirements.txt

##Step 1: Load json response: 
with open('/Users/test/MCQGenerator/response.json') as file:
    RESPONSE_JSON = json.load(file)

## Step 2: create title for app 
st.title('MCQ Generator Application with LangChain')

## Create form using st.form
with st.form('user_inputs'):
    #File upload: 
    uploaded_file = st.file_uploader("Upload a PDF or tct file")

    #Inout fields
    mcq_count = st.number_input('No. of MCQs', min_value = 3, max_value = 50)

    #subject
    subject = st.text_input('Insert Subject', max_chars = 20)

    #Quiz Tone (difficulty level)
    tone = st.text_input('Complexity Level of Questions', max_chars = 20, placeholder = 'Simple')

    #add button 
    button = st.form_submit_button('Create MCQs')

    #Check if the button is clicked and all fields have input: 
    if button and uploaded_file is not None and mcq_count and subject and tone: 
        with st.spinner('Loading...'):
            try: 
                text = read_file(uploaded_file)
                #count tokens and the cosft of OpenAI
                with get_openai_callback() as cb: 
                    response = generate_evaluate_chain(
                        {
                            'text': text, 
                            'number': mcq_count, 
                            'subject': subject, 
                            'tone': tone, 
                            'response_json': json.dumps(RESPONSE_JSON)

                        }
                    )

                #st.write(response)

            except Exception as e:
                traceback.print_exception(type(e), e, e.__trackeback__)
                st.error('Error')

            else: 
                print(f'Total tokens: {cb.total_tokens}')
                print(f'Prompt tokens: {cb.prompt_tokens}')
                print(f'Completion tokens: {cb.completion_tokens}')
                print(f'Total cost: {cb.total_cost}')

                if isinstance(response, dict):
                    #extract quiz data from response
                    quiz = response.get('quiz', None)
                    if quiz is not None: 
                        table_data = get_table_data(quiz)
                        if table_data is not None: 
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)

                            #Display the review in a text box as well
                            st.text_area(label= 'Review', value = response['review'])

                        else:
                            st.error('Error in table data')

                else:
                    st.write(response)

                    


