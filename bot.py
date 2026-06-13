"""
Telegram bot — persuasion technique detector (PL/UK).
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


def podziel_na_chunki(tekst: str) -> list:
    """Splits a long paragraph into chunks by sentence, max MAX_CHUNK_CHARS characters."""
    if len(tekst) <= MAX_CHUNK_CHARS:
        return [tekst]
    zdania = re.split(r'(?<=[.!?])\s+', tekst)
    chunki, obecny = [], ""
    for zdanie in zdania:
        if obecny and len(obecny) + len(zdanie) + 1 > MAX_CHUNK_CHARS:
            chunki.append(obecny.strip())
            obecny = zdanie
        else:
            obecny = (obecny + " " + zdanie).strip() if obecny else zdanie
    if obecny:
        chunki.append(obecny.strip())
    return chunki if chunki else [tekst]


def klasyfikuj_z_podzialem(tekst: str) -> list:
    """Classifies a paragraph with silent chunk splitting. Returns max probability per class."""
    chunki = podziel_na_chunki(tekst)
    if len(chunki) == 1:
        return klasyfikuj_akapit(tekst)
    maks = {}
    for chunk in chunki:
        for nazwa, p in klasyfikuj_akapit(chunk):
            maks[nazwa] = max(maks.get(nazwa, 0.0), p)
    return sorted(maks.items(), key=lambda x: -x[1])


@torch.no_grad()
def klasyfikuj_akapit(tekst: str):
    enc = tokenizer(tekst, truncation=True, max_length=MAX_LENGTH, return_tensors="pt").to(device)
    probs = torch.sigmoid(model(**enc).logits)[0].cpu().numpy()
    wykryte = [(LABELS[i], float(probs[i])) for i in range(len(LABELS)) if probs[i] >= THRESHOLDS[i]]
    return sorted(wykryte, key=lambda x: -x[1])

def poziom(p: float, s: dict) -> str:
    if p >= 0.80: return s["high"]
    if p >= 0.60: return s["medium"]
    return s["low"]

def analizuj(tekst: str, lang: str) -> str:
    s = STRINGS[lang]
    opisy = OPISY[lang]
    akapity = [p.strip() for p in tekst.split("\n\n") if p.strip()]
    if not akapity:
        return s["no_text"]

    bloki = []
    wykryte_wszystkie = set()
    for i, akapit in enumerate(akapity, 1):
        wykryte = klasyfikuj_z_podzialem(akapit)
        podglad = (akapit[:70] + "...") if len(akapit) > 70 else akapit
        if wykryte:
            techniki = "\n".join(
                f"  • {nazwa} — {s['confidence']} {poziom(p, s)} ({p:.0%})"
                for nazwa, p in wykryte
            )
            bloki.append(f"{s['paragraph']} {i}: [{podglad}]\n{techniki}")
            wykryte_wszystkie.update(nazwa for nazwa, _ in wykryte)
        else:
            bloki.append(f"{s['paragraph']} {i}: [{podglad}]\n  {s['no_technique']}")

    wynik = "\n\n".join(bloki)
    if wykryte_wszystkie:
        legenda = "\n".join(
            f"  • {nazwa}: {opisy.get(nazwa, '')}\n"
            for nazwa in LABELS if nazwa in wykryte_wszystkie
        )
        wynik += "\n\n" + "─" * 15 + "\n" + s["legend_title"] + "\n\n" + legenda
    return wynik

# ============ LANGUAGE SELECTION KEYBOARD ============
def lang_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Polski \U0001f1f5\U0001f1f1", callback_data="lang_pl"),
        InlineKeyboardButton(text="Українська \U0001f1fa\U0001f1e6", callback_data="lang_uk"),
    ]])

LANG_CHOOSE_TEXT = STRINGS["pl"]["lang_choose"]

# ============ BOT HANDLERS ============
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(LANG_CHOOSE_TEXT, reply_markup=lang_keyboard())

@dp.message(Command("language"))
async def language_cmd(message: Message):
    await message.answer(LANG_CHOOSE_TEXT, reply_markup=lang_keyboard())

@dp.callback_query(F.data.in_({"lang_pl", "lang_uk"}))
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
    opisy = OPISY[lang]
    linie = [s["help_title"] + "\n"]
    for nazwa, opis in opisy.items():
        linie.append(f"- {nazwa}:\n  {opis}")
    tekst = "\n\n".join(linie)
    for i in range(0, len(tekst), TG_LIMIT):
        await message.answer(tekst[i:i + TG_LIMIT])

@dp.message(Command("example"))
async def example_cmd(message: Message):
    lang = get_lang(message.from_user.id)
    if lang is None:
        await message.answer(LANG_CHOOSE_TEXT, reply_markup=lang_keyboard())
        return
    s = STRINGS[lang]
    przyklad = EXAMPLES[lang]
    await message.answer(f"{s['example_intro']}\n\n{przyklad}")
    wynik = await asyncio.to_thread(analizuj, przyklad, lang)
    await message.answer(f"{s['example_result_intro']}\n\n{wynik}")

@dp.message(Command("model"))
async def model_cmd(message: Message):
    lang = get_lang(message.from_user.id)
    if lang is None:
        await message.answer(LANG_CHOOSE_TEXT, reply_markup=lang_keyboard())
        return
    await message.answer(STRINGS[lang]["about"])

@dp.message()
async def obsluga(message: Message):
    if not message.text:
        return
    lang = get_lang(message.from_user.id)
    if lang is None:
        await message.answer(LANG_CHOOSE_TEXT, reply_markup=lang_keyboard())
        return
    s = STRINGS[lang]
    await message.answer(s["analyzing"])
    try:
        wynik = await asyncio.to_thread(analizuj, message.text, lang)
    except Exception as e:
        logging.error("Error during analysis: %s", e)
        await message.answer(s["error"])
        return
    for i in range(0, len(wynik), TG_LIMIT):
        await message.answer(wynik[i:i + TG_LIMIT])

async def main():
    bot = Bot(BOT_TOKEN)
    logging.info("Bot started.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
