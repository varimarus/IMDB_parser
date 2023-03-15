class OtherFunc:
    @classmethod
    def convert_time(cls, time):
        """
        Функция конвертации времени
        :param time: Время в минутах
        :return: Время по формату вывода
        """
        sec = time * 60
        hour = sec // 3600
        sec %= 3600
        min = sec // 60
        sec %= 60
        return "%02d:%02d:%02d" % (hour, min, sec)
