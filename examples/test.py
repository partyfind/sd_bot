from transformers import GPT2Tokenizer, GPT2LMHeadModel
tokenizer = GPT2Tokenizer.from_pretrained('distilgpt2')
tokenizer.add_special_tokens({'pad_token': '[PAD]'})
model = GPT2LMHeadModel.from_pretrained('FredZhang7/distilgpt2-stable-diffusion-v2')

prompt = r'a cat sitting'     # the beginning of the prompt
temperature = 0.9             # a higher temperature will produce more diverse results, but with a higher risk of less coherent text
top_k = 8                     # the number of tokens to sample from at each step
max_length = 80               # the maximum number of tokens for the output of the model
repitition_penalty = 1.2      # the penalty value for each repetition of a token
num_return_sequences=5        # the number of results to generate

# generate the result with contrastive search
input_ids = tokenizer(prompt, return_tensors='pt').input_ids
output = model.generate(input_ids, do_sample=True, temperature=0.9, top_k=8, max_length=200, num_return_sequences=1, repetition_penalty=1.2, penalty_alpha=0.6, no_repeat_ngram_size=1, early_stopping=True)

print('\nInput:\n' + 100 * '-')
print('\033[96m' + prompt + '\033[0m')
print('\nOutput:\n' + 100 * '-')
for i in range(len(output)):
    print('\033[92m' + tokenizer.decode(output[i], skip_special_tokens=True) + '\033[0m\n')
