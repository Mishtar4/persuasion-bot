# ============ UI STRINGS ============
STRINGS = {
    "pl": {
        "start":        "Cześć! Wyślij mi tekst, a wykryję w nim techniki perswazji akapit po akapicie.\n\nOddziel akapity pustą linią.\n\nKomendy:\n/example — przykład działania bota\n/techniques — lista wszystkich technik\n/model — informacja dotycząca modelu\n/language — zmień język\n\n💡 Nie wiesz, jak to działa? Napisz /example, aby zobaczyć przykład.",
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
        "example_intro": (
            "📌 Przykład działania bota\n\n"
            "Wyślij tekst podzielony na akapity — każdy akapit oddziel pustą linią "
            "(wciśnij Enter dwa razy). Bot analizuje każdy akapit osobno.\n\n"
            "Przykładowy tekst:"
        ),
        "example_result_intro": "Wynik analizy:",
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
        "start":        "Привіт! Надішли мені текст, і я знайду в ньому техніки переконання абзац за абзацом.\n\nРозділяй абзаци порожнім рядком.\n\nКоманди:\n/example — приклад роботи бота\n/techniques — список усіх технік\n/model — інформація про модель\n/language — змінити мову\n\n💡 Не знаєш, як це працює? Напиши /example, щоб побачити приклад.",
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
        "example_intro": (
            "📌 Приклад роботи бота\n\n"
            "Надішли текст, поділений на абзаци — кожен абзац відділяй порожнім рядком "
            "(натисни Enter двічі). Бот аналізує кожен абзац окремо.\n\n"
            "Приклад тексту:"
        ),
        "example_result_intro": "Результат аналізу:",
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
        "Appeal_to_Authority":              'odwołanie się do opinii znanej lub uznanej osoby/instytucji jako poparcia dla twierdzenia',
        "Appeal_to_Popularity":             'wzmocnienie twierdzenia informacją, że tak myśli lub robi wiele osób',
        "Appeal_to_Values":                 'odwołanie do wartości (patriotyzm, rodzina, tradycja) jako argumentu, obok lub zamiast faktów',
        "Appeal_to_Fear-Prejudice":         'odwołanie się do strachu, obaw lub uprzedzeń odbiorcy jako wsparcia dla przekazu',
        "Flag_Waving":                      'odwołanie do dumy narodowej lub grupowej, podział na „my" i „oni"',
        "Causal_Oversimplification":        'przypisanie złożonego problemu jednej przyczynie, choć w rzeczywistości może mieć ich więcej',
        "False_Dilemma-No_Choice":          'przedstawienie sytuacji jako wyboru tylko między dwiema opcjami, choć możliwości może być więcej',
        "Consequential_Oversimplification": 'założenie, że jedno zdarzenie nieuchronnie doprowadzi do łańcucha kolejnych konsekwencji',
        "Straw_Man":                        'przedstawienie czyjegoś stanowiska w uproszczonej lub wyolbrzymionej formie przed jego skrytykowaniem',
        "Red_Herring":                      'wprowadzenie do rozmowy tematu, który odwraca uwagę od głównego zagadnienia',
        "Whataboutism":                     'odpowiedź na krytykę poprzez wskazanie podobnego zachowania u innej strony',
        "Slogans":                          'krótkie, łatwe do zapamiętania zdanie, które przekazuje główną myśl bez rozwiniętej argumentacji',
        "Appeal_to_Time":                   'podkreślenie ograniczonego czasu na podjęcie decyzji lub działania',
        "Conversation_Killer":              'zdanie mające na celu zakończenie dyskusji na dany temat, np. „to nie podlega dyskusji"',
        "Loaded_Language":                  'użycie słów o silnym zabarwieniu emocjonalnym, które wzmacniają wydźwięk przekazu',
        "Repetition":                       'wielokrotne powtórzenie tego samego komunikatu',
        "Exaggeration-Minimisation":        'przedstawienie czegoś jako większego/ważniejszego albo mniejszego/mniej istotnego, niż wynika to z faktów',
        "Obfuscation-Vagueness-Confusion":  'użycie niejasnego, złożonego języka, który utrudnia jednoznaczne zrozumienie przekazu',
        "Name_Calling-Labeling":            'użycie etykiety lub określenia wobec osoby albo grupy zamiast odniesienia się do jej argumentów',
        "Doubt":                            'wyrażenie wątpliwości co do wiarygodności lub kompetencji osoby albo źródła',
        "Guilt_by_Association":             'powiązanie osoby lub idei z inną osobą bądź grupą w celu wpłynięcia na jej odbiór',
        "Appeal_to_Hypocrisy":              'wskazanie, że druga strona sama postępuje w sposób, który krytykuje',
        "Questioning_the_Reputation":       'komentarz odnoszący się do reputacji lub charakteru osoby, a nie do treści jej argumentów',
    },
    "uk": {
        "Appeal_to_Authority":              'посилання на думку відомої або авторитетної особи/інституції як на підтвердження твердження',
        "Appeal_to_Popularity":             'підсилення твердження інформацією про те, що так думає або робить багато людей',
        "Appeal_to_Values":                 'апеляція до цінностей (патріотизм, сім\'я, традиція) як аргумент, поряд із фактами або замість них',
        "Appeal_to_Fear-Prejudice":         'звернення до страхів, побоювань або упереджень аудиторії як підтримки повідомлення',
        "Flag_Waving":                      'апеляція до національної чи групової гордості, поділ на «ми» та «вони»',
        "Causal_Oversimplification":        'складній проблемі приписується одна причина, хоча насправді причин може бути декілька',
        "False_Dilemma-No_Choice":          'ситуація подається як вибір лише між двома варіантами, хоча насправді варіантів може бути більше',
        "Consequential_Oversimplification": 'припущення, що одна подія неминуче призведе до ланцюга подальших наслідків',
        "Straw_Man":                        'переформулювання чужої позиції у спрощеному або перебільшеному вигляді перед її критикою',
        "Red_Herring":                      'введення в розмову теми, яка відволікає увагу від основного питання',
        "Whataboutism":                     'відповідь на критику через вказівку на подібну поведінку іншої сторони',
        "Slogans":                          'короткий, легкий для запам\'ятовування вислів, що передає основну думку без розгорнутої аргументації',
        "Appeal_to_Time":                   'наголос на обмеженості часу для прийняття рішення чи дії',
        "Conversation_Killer":              'фраза, що покликана завершити обговорення теми, наприклад «це не підлягає обговоренню»',
        "Loaded_Language":                  'використання слів із сильним емоційним забарвленням, які підсилюють враження від повідомлення',
        "Repetition":                       'багаторазове повторення одного й того ж повідомлення',
        "Exaggeration-Minimisation":        'представлення чогось як більшого/важливішого або меншого/менш суттєвого, ніж випливає з фактів',
        "Obfuscation-Vagueness-Confusion":  'використання нечіткого, заплутаного формулювання, яке ускладнює однозначне розуміння повідомлення',
        "Name_Calling-Labeling":            'використання ярлика чи означення щодо особи або групи замість звернення до її аргументів',
        "Doubt":                            'висловлення сумніву щодо достовірності чи компетентності особи або джерела',
        "Guilt_by_Association":             'пов\'язування особи чи ідеї з іншою особою або групою з метою впливу на її сприйняття',
        "Appeal_to_Hypocrisy":              'вказівка на те, що інша сторона сама діє так, як критикує',
        "Questioning_the_Reputation":       'коментар стосується репутації чи характеру особи, а не суті її аргументів',
    },
}

# ============ /example SAMPLE TEXT ============
EXAMPLES = {
    "pl": (
        "Wszyscy eksperci są przekupieni i mówią tylko to, co im się kazano powiedzieć - "
        "prawdziwa prawda jest zupełnie inna.\n\n"
        "Jeśli teraz nie podejmiesz działania, stracisz wszystko, na czym ci zależy - "
        "czas niemal się skończył."
    ),
    "uk": (
        "Усі експерти продажні й кажуть лише те, що їм наказали - "
        "справжня правда зовсім інша.\n\n"
        "Якщо ти не діятимеш зараз, втратиш усе, що тобі дороге - "
        "часу майже не залишилося."
    ),
}
