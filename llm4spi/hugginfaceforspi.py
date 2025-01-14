from huggingface_hub import InferenceClient

from datetime import datetime
from typing import Dict, List
import os
import time

from data import ZEROSHOT_DATA, read_problems, write_jsonl
from openai4spi import PromptResponder, generate_results

from prompting import create_prompt
from evaluation import evaluate_task_results


class MyHugginface_Client(PromptResponder):
    """
    An instance of prompt-responder that uses a GPT4All's LLM as the backend model.
    """
    def __init__(self, client:InferenceClient, modelId:str):
        PromptResponder.__init__(self)
        self.client = client
        self.model = modelId 
    
    def completeIt(self, prompt:str) -> str:
        if self.DEBUG: print(">>> PROMPT:\n" + prompt)
        completion  = self.client.chat.completions.create(
                model=self.model, 
                messages=[
                {
                    "role": "user",
                    "content": prompt
                }
                ]
            )
        response = completion.choices[0].message.content
        if self.DEBUG: print(">>> raw response:\n" + response)
        return response
    

if __name__ == '__main__':
    Hugginface_api_key = os.environ.get('HUGGINFACE_API_KEY') 
    client = InferenceClient(api_key=Hugginface_api_key)
    model = "google/gemma-2-27b-it"
    myAIclient = MyHugginface_Client(client, model)
    myAIclient.DEBUG = True

    dataset = ZEROSHOT_DATA
    ROOT = os.path.dirname(os.path.abspath(__file__))
    #dataset = os.path.join(ROOT, "..", "..", "llm4spiDatasets", "data", "x.json")
    dataset = os.path.join(ROOT, "..", "..", "llm4spiDatasets", "data", "simple-specs.json")

    generate_results(myAIclient,
                     dataset, 
                     specificProblem = None,
                     experimentName = "gemma-2-27b-it",     
                     enableEvaluation=True, 
                     prompt_type="usePredDesc"
                     #prompt_type="cot2"
                     )
    
