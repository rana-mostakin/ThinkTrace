# Author: rana-mostakin
"""
ThinkTrace v1 — Languages Data
50+ languages with native name + English name
"""

LANGUAGES: list[dict] = [
    {"native": "English",      "english": "English",       "code": "en"},
    {"native": "বাংলা",         "english": "Bengali",       "code": "bn"},
    {"native": "العربية",       "english": "Arabic",        "code": "ar"},
    {"native": "हिन्दी",         "english": "Hindi",         "code": "hi"},
    {"native": "Español",       "english": "Spanish",       "code": "es"},
    {"native": "Français",      "english": "French",        "code": "fr"},
    {"native": "普通话",          "english": "Mandarin",      "code": "zh"},
    {"native": "Português",     "english": "Portuguese",    "code": "pt"},
    {"native": "Русский",       "english": "Russian",       "code": "ru"},
    {"native": "Türkçe",        "english": "Turkish",       "code": "tr"},
    {"native": "日本語",          "english": "Japanese",      "code": "ja"},
    {"native": "한국어",          "english": "Korean",        "code": "ko"},
    {"native": "Deutsch",       "english": "German",        "code": "de"},
    {"native": "اردو",           "english": "Urdu",          "code": "ur"},
    {"native": "Bahasa Indonesia","english": "Indonesian",   "code": "id"},
    {"native": "Kiswahili",     "english": "Swahili",       "code": "sw"},
    {"native": "فارسی",          "english": "Persian",       "code": "fa"},
    {"native": "ภาษาไทย",        "english": "Thai",          "code": "th"},
    {"native": "Tiếng Việt",    "english": "Vietnamese",    "code": "vi"},
    {"native": "Italiano",      "english": "Italian",       "code": "it"},
    {"native": "Nederlands",    "english": "Dutch",         "code": "nl"},
    {"native": "Polski",        "english": "Polish",        "code": "pl"},
    {"native": "Bahasa Melayu", "english": "Malay",         "code": "ms"},
    {"native": "தமிழ்",          "english": "Tamil",         "code": "ta"},
    {"native": "తెలుగు",         "english": "Telugu",        "code": "te"},
    {"native": "मराठी",          "english": "Marathi",       "code": "mr"},
    {"native": "ગુજરાતી",        "english": "Gujarati",      "code": "gu"},
    {"native": "ਪੰਜਾਬੀ",         "english": "Punjabi",       "code": "pa"},
    {"native": "አማርኛ",          "english": "Amharic",       "code": "am"},
    {"native": "Soomaali",      "english": "Somali",        "code": "so"},
    {"native": "Hausa",         "english": "Hausa",         "code": "ha"},
    {"native": "Yorùbá",        "english": "Yoruba",        "code": "yo"},
    {"native": "isiZulu",       "english": "Zulu",          "code": "zu"},
    {"native": "Română",        "english": "Romanian",      "code": "ro"},
    {"native": "Ελληνικά",      "english": "Greek",         "code": "el"},
    {"native": "Čeština",       "english": "Czech",         "code": "cs"},
    {"native": "Svenska",       "english": "Swedish",       "code": "sv"},
    {"native": "Norsk",         "english": "Norwegian",     "code": "no"},
    {"native": "Українська",    "english": "Ukrainian",     "code": "uk"},
    {"native": "עברית",          "english": "Hebrew",        "code": "he"},
    {"native": "Magyar",        "english": "Hungarian",     "code": "hu"},
    {"native": "Dansk",         "english": "Danish",        "code": "da"},
    {"native": "Suomi",         "english": "Finnish",       "code": "fi"},
    {"native": "ქართული",       "english": "Georgian",      "code": "ka"},
    {"native": "Azərbaycan",    "english": "Azerbaijani",   "code": "az"},
    {"native": "O'zbek",        "english": "Uzbek",         "code": "uz"},
    {"native": "Қазақша",       "english": "Kazakh",        "code": "kk"},
    {"native": "မြန်မာ",          "english": "Burmese",       "code": "my"},
    {"native": "ខ្មែរ",           "english": "Khmer",         "code": "km"},
    {"native": "සිංහල",          "english": "Sinhala",       "code": "si"},
    {"native": "नेपाली",          "english": "Nepali",        "code": "ne"},
]

DEFAULT_LANGUAGE = "English"


def get_language_names() -> list[str]:
    return [lang["english"] for lang in LANGUAGES]


def get_language_by_english(name: str) -> dict:
    for lang in LANGUAGES:
        if lang["english"] == name:
            return lang
    return {"native": name, "english": name, "code": "en"}
