import os
import sys
import warnings
from audioTranscript import main

warnings.filterwarnings("ignore", message="Some weights of PegasusForConditionalGeneration were not initialized from the model checkpoint")

import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer, pipeline

# Check if CUDA is available and set the device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load the transcription
# transcription = open("output.txt", "r").read()
transcription = main()

# Pick model
model_name = "google/pegasus-xsum"

# Load pretrained tokenizer and model
pegasus_tokenizer = PegasusTokenizer.from_pretrained(model_name)
pegasus_model = PegasusForConditionalGeneration.from_pretrained(model_name).to(device)

# Define summarization pipeline
summarizer = pipeline(
    "summarization",
    model=model_name,
    tokenizer=pegasus_tokenizer,
    framework="pt",
    device=0 if device == "cuda" else -1
)

def memory_efficient_summarize(text, max_length=512, stride=100, min_length=30, max_length_output=150):
    inputs = pegasus_tokenizer(text, return_tensors="pt", max_length=max_length, truncation=True)
    input_ids = inputs.input_ids.to(device)
    attention_mask = inputs.attention_mask.to(device)

    summary = ""
    for i in range(0, input_ids.shape[1], stride):
        start_i = i
        end_i = min(i + max_length, input_ids.shape[1])

        chunk_input_ids = input_ids[:, start_i:end_i].to(device)
        chunk_attention_mask = attention_mask[:, start_i:end_i].to(device)

        generated_ids = pegasus_model.generate(
            chunk_input_ids,
            attention_mask=chunk_attention_mask,
            min_length=min_length,
            max_length=max_length_output,
            num_beams=2,
            no_repeat_ngram_size=3,
            early_stopping=True
        )

        chunk_summary = pegasus_tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        summary += chunk_summary + " "

        # Clear CUDA cache to free up memory
        if device == "cuda":
            torch.cuda.empty_cache()

    return summary.strip()

# Perform memory-efficient summarization
final_summary = memory_efficient_summarize(transcription)

out_file = open("summarized.txt", "w")
out_file.write(final_summary)
out_file.close()