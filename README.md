# Project: using LLMs to write SPises

Since LLMs are so smart, we wonder how good they are for generating 'formal' specifications. Or at least, specifications that can be executed so we can actually use them for checking the inputs and outputs of programs under test.

In the current study we look both commercial LLMs like OpenAI GPT as well open source LLMs for writing specifications in the form of pre- and post-conditions.

simple-specs, N=25.

  |  | accepted |
  |--|----------|
  | GPT 3.5         | 76%  |
  | GPT 4           | 88%  |
  | Meta-Llama-3-8B | 32%  |
  | Mistral-7B      | 10%  |
  | Orca-mini-3B    | 4%   |


Example prompt-1: _Give a Python program `Postcondition(x,y,z)` that checks whether the sum of x and y is zero or equal to z_

Answer by Orca-mini-3B: 😅

```python
Postcondition(x,y,z):
     if x + y == 0 or x - y == 0 or z - x == 0:
     return True
     else:
     return False
```

Example prompt-2: _Give a Python program `Postcondition(joke:str)` that checks whether the joke is indeed funny._ 😉

Answer by OpenAI's GPT:

```python
def Postcondition(joke: str) -> bool:
    # Use VADER for a basic sentiment analysis approach
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(joke)

    # Consider a joke "funny" if it has a positive sentiment
    if sentiment['pos'] > sentiment['neg']:
        return True
    return False

# Example usage
joke = "Why don't scientists trust atoms? Because they make up everything!"
print(Postcondition(joke))  # Output: True
```

#### Using GPT4All.

You can use a [Docker-image with GPT4All installed](https://hub.docker.com/r/morgaine/llm4spi). The image has:

* Ubuntu 22-04
* Python 3.12 installed
* NVIDIA Container Toolkit installed
* Vulkan SDK installed
* GPT4All installed (as a Python package)
