class Options:
    options_list = []
    option2name = {}
    option2image = {}

    def __init__(self, options_list_, option2name_):
        self.options_list = options_list_
        self.option2name = option2name_
    def option_to_name(self, option):
        return self.option2name.get(option, "Другое")

haircut_list = [
    "ManBun",
    "Afro",
    "UndercutLongHair",
    "LongWavyCurtainBangs",
    "MessyTousled",
    "LongHairTiedUp",
    "DoubleBun",
    "LongCurly",
    "LongStraight",
    "FishtailBraid",
    "TwinBraids",
    "BoxBraids"
]

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

haircut_translation = {
    "ManBun": "Мужской пучок",
    "Afro": "Афро",
    "UndercutLongHair": "Андеркат+длинные",
    "LongWavyCurtainBangs": "Волнистые челки",
    "MessyTousled": "Небрежные",
    "LongHairTiedUp": "Собранные",
    "DoubleBun": "Двойной пучок",
    "LongCurly": "Длинные кудри",
    "LongStraight": "Длинные прямые",
    "FishtailBraid": "Рыбий хвост",
    "TwinBraids": "Две косы",
    "BoxBraids": "Бокс-брейдс"
}


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

callback_options = dict()
callback_options["haircut"] = Options(haircut_list, haircut_translation)
callback_options["color"] = Options(color_list, color_translation)
callback_options["purchase"] = Options(["buy"], {"buy": "Купить 10 генераций за 200 рублей"})
callback_options["haircut_view"] = Options(["back", "choose"], {"back": "Назад к выбору", "choose": "Хочу такую"})
#pay_options