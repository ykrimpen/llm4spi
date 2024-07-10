from gpt4all import GPT4All
model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf", model_path="~/models/") # downloads / loads a 4.66GB LLM
with model.chat_session():
    print(model.generate("Generate a python function that takes two inputs A and B, and returns whether A is less than B", max_tokens=1024))