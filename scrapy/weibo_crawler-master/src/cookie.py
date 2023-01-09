class CookiePool(object):

    def __init__(self, cookie_list: list) -> None:
        self.__good_list = cookie_list
        self.__last_cookie = None

    def get_cookie(self) -> dict:
        self.__last_cookie = self.__good_list.pop()
        # self.__good_list.insert(0, self.__last_cookie)
        return self.__last_cookie

    def have_cookie(self) -> bool:
        return True if self.__good_list else False
