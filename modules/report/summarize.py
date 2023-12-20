from transformers import pipeline, T5ForConditionalGeneration, T5Tokenizer

def summarize_text(text):
    model_name = "t5-small"
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    tokenizer = T5Tokenizer.from_pretrained(model_name)

    inputs = tokenizer("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(inputs["input_ids"], max_length=150, min_length=30, length_penalty=2, num_beams=4, temperature=0.9)

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

