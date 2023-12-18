import os

from langchain.chains import LLMChain, SequentialChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

from prompts import *
from secret_key import openai_api_key

# Setup the OpenAI API key
os.environ["OPENAI_API_KEY"] = openai_api_key


# Define the OpenAI LLM model
def define_llm_model(model_name, temperature, max_tokens):
    if model_name == "gpt-3.5-turbo":
        llm_model = ChatOpenAI(
            model_name=model_name,
            max_tokens=int(max_tokens),
            temperature=float(temperature)
        )
    else:
        llm_model = OpenAI(
            model_name=model_name,
            max_tokens=int(max_tokens),
            temperature=float(temperature)
        )
    return llm_model


# Function to generate mermaid code for the given input text
def generate_mermaid_code(input_text, model_name, temperature, max_tokens, prompt_type):
    llm_model = define_llm_model(model_name, temperature, max_tokens)

    instructions = """
               - strict rules: do not explain the code and do not add any additional text except code
               - do not use ``` and do not add mermaid text in the code"""

    if prompt_type == "Zero-shot":
        # Define the prompt template
        prompt = PromptTemplate(
            input_variables=["instructions", "input_text"],
            template="{instructions} Generate a flowchart mermaid code for the text: {input_text}"
        )

        # Create the LLM chain and pass llm model, prompt as parameters
        llm_chain = LLMChain(
            llm=llm_model,
            prompt=prompt
        )

        # Run the chain to generate the mermaid code for the input text
        response_code = llm_chain.run(instructions=instructions, input_text=input_text)
        response = response_code.strip()

    if prompt_type == "Few-shot":
        # Define the prompt for the input text to break down the given text into sequence of steps
        prompt_template_sequence_steps = PromptTemplate(
            input_variables=["sequence_steps_example", "input_text"],
            template="{sequence_steps_example} Breakdown the given text into sequence steps: {input_text}"
        )

        # Create the LLM chain for the prompt template: prompt_template_sequence_steps
        sequence_steps_chain = LLMChain(llm=llm_model, prompt=prompt_template_sequence_steps,
                                        output_key="sequence_steps")

        prompt_template_mermaid_code = PromptTemplate(
            input_variables=["mermaid_code_example", "instructions", "sequence_steps"],
            template="{mermaid_code_example} - {instructions} Generate a flowchart mermaid code for the {sequence_steps}"
        )

        # Create the LLM chain for the prompt template: prompt_template_mermaid_code
        mermaid_code_chain = LLMChain(llm=llm_model, prompt=prompt_template_mermaid_code, output_key="mermaid_code")

        # Create the Sequential chain to join above two chains to generate mermaid code
        final_chain = SequentialChain(chains=[sequence_steps_chain, mermaid_code_chain],
                                      input_variables=["sequence_steps_example",
                                                       "input_text",
                                                       "mermaid_code_example",
                                                       "instructions"],
                                      output_variables=["sequence_steps", "mermaid_code"])

        # Run the chains to generate the mermaid code for the input text
        response_code = final_chain({"sequence_steps_example": sequence_steps_example,
                                     "input_text": input_text,
                                     "mermaid_code_example": mermaid_code_example,
                                     "instructions": instructions})
        response = response_code.get('mermaid_code').strip()

    # Return the response
    return response

# if __name__ == "__main__":
#     print(generate_mermaid_code(
#         "For Christmas shopping, we need first need to have some money. Then we go shopping, and then think what we "
#         "want to buy. The things we can buy are iPhone, car or laptop", "gpt-3.5-turbo", "0.0", "700"))
