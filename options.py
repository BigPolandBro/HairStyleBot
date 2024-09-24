class Options:
    options_list = []
    option2name = {}
    option2image = {}

    def __init__(self, options_list_, option2name_):
        self.options_list = options_list_
        self.option2name = option2name_
    def option_to_name(self, option):
        return self.option2name.get(option, "Другое")


haircut_translation = {
    "BuzzCut": "[М] Машинкой",
    "UnderCut": "[М] Андеркат",
    "Pompadour": "[М] Помпадур",
    "SlickBack": "[М] Зализанные",
    "CurlyShag": "[М] Кудрявые объемные",
    "WavyShag": "[М] Волнистые объемные",
    "FauxHawk": "[М] Ястреб",
    "Spiky": "[М] Торчащие",
    "CombOver": "[М] Пробор",
    "HighTightFade": "[М] Низкий Фейд",
    "ManBun": "[М] Мужской пучок",
    "Afro": "[М] Афро",
    "LowFade": "[М] Высокий Фейд",
    "UndercutLongHair": "[М] Андеркат + длинные",
    "TwoBlockHaircut": "[М] Двухблочная",
    "TexturedFringe": "[М] Текстурная челка",
    "BluntBowlCut": "[М] Каре",
    "LongWavyCurtainBangs": "[М] Волнистые длинные",
    "MessyTousled": "[М] Взлохмаченный",
    "CornrowBraids": "[М] Французские косички",
    "LongHairTiedUp": "[М] Длинные, собранные",
    "Middle-parted": "[М] Средний пробор",
    "ShortPixieWithShavedSides": "[Ж] Пикси с выбритыми боками",
    "ShortNeatBob": "[Ж] Аккуратное каре",
    "DoubleBun": "[Ж] Двойной пучок",
    "Updo": "[Ж] Высокая укладка",
    "Spiked": "[Ж] Колючий стиль",
    "bowlCut": "[Ж] Прямое каре",
    "Chignon": "[Ж] Шиньон",
    "PixieCut": "[Ж] Пикси",
    "SlickedBack": "[Ж] Зализанные назад",
    "LongCurly": "[Ж] Длинные кудри",
    "CurlyBob": "[Ж] Кудрявое каре",
    "StackedCurlsInShortBob": "[Ж] Кучерявое короткое каре",
    "SidePartCombOverHairstyleWithHighFade": "[Ж] Боковой пробор, высокий фейд",
    "WavyFrenchBobVibesfrom1920": "[Ж] Вайб 1920-х",
    "BobCut": "[Ж] Боб",
    "ShortTwintails": "[Ж] Короткие хвостики",
    "ShortCurlyPixie": "[Ж] Короткое кудрявое пикси",
    "LongStraight": "[Ж] Длинные прямые",
    "LongWavy": "[Ж] Длинные волнистые",
    "FishtailBraid": "[Ж] Косичка рыбий хвост",
    "TwinBraids": "[Ж] Две косички",
    "Ponytail": "[Ж] Хвост",
    "Dreadlocks": "[Ж] Дреды",
    "Cornrows": "[Ж] Корнроуз",
    "ShoulderLengthHair": "[Ж] По плечи",
    "LooseCurlyAfro": "[Ж] Легкое афро",
    "LongTwintails": "[Ж] Длинные хвостики",
    "LongHimeCut": "[Ж] Химэ",
    "BoxBraids": "[Ж] Бокс брейды"
}
haircut_list = [
    "DoubleBun",
    "BuzzCut",
    "LongCurly",
    "UndercutLongHair",
    "WavyFrenchBobVibesfrom1920",
    "SlickedBack",
    "LongWavy",
    "HighTightFade",
    "FishtailBraid",
    "Pompadour",
    "ShoulderLengthHair",
    "SidePartCombOverHairstyleWithHighFade",
    "PixieCut",
    "CombOver",
    "LooseCurlyAfro",
    "TwoBlockHaircut",
    "LongStraight",
    "BobCut",
    "ManBun",
    "StackedCurlsInShortBob",
    "bowlCut",
    "MessyTousled",
    "Spiked",
    "Cornrows",
    "TwinBraids",
    "TexturedFringe",
    "LowFade",
    "BoxBraids",
    "Ponytail",
    "LongTwintails",
    "ShortNeatBob",
    "Spiky",
    "Updo",
    "Chignon",
    "CurlyShag",
    "ShortCurlyPixie",
    "WavyShag",
    "FauxHawk",
    "CornrowBraids",
    "BluntBowlCut",
    "Middle-parted",
    "ShortTwintails",
    "LongHairTiedUp",
    "CurlyBob",
    "Afro",
    "SlickBack",
    "LongWavyCurtainBangs",
    "UnderCut",
    "Dreadlocks",
    "LongHimeCut",
    "ShortPixieWithShavedSides"
]


color_translation = {
    "blonde": "Блонд",
    "platinumBlonde": "Платиновый блонд",
    "brown": "Коричневый",
    "lightBrown": "Светло-коричневый",
    "blue": "Синий",
    "lightBlue": "Голубой",
    "purple": "Фиолетовый",
    "lightPurple": "Светло-фиолетовый",
    "pink": "Розовый",
    "black": "Черный",
    "white": "Белый",
    "grey": "Серый",
    "silver": "Серебристый",
    "red": "Красный",
    "orange": "Оранжевый",
    "green": "Зеленый",
    "gradient": "Градиент",
    "multicolored": "Многоцветный",
    "darkBlue": "Темно-синий",
    "burgundy": "Бордовый",
    "darkGreen": "Темно-зеленый"
}

color_list = [
    "blonde",
    "platinumBlonde",
    "brown",
    "lightBrown",
    "blue",
    "lightBlue",
    "purple",
    "lightPurple",
    "pink",
    "black",
    "white",
    "grey",
    "silver",
    "red",
    "orange",
    "green",
    "gradient",
    "multicolored",
    "darkBlue",
    "burgundy",
    "darkGreen"
]

callback_options = dict()
callback_options["haircut"] = Options(haircut_list, haircut_translation)
callback_options["color"] = Options(color_list, color_translation)
callback_options["purchase"] = Options(["buy"], {"buy": "Купить 10 генераций за 200 рублей"})
callback_options["haircut_view"] = Options(["back", "choose"], {"back": "Назад к выбору", "choose": "Хочу такую"})
#pay_options