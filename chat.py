import argparse
from transformers import AutoModelWithLMHead, AutoTokenizer
import torch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

parser = argparse.ArgumentParser(
    description="Process chatbot variables. for help run python app.py -h"
)
parser.add_argument(
    "-m", "--model", type=str, default="medium", help="Size of DialoGPT model"
)
parser.add_argument(
    "-s",
    "--steps",
    type=int,
    default=7,
    help="Number of steps to run the Dialogue System for",
)

args = parser.parse_args()
tokenizer = AutoTokenizer.from_pretrained(f"microsoft/DialoGPT-{args.model}")
model = AutoModelWithLMHead.from_pretrained(f"microsoft/DialoGPT-{args.model}")

bot_name = "Sam"

def get_response(msg):
    for step in range(args.steps):
        new_user_input_ids = tokenizer.encode(
            msg + tokenizer.eos_token, return_tensors="pt"
            )
        bot_input_ids = (
            torch.cat([chat_history_ids, new_user_input_ids], dim=-1)
            if step > 0
            else new_user_input_ids
            )
        chat_history_ids = model.generate(
            bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id
            )

        ans = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)    
        return str(ans)


if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(resp)

