class APIKeyManager:
    """
    Класс для управления API-ключами.
    """

    _api_keys = ['s6l0K1wSbI2rSY0ntFlPEsRqbXdB7TXYvyCLxZi4jhMEkgrV6zNHezm9ULGJcn3O',
                 # 'XXjL90yUJYO2RsocHN0pFeS2ZGhNKLKGhq3OeEirWQ146Id5mxMlAnPVCwbEl4Jo',
                 # 'vjSdUng03HfgqVuMrlmJibDFA7KhVRUoeYFPP3qiBzT2wHwzWLZLGackExsYJRlf',
                 # '0coH412v8qKpVoYJBAi59wesW9MdgGYO36Vrx5qRZ2SckUXIaEAsQrChZtxjOEQF',
                 # 'j9AyfiMkbSGWUqHgsqBVG0lY0dytSZ1pzmM6Um5bBe8v7fQLTZNw2CK4CtkJFYhr',
                 # 'wS8cSZKUof6JXHo2eN9U5diMXb2ggC0aYx7bOem7lauImvQDdyzVyxpVRPqT3nBw'
                 ]
    _current_index = 0

    @classmethod
    def get_current_key(cls):
        """
        Возвращает текущий API-ключ.

        :return: Текущий API-ключ.
        """
        return cls._api_keys[cls._current_index]

    @classmethod
    def switch_to_next_key(cls):
        """
        Переключается на следующий API-ключ в списке.
        """
        if cls._current_index >= len(cls._api_keys):
            raise Exception()
        cls._current_index = (cls._current_index + 1)

    @classmethod
    def add_key(cls, new_key):
        """
        Добавляет новый ключ в список API-ключей.

        :param new_key: Новый API-ключ для добавления.
        """
        cls._api_keys.append(new_key)
