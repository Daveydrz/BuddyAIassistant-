# utils.py - Helper functions that everyone uses
import re
import time
import json
import os
from textblob import TextBlob

def is_echo(text, last_few_buddy=[]):
    """Check if text is likely an echo of Buddy's recent speech"""
    if not text or len(text.strip()) < 3:
        return False

    cleaned = re.sub(r'[^\w\s]', '', text.strip().lower())
    if not cleaned or len(cleaned.split()) < 2:
        return False

    # Check against recent Buddy responses
    for prev in last_few_buddy[-3:]:
        if not prev:
            continue
            
        prev_clean = re.sub(r'[^\w\s]', '', prev.strip().lower())
        if not prev_clean:
            continue
            
        # Calculate similarity
        import difflib
        ratio = difflib.SequenceMatcher(None, cleaned, prev_clean).ratio()
        word_diff = abs(len(cleaned.split()) - len(prev_clean.split()))

        if ratio > 0.87 and word_diff <= 4:
            return True

    return False

def is_noise_or_gibberish(text):
    """Reject input if it's likely noise, gibberish, or too short"""
    if not text or len(text.strip()) < 2:
        return True
    words = text.strip().split()
    avg_len = sum(len(w) for w in words) / len(words) if words else 0
    if len(words) < 2 and avg_len < 4:
        return True
    return False

def analyze_emotion(text):
    """Returns emotion and confidence score"""
    if not text.strip():
        return "neutral", 0
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.25:
        return "positive", polarity
    elif polarity < -0.25:
        return "negative", polarity
    else:
        return "neutral", polarity

def clean_text_for_tts(text):
    """Clean text for better TTS output"""
    # Remove markdown
    text = re.sub(r'\*\*.*?\*\*', '', text)
    text = re.sub(r'\*.*?\*', '', text)
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    return text.strip()

def should_end_conversation(text):
    """Check if user wants to end conversation"""
    end_phrases = [
        "koniec", "do widzenia", "dziękuję", "thanks", "bye", 
        "goodbye", "that's all", "quit", "exit"
    ]
    if not text:
        return False
    lower = text.strip().lower()
    return any(phrase in lower for phrase in end_phrases)