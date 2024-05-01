from unsloth import FastLanguageModel

from code_repo_dataset import qa_prompt
from train import max_seq_length, dtype, load_in_4bit

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="lora_model",  # YOUR MODEL YOU USED FOR TRAINING
    max_seq_length=max_seq_length,
    dtype=dtype,
    load_in_4bit=load_in_4bit,
)

FastLanguageModel.for_inference(model)  # Enable native 2x faster inference

input_str = qa_prompt.format(
    "Continue the fibonnaci sequence.",  # instruction
    "1, 1, 2, 3, 5, 8",  # input
    "",  # output - leave this blank for generation!
)

inputs = tokenizer([input_str], return_tensors="pt").to("cuda")

outputs = model.generate(**inputs, max_new_tokens=64, use_cache=True)
tokenizer.batch_decode(outputs)
