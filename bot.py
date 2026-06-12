"""
Bot Telegram — detektor technik perswazji (PL/UA).
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

# ============ KONFIGURACJA ============
BOT_TOKEN      = os.getenv("BOT_TOKEN")
MODEL_DIR      = Path("./model")
MAX_LENGTH     = 256
MAX_CHUNK_CHARS = 400   # maks. znakow w jednym chunku (ciche dzielenie dlugich akapitow)
TG_LIMIT       = 4000
LANGS_FILE     = Path("./user_langs.json")   # tu zapisujemy wybor jezyka per user_id

# ============ JEZYKI ============
STRINGS = {
    "pl": {
        "start":        "Cześć! Wyślij mi tekst, a wykryję w nim techniki perswazji akapit po akapicie.\n\nOddziel akapity pustą linią.\n\nKomendy:\n/help — lista wszystkich technik\n/about - informacja dotycząca modelu\n/language — zmień język",
        "analyzing":    "Analizuję…",
        "no_text":      "Nie znalazłem tekstu do analizy.",
        "no_technique": "— brak wykrytych technik",
        "legend_title": "ℹ️ Co oznaczają wykryte techniki:",
        "paragraph":    "Akapit",
        "confidence":   "pewność",
        "high":         "wysoka",
        "medium":       "średnia",
        "low":          "niska",
        "help_title":   "23 techniki perswazji, które wykrywam:",
        "error":        "Wystąpił błąd podczas analizy. Spróbuj ponownie za chwilę.\nJeśli problem się powtarza, skróć tekst lub podziel go na mniejsze części.",
        "lang_choose":  "Wybierz język / Оберіть мову:",
        "lang_set":     "Język ustawiony na: Polski 🇵🇱",
        "about": (
            "O modelu:\n\n"
            "Model: XLM-RoBERTa-large\n"
            "Zadanie: wykrywanie technik perswazji na poziomie akapitu (multi-label)\n"
            "Dane: SemEval 2023 Task 3 — ok. 20k akapitów w 9 językach\n"
            "Dokładność: micro-F1 ≈ 0.45 na polskim zbiorze testowym\n"
            "Klas: 23 techniki"
            "GitHub: https://github.com/Mishtar4/persuasion-bot\n"
            "Model: https://huggingface.co/Mishtar4/persuasion-detector-xlm-roberta"
        ),
    },
    "ua": {
        "start":        "Привіт! Надішли мені текст, і я знайду в ньому техніки переконання абзац за абзацом.\n\nРозділяй абзаци порожнім рядком.\n\nКоманди:\n/help — список усіх технік\n/about - інформація про модель\n/language — змінити мову",
        "analyzing":    "Аналізую…",
        "no_text":      "Не знайшов тексту для аналізу.",
        "no_technique": "— технік не виявлено",
        "legend_title": "ℹ️ Що означають виявлені техніки:",
        "paragraph":    "Абзац",
        "confidence":   "впевненість",
        "high":         "висока",
        "medium":       "середня",
        "low":          "низька",
        "help_title":   "23 техніки переконання, які я розпізнаю:",
        "error":        "Виникла помилка під час аналізу. Спробуй ще раз.\nЯкщо проблема повторюється — скороти текст або розбий на менші частини.",
        "lang_choose":  "Wybierz język / Оберіть мову:",
        "lang_set":     "Мову встановлено: Українська 🇺🇦",
        "about": (
            "Про модель:\n\n"
            "Модель: XLM-RoBERTa-large\n"
            "Завдання: виявлення технік переконання на рівні абзацу (multi-label)\n"
            "Дані: SemEval 2023 Task 3 — блол 20k абзаців у 9 мовах\n"
            "Точність: micro-F1 ≈ 0.45 на польському тестовому наборі\n"
            "Класів: 23 техніки"
            "GitHub: https://github.com/Mishtar4/persuasion-bot\n"
            "Модель: https://huggingface.co/Mishtar4/persuasion-detector-xlm-roberta"
        ),
    },
}

OPISY = {
    "pl": {
        "Appeal_to_Authority":              'zamiast podać dowody, autor powołuje się na kogoś sławnego lub ważnego — „ekspert powiedział, więc musi być prawda"',
        "Appeal_to_Popularity":             'argument, że coś jest słuszne tylko dlatego, że robi to wiele osób — „wszyscy tak myślą, więc i ty powinieneś"',
        "Appeal_to_Values":                 'odwołanie do emocji i wartości (patriotyzm, rodzina, tradycja) zamiast do faktów i logiki',
        "Appeal_to_Fear-Prejudice":         'straszenie katastrofą lub odwoływanie się do uprzedzeń, by wywołać strach i wyłączyć krytyczne myślenie',
        "Flag_Waving":                      'granie na dumie narodowej lub grupowej — „my jesteśmy lepsi, oni są gorsi"',
        "Causal_Oversimplification":        'złożony problem ma wiele przyczyn, ale autor wskazuje tylko jedną — „wszystkiemu winni są imigranci/politycy/media"',
        "False_Dilemma-No_Choice":          'przedstawienie sytuacji jako wyboru między tylko dwiema opcjami — „albo z nami, albo przeciwko nam"',
        "Consequential_Oversimplification": 'twierdzenie, że jedno wydarzenie nieuchronnie wywoła lawinę złych skutków — „jeśli to dopuścimy, stanie się X, Y i Z"',
        "Straw_Man":                        'celowe przekręcenie słów przeciwnika, by łatwiej go zaatakować — krytykuje się coś, czego on nigdy nie powiedział',
        "Red_Herring":                      'zmiana tematu na coś nieistotnego, by odwrócić uwagę od prawdziwego problemu',
        "Whataboutism":                     'odpowiedź na krytykę przez wskazanie cudzych win — „a wy to co zrobiliście?"',
        "Slogans":                          'krótkie, chwytliwe hasło powtarzane zamiast rzeczowego argumentu',
        "Appeal_to_Time":                   'sztuczna presja czasu — „działaj teraz, bo za chwilę będzie za późno"',
        "Conversation_Killer":              'zdanie ucinające dyskusję zanim się zacznie — „to nie podlega dyskusji", „sprawa jest zamknięta"',
        "Loaded_Language":                  'używanie słów silnie nacechowanych emocjonalnie, by wywołać reakcję bez podawania faktów',
        "Repetition":                       'wielokrotne powtarzanie tego samego przekazu — im częściej słyszymy, tym bardziej wierzymy',
        "Exaggeration-Minimisation":        'wyolbrzymianie tego, co pasuje, i pomniejszanie tego, co nie pasuje',
        "Obfuscation-Vagueness-Confusion":  'celowo niejasny, zawiły język, który ukrywa brak argumentów',
        "Name_Calling-Labeling":            'przyklejanie obraźliwych etykiet zamiast merytorycznej dyskusji — „faszysta", „zdrajca", „lewak"',
        "Doubt":                            'podważanie wiarygodności osoby lub źródła bez konkretnych dowodów — „czy można mu ufać?"',
        "Guilt_by_Association":             'dyskredytacja przez skojarzenie z osobą lub grupą o złej reputacji — „on zna X, więc sam jest podejrzany"',
        "Appeal_to_Hypocrisy":              'odpieranie zarzutów przez wskazanie, że rozmówca sam postępuje podobnie — „sam nie jesteś bez winy"',
        "Questioning_the_Reputation":       'atak na reputację osoby zamiast na jej argumenty — „kto ty jesteś, żeby się wypowiadać?"',
    },
    "ua": {
        "Appeal_to_Authority":              'замість доказів автор посилається на когось відомого — «експерт сказав, значить правда»',
        "Appeal_to_Popularity":             'щось є правильним лише тому, що так думають усі — «всі так роблять, і ти повинен»',
        "Appeal_to_Values":                 'звернення до емоцій і цінностей (патріотизм, сім\'я, традиція) замість фактів',
        "Appeal_to_Fear-Prejudice":         'залякування катастрофою або апеляція до упереджень, щоб вимкнути критичне мислення',
        "Flag_Waving":                      'гра на національній або груповій гордості — «ми кращі, вони гірші»',
        "Causal_Oversimplification":        'складна проблема має багато причин, але автор вказує лише одну — «у всьому винні мігранти/політики/медіа»',
        "False_Dilemma-No_Choice":          'ситуацію подано як вибір між двома варіантами, хоча їх більше — «або з нами, або проти нас»',
        "Consequential_Oversimplification": 'твердження, що одна подія неминуче спричинить лавину поганих наслідків — «якщо це допустимо, станеться X, Y і Z»',
        "Straw_Man":                        'навмисне перекручення слів опонента, щоб легше його атакувати — критикують те, чого він ніколи не казав',
        "Red_Herring":                      'зміна теми на щось несуттєве, щоб відвернути увагу від справжньої проблеми',
        "Whataboutism":                     'відповідь на критику через вказівку на чужі помилки — «а ви що зробили?»',
        "Slogans":                          'короткий, запам\'ятовуваний лозунг замість реального аргументу',
        "Appeal_to_Time":                   'штучний тиск часу — «дій зараз, бо завтра буде пізно»',
        "Conversation_Killer":              'фраза, що обриває дискусію до її початку — «це не підлягає обговоренню»',
        "Loaded_Language":                  'слова з сильним емоційним забарвленням, які мають викликати реакцію без фактів',
        "Repetition":                       'багаторазове повторення того самого — що частіше чуємо, то більше віримо',
        "Exaggeration-Minimisation":        'перебільшення того, що підходить, і применшення того, що не підходить',
        "Obfuscation-Vagueness-Confusion":  'навмисно нечітка, заплутана мова, яка приховує відсутність аргументів',
        "Name_Calling-Labeling":            'наклеювання образливих ярликів замість змістовної дискусії — «фашист», «зрадник»',
        "Doubt":                            'підрив довіри до особи або джерела без конкретних доказів — «чи можна йому довіряти?»',
        "Guilt_by_Association":             'дискредитація через асоціацію з особою або групою з поганою репутацією',
        "Appeal_to_Hypocrisy":              'відповідь на звинувачення тим, що співрозмовник сам так робить — «сам не без гріха»',
        "Questioning_the_Reputation":       'атака на репутацію людини замість її аргументів — «хто ти такий, щоб висловлюватись?»',
    },
}

# ============ PERSYSTENCJA JEZYKA ============
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

def get_lang(user_id: int) -> str:
    return load_langs().get(str(user_id), "pl")   # domyslnie polski

# ============ MODEL ============
logging.basicConfig(level=logging.INFO)
logging.info("Ladowanie modelu...")

device     = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer  = AutoTokenizer.from_pretrained(str(MODEL_DIR))
model      = AutoModelForSequenceClassification.from_pretrained(str(MODEL_DIR)).to(device).eval()
LABELS     = (MODEL_DIR / "labels.txt").read_text(encoding="utf-8").splitlines()
THRESHOLDS = np.load(MODEL_DIR / "thresholds.npy")
assert len(LABELS) == len(THRESHOLDS)
logging.info("Model gotowy (urzadzenie: %s).", device)


def podziel_na_chunki(tekst: str) -> list:
    """Dzieli dlugi akapit na chunki po zdaniach, max MAX_CHUNK_CHARS znakow."""
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
    """Klasyfikuje akapit z cichym podzialem na chunki. Zwraca max prob per klasa."""
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
                f"  \u2022 {nazwa} \u2014 {s['confidence']} {poziom(p, s)} ({p:.0%})"
                for nazwa, p in wykryte
            )
            bloki.append(f"{s['paragraph']} {i}: [{podglad}]\n{techniki}")
            wykryte_wszystkie.update(nazwa for nazwa, _ in wykryte)
        else:
            bloki.append(f"{s['paragraph']} {i}: [{podglad}]\n  {s['no_technique']}")

    wynik = "\n\n".join(bloki)
    if wykryte_wszystkie:
        legenda = "\n".join(
            f"  \u2022 {nazwa}: {opisy.get(nazwa, '')}\n"
            for nazwa in LABELS if nazwa in wykryte_wszystkie
        )
        wynik += "\n\n" + "\u2500" * 15 + "\n" + s["legend_title"] + "\n\n" + legenda
    return wynik

# ============ KLAWIATURA WYBORU JEZYKA ============
def lang_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Polski \U0001f1f5\U0001f1f1", callback_data="lang_pl"),
        InlineKeyboardButton(text="\u0423\u043a\u0440\u0430\u0457\u043d\u0441\u044c\u043a\u0430 \U0001f1fa\U0001f1e6", callback_data="lang_ua"),
    ]])

# ============ BOT ============
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(STRINGS["pl"]["lang_choose"], reply_markup=lang_keyboard())

@dp.message(Command("language"))
async def language_cmd(message: Message):
    await message.answer(STRINGS["pl"]["lang_choose"], reply_markup=lang_keyboard())

@dp.callback_query(F.data.in_({"lang_pl", "lang_ua"}))
async def set_language(callback: CallbackQuery):
    lang = callback.data.split("_")[1]
    save_lang(callback.from_user.id, lang)
    s = STRINGS[lang]
    await callback.message.answer(s["lang_set"])
    await callback.message.answer(s["start"])
    await callback.answer()

@dp.message(Command("help"))
async def help_cmd(message: Message):
    lang = get_lang(message.from_user.id)
    s = STRINGS[lang]
    opisy = OPISY[lang]
    linie = [s["help_title"] + "\n"]
    for nazwa, opis in opisy.items():
        linie.append(f"- {nazwa}:\n  {opis}")
    tekst = "\n\n".join(linie)
    for i in range(0, len(tekst), TG_LIMIT):
        await message.answer(tekst[i:i + TG_LIMIT])

@dp.message(Command("about"))
async def about_cmd(message: Message):
    lang = get_lang(message.from_user.id)
    await message.answer(STRINGS[lang]["about"])

@dp.message()
async def obsluga(message: Message):
    if not message.text:
        return
    lang = get_lang(message.from_user.id)
    s = STRINGS[lang]
    await message.answer(s["analyzing"])
    try:
        wynik = await asyncio.to_thread(analizuj, message.text, lang)
    except Exception as e:
        logging.error("Blad podczas analizy: %s", e)
        await message.answer(s["error"])
        return
    for i in range(0, len(wynik), TG_LIMIT):
        await message.answer(wynik[i:i + TG_LIMIT])

async def main():
    bot = Bot(BOT_TOKEN)
    logging.info("Bot wystartowal.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
