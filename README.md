# 🔍 Persuasion Bot

Telegram bot that detects 23 persuasion techniques in text using a fine-tuned XLM-RoBERTa-large model. Analyzes text paragraph by paragraph. Supports English, Polish and Ukrainian.

## Demo

> Bot runs locally. Cloud deployment coming soon.

## How it works

1. User sends a text to the bot (paragraphs separated by blank lines)
2. Each paragraph is analyzed independently
3. Bot returns detected persuasion techniques with confidence levels (high / medium / low)
4. A legend explains each detected technique

## Model

Fine-tuned on SemEval 2023 Task 3 dataset (6 languages, ~19,900 training paragraphs).  
Micro-F1 ≈ 0.45 on Polish dev set.

👉 [Mishtar4/persuasion-detector-xlm-roberta](https://huggingface.co/Mishtar4/persuasion-detector-xlm-roberta) on HuggingFace

## Project Structure

```
persuasion-bot/
├── bot.py                  # Telegram bot (aiogram 3.x)
├── locales.py              # Localization
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── notebooks/
│   ├── 1_dane.ipynb        # Data preparation (SemEval 2023)
│   ├── 2_model.ipynb       # Fine-tuning XLM-RoBERTa
│   └── 3_analiza.ipynb     # Threshold tuning + analysis
└── model/                  # Model files (download from HuggingFace, see below)
    ├── model.safetensors
    ├── config.json
    ├── tokenizer.json
    ├── tokenizer_config.json
    ├── labels.txt
    └── thresholds.npy
```



## Installation

**1. Clone the repository**

```bash
git clone https://github.com/Mishtar4/persuasion-bot.git
cd persuasion-bot
```

**2. Create and activate virtual environment**

```bash
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Download the model**

The `model/` folder is not included in this repository. Download it from HuggingFace by running this Python script once:

```python
from huggingface_hub import snapshot_download
snapshot_download("Mishtar4/persuasion-detector-xlm-roberta", local_dir="./model")
```

This will automatically download all required model files into the `model/` directory.

**5. Configure environment variables**

Copy `.env.example` to `.env` and fill in your Telegram bot token:

```bash
cp .env.example .env
```

```
BOT_TOKEN=your_telegram_bot_token_here
```

**6. Run the bot**

```bash
python bot.py
```

## Tech Stack

- **Model:** XLM-RoBERTa-large (HuggingFace Transformers)
- **Bot:** aiogram 3.x
- **Training:** SemEval 2023 Task 3, multi-label classification, BCEWithLogitsLoss
- **Threshold tuning:** per-class thresholds with precision floor

## License

MIT
