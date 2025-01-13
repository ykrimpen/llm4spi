import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

from datetime import datetime
from typing import Dict, List
import os
import time

from data import ZEROSHOT_DATA, read_problems, write_jsonl
from openai4spi import PromptResponder, generate_results

from prompting import create_prompt
from evaluation import evaluate_task_results



# client = ChatCompletionsClient(
#     endpoint = "https://Llama-3-3-70B-Instruct-trrpq.eastus.models.ai.azure.com",
#     credential = AzureKeyCredential(os.environ["AZURE_API_KEY"]),
# )

# model_info = client.get_model_info()

# print(f"Model name: {model_info.model_name}")
# print(f"Model provider name: {model_info.model_provider_name}")
# print(f"Model type: {model_info.model_type}")

# response = client.complete(
#     messages=[
#         SystemMessage(content="You are a helpful assistant."),
#         UserMessage(content="How many feet are in a mile?"),
#     ]
# )

# print(response.choices[0].message.content)


class MyAzure_Client(PromptResponder):
    """
    An instance of prompt-responder that uses a GPT4All's LLM as the backend model.
    """
    def __init__(self, endpoint: str, api_key: str):
        PromptResponder.__init__(self)
        if not endpoint or not api_key:
            raise ValueError("Both 'endpoint' and 'api_key' must be provided.")
        
        self.client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(api_key)
        )

    
    def completeIt(self, prompt:str) -> str:
        if self.DEBUG: print(">>> PROMPT:\n" + prompt)
        completion  = self.client.complete(
                messages=[
                    UserMessage(content=prompt)
                ]
            )
        reponse = completion.choices[0].message.content
        if self.DEBUG: print(">>> raw response:\n" + reponse)
        return reponse
    

if __name__ == '__main__':
    # endpoint = "https://Llama-3-3-70B-Instruct-trrpq.eastus.models.ai.azure.com"
    # api_key = os.getenv("AZURE_API_KEY")
    endpoint = "https://Phi-3-5-MoE-instruct-tzpmi.eastus.models.ai.azure.com"
    api_key = "GuiupoqWIhSHyco3gxBkfhm0YFphqIsG"
    myAIclient = MyAzure_Client(endpoint, api_key)
    myAIclient.DEBUG = True

    dataset = ZEROSHOT_DATA
    ROOT = os.path.dirname(os.path.abspath(__file__))
    #dataset = os.path.join(ROOT, "..", "..", "llm4spiDatasets", "data", "x.json")
    dataset = os.path.join(ROOT, "..", "..", "llm4spiDatasets", "data", "simple-specs.json")

    generate_results(myAIclient,
                     dataset, 
                     specificProblem = None,
                     experimentName = "Phi-3-5-MoE-instruct",     
                     enableEvaluation=True, 
                     prompt_type="usePredDesc"
                     #prompt_type="cot2"
                     )