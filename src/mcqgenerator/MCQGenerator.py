## This is the file that will contain the main code 
### After initializing this file, in the root directory 
#### of this project, initialize a response.json file 

## response.json file will essentially have the RESPONSE_JSON that
### was made in the experiment jupyter notebook 

## 1. Import everything (we're just copying-pasting from experiment notebook)
import os
import pandas as pd 
import json 
import traceback 
import numpy as np

from langchain.chat_models import ChatOpenAI ##Lets us access OpenAI with LangChain
from dotenv import load_dotenv

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.callbacks import get_openai_callback
import PyPDF2

#import these two things from our created packages: 
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging 


#load OpenAI API key
load_dotenv()

KEY = os.getenv("OPENAI_API_KEY")

#call OpenAI LLM (GPT 3.5 turbo):
llm = ChatOpenAI(openai_api_key = KEY, 
                 model_name = 'gpt-3.5-turbo', 
                 temperature = 0.3) ##temperature means how creative the answers will be (0 = not create, 2 = ,most creative)


##Create prompt template 
## The below prompt is a "FEW SHOT PROMPT"
### In this prompt type, we are giving a bit of context and instruction to the model
### ZERO SHOT prompt would be if we just ask a straightforward question (like "who was the winner of the 1979 Cricket World Cup?")
TEMPLATE = """
Text: {text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quize o {number} multiple choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
Ensure to make {number} MCQs. 

### RESPONSE_JSON
{response_json}

"""

##create input PromptTemplate using above template: 
quiz_generation_prompt = PromptTemplate(
    input_variables= ['text', 'number', 'subject', 
                      'tone', 'response_json'], 
                      template = TEMPLATE 
)

# Create a Chain object, to connect the llm with the above PromptTemplate
quiz_chain = LLMChain(llm = llm, prompt = quiz_generation_prompt, 
                      output_key = 'quiz', verbose = True)

##In the above, the output of the quiz chain (the quiz itself) will be 
##stored in the variable "quiz" (indicated by output_key)
### The output_key's purpose is so that we can reference it in any other template we may end up SequentialChain-ing to this chain

# Create another template to evaluate the quiz 
SECOND_TEMPLATE = """ 
You are an expert English grammarian and writer. Given a Multiple Choice Quiz for {subject} students, \
you need to evauate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity. \
If the quiz is not at par with cognitive and analytical abilities of the students, \
update the quiz questions which needs to be changed, and change the tone such that it perfectly fits the student's ability. \
Quiz_MCQs: 
{quiz}

Check from an expert English writer of the above quiz: 

"""

##For the above template, create another PromptTemplate, and another chain
quiz_evaluation_prompt = PromptTemplate(input_variables = ['subject', 'quiz'], 
                                        template = SECOND_TEMPLATE)

review_chain = LLMChain(llm = llm, prompt = quiz_evaluation_prompt, 
                        output_key = 'review', verbose = True)


## Now combine the two chains by using SequentialChain object
generate_evaluate_chain = SequentialChain(chains = [quiz_chain, review_chain], 
                                          input_variables = ['text', 'number', 'subject', 'tone', 'response_json'],
                                          output_variables = ['quiz', 'review'], verbose = True)


##Now, in utils.py file, create the helper functions that will be used (in our case, to get the data) 


