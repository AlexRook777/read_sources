import re

def clean_string_keep_cyrillic_alphanumeric_and_space(text: str) -> str:
    filtered_chars = [char for char in text if char.isalnum() or char.isspace()]
    cleaned_text_step1 = "".join(filtered_chars)
    cleaned_text_step2 = re.sub(r'\s+', ' ', cleaned_text_step1).strip()
    return cleaned_text_step2