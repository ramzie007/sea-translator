import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/../"))
from helpers import chunk_text_sentences, build_translate_prompt


def test_chunk_text_sentences():
    text = "Hello world! How are you? Fine."
    chunks = chunk_text_sentences(text, 10)
    assert len(chunks) == 3
    assert all(isinstance(c, str) for c in chunks)


def test_build_translate_prompt():
    chunk = "Hello world."
    lang = "thai"
    prompt = build_translate_prompt(chunk, lang)
    assert isinstance(prompt, list)
    assert prompt[0]["role"] == "system"
    assert lang in prompt[0]["content"].lower()
    assert prompt[1]["role"] == "user"
    assert chunk in prompt[1]["content"]
