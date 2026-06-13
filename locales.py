# ============ UI STRINGS ============
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
            "Klas: 23 techniki\n"
            "GitHub: https://github.com/Mishtar4/persuasion-bot\n"
            "Model: https://huggingface.co/Mishtar4/persuasion-detector-xlm-roberta"
        ),
    },
    "uk": {
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
            "Класів: 23 техніки\n"
            "GitHub: https://github.com/Mishtar4/persuasion-bot\n"
            "Модель: https://huggingface.co/Mishtar4/persuasion-detector-xlm-roberta"
        ),
    },
}

# ============ TECHNIQUE DESCRIPTIONS ============
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
    "uk": {
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
