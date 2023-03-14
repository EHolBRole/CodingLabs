import datetime as dt
import statistics
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    count = 0
    summ = 0
    friends = get_friends(user_id).items
    curr_year = dt.datetime.now().year
    for i in friends:
        try:
            summ += int(curr_year - int(i["bdate"][5:]))  # type: ignore
            count += 1
        except:
            pass
    if count > 0:
        return summ / count
    return None
