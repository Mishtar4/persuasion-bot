"""
Telegram bot — persuasion technique detector (PL/UK/EN).
"""
import asyncio
import json
import logging
import re
import os
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path

import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from locales import STRINGS, OPISY, EXAMPLES

# ============ CONFIGURATION ============
BOT_TOKEN      = os.getenv("BOT_TOKEN")
MODEL_DIR      = Path("./model")
MAX_LENGTH     = 256
MAX_CHUNK_CHARS = 400   # max characters per chunk (silent splitting of long paragraphs)
TG_LIMIT       = 4000
LANGS_FILE     = Path("./user_langs.json")   # stores each user's language choice

# ============ LANGUAGE PERSISTENCE ============
def load_langs() -> dict:
    if LANGS_FILE.exists():
        try:
            return json.loads(LANGS_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def save_lang(user_id: int, lang: str):
    data = load_langs()
    data[str(user_id)] = lang
    LANGS_FILE.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

def get_lang(user_id: int) -> str | None:
    return load_langs().get(str(user_id))   # None = language not chosen yet

# ============ MODEL ============
logging.basicConfig(level=logging.INFO)
logging.info("Loading model...")

device     = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer  = AutoTokenizer.from_pretrained(str(MODEL_DIR))
model      = AutoModelForSequenceClassification.from_pretrained(str(MODEL_DIR)).to(device).eval()
LABELS     = (MODEL_DIR / "labels.txt").read_text(encoding="utf-8").splitlines()
THRESHOLDS = np.load(MODEL_DIR / "thresholds.npy")
assert len(LABELS) == len(THRESHOLDS)
logging.info("Model ready (device: %s).", device)


def split_into_chunks(text: str) -> list:
    """Splits a long paragraph into chunks by sentence, max MAX_CHUNK_CHARS characters."""
    if len(text) <= MAX_CHUNK_CHARS:
        return [text]
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks, current = [], ""
    for sentence in sentences:
        if current and len(current) + len(sentence) + 1 > MAX_CHUNK_CHARS:
            chunks.append(current.strip())
            current = sentence
        else:
            current = (current + " " + sentence).strip() if current else sentence
    if current:
        chunks.append(current.strip())
    return chunks if chunks else [text]


def classify_with_chunking(text: str) -> list:
    """Classifies a paragraph with silent chunk splitting. Returns max probability per class."""
    chunks = split_into_chunks(text)
    if len(chunks) == 1:
        return classify_paragraph(text)
    best = {}
    for chunk in chunks:
        for label, p in classify_paragraph(chunk):
            best[label] = max(best.get(label, 0.0), p)
    return sorted(best.items(), key=lambda x: -x[1])


@torch.no_grad()
def classify_paragraph(text: str):
    enc = tokenizer(text, truncation=True, max_length=MAX_LENGTH, return_tensors="pt").to(device)
    probs = torch.sigmoid(model(**enc).logits)[0].cpu().numpy()
    detected = [(LABELS[i], float(probs[i])) for i in range(len(LABELS)) if probs[i] >= THRESHOLDS[i]]
    return sorted(detected, key=lambda x: -x[1])

def confidence_level(p: float, s: dict) -> str:
    if p >= 0.80: return s["high"]
    if p >= 0.60: return s["medium"]
    return s["low"]

def analyze(text: str, lang: str) -> str:
    s = STRINGS[lang]
    descriptions = OPISY[lang]
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not paragraphs:
        return s["no_text"]

    blocks = []
    all_detected = set()
    for i, paragraph in enumerate(paragraphs, 1):
        detected = classify_with_chunking(paragraph)
        preview = (paragraph[:70] + "...") if len(paragraph) > 70 else paragraph
        if detected:
            techniques = "\n".join(
                f"  • {label} — {s['confidence']} {confidence_level(p, s)} ({p:.0%})"
                for label, p in detected
            )
            blocks.append(f"{s['paragraph']} {i}: [{preview}]\n{techniques}")
            all_detected.update(label for label, _ in detected)
        else:
            blocks.append(f"{s['paragraph']} {i}: [{preview}]\n  {s['no_technique']}")

    result = "\n\n".join(blocks)
    if all_detected:
        legend = "\n".join(
            f"  • {label}: {descriptions.get(label, '')}\n"
            for label in LABELS if label in all_detected
        )
        result += "\n\n" + "─" * 15 + "\n" + s["legend_title"] + "\n\n" + legend
    return result

# ============ LANGUAGE SELECTION KEYBOARD ============
def lang_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Polski \U0001f1f5\U0001f1f1", callback_data="lang_pl"),
        InlineKeyboardButton(text="Українська \U0001f1fa\U0001f1e6", callback_data="lang_uk"),
        InlineKeyboardButton(text="English \U0001f1ec\U0001f1e7", callback_data="lang_en"),
    ]])

LANG_CHOOSE_TEXT = STRINGS["en"]["lang_choose"]

# ============ BOT HANDLERS ============
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(LANG_CHOOSE_TEXT, reply_markup=lang_keyboard())

@dp.message(Command("language"))
async def language_cmd(message: Message):
    await message.answer(LANG_CHOOSE_TEXT, reply_markup=lang_keyboard())

@dp.callback_query(F.data.in_({"lang_pl", "lang_uk", "lang_en"}))
async def set_language(callback: CallbackQuery):
    lang = callback.data.split("_")[1]
    save_lang(callback.from_user.id, lang)
    s = STRINGS[lang]
    await callback.message.answer(s["lang_set"])
    await callback.message.answer(s["start"])
    await callback.answer()

@dp.message(Command("techniques"))
async def techniques_cmd(message: Message):
    lang = get_lang(message.from_user.id)
    if lang is None:
        await message.answer(LANG_CHOOSE_TEXT, reply_markup=lang_keyboard())
        return
    s = STRINGS[lang]
    descriptions = OPISY[lang]
    lines = [s["help_title"] + "\n"]
    for name, description in descriptions.items():
        lines.append(f"- {name}:\n  {description}")
    text = "\n\n".join(lines)
    for i in range(0, len(text), TG_LIMIT):
        await message.answer(text[i:i + TG_LIMIT])

@dp.message(Command("example"))
async def example_cmd(message: Message):
    lang = get_lang(message.from_user.id)
    if lang is None:
        await message.answer(LANG_CHOOSE_TEXT, reply_markup=lang_keyboard())
        return
    s = STRINGS[lang]
    sample = EXAMPLES[lang]
    await message.answer(f"{s['example_intro']}\n\n{sample}")
    result = await asyncio.to_thread(analyze, sample, lang)
    await message.answer(f"{s['example_result_intro']}\n\n{result}")

@dp.message(Command("model"))
async def model_cmd(message: Message):
    lang = get_lang(message.from_user.id)
    if lang is None:
        await message.answer(LANG_CHOOSE_TEXT, reply_markup=lang_keyboard())
        return
    await message.answer(STRINGS[lang]["about"])

@dp.message()
async def handle_message(message: Message):
    if not message.text:
        return
    lang = get_lang(message.from_user.id)
    if lang is None:
        await message.answer(LANG_CHOOSE_TEXT, reply_markup=lang_keyboard())
        return
    s = STRINGS[lang]
    await message.answer(s["analyzing"])
    try:
        result = await asyncio.to_thread(analyze, message.text, lang)
    except Exception as e:
        logging.error("Error during analysis: %s", e)
        await message.answer(s["error"])
        return
    for i in range(0, len(result), TG_LIMIT):
        await message.answer(result[i:i + TG_LIMIT])

async def main():
    bot = Bot(BOT_TOKEN)
    logging.info("Bot started.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
