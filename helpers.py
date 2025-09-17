import requests
import re
from typing import List


def download_text(url: str) -> str:
    """Download text file from a URL."""
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.text


def chunk_text_sentences(text: str, max_chunk_chars: int) -> List[str]:
    """
    Split text by sentences (using regex), grouping up to max_chunk_chars per chunk.
    Returns a list of chunked strings.
    """
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks, curr, curr_len = [], [], 0
    for s in sentences:
        sentence_len = len(s) + 1
        if curr_len + sentence_len > max_chunk_chars and curr:
            chunks.append(" ".join(curr).strip())
            curr, curr_len = [s], sentence_len
        else:
            curr.append(s)
            curr_len += sentence_len
    if curr:
        chunks.append(" ".join(curr).strip())
    return chunks


def build_translate_prompt(chunk: str, target_language: str) -> List[dict]:
    """
    Build prompt for SEA-LION translation API.
    Returns a list of message dicts for OpenAI-compatible chat completion.
    """
    system_msg = (
        f"You are a precise translator. Translate the following English text into {target_language}. "
        "Preserve formatting and line breaks. Output ONLY the translation."
    )
    return [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": chunk},
    ]


def translate_chunk(client, model: str, messages: List[dict]) -> str:
    """
    Call SEA-LION API to translate a chunk of text.
    Returns the translated string.
    """
    completion = client.chat.completions.create(
        model=model, messages=messages, temperature=0.0
    )
    return completion.choices[0].message.content or ""
