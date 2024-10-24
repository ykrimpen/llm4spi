

# transform Human-evals dataset to a slightly different jsonlines format:
def reformat_HE_json(HE_data_file:str , outputfile:str) :
    with open(HE_data_file) as f:
       content = f.read().strip()
    lines = content.split('\n')
    lines = [ '   ' + z for z in lines]

    new_content = '[\n' + ',\n'.join(lines) + '\n]'

    with open(outputfile,'w') as f:
        f.write(new_content)

if __name__ == '__main__':
   reformat_HE_json("../../human-eval/HumanEval.jsonl","humaneval-reformatted.json")

