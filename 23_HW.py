import os
os.system('cls')


# Стратегия проверки палиндрома
class PalindromeStrategy:
    def isPalindrome(self, word: str) -> bool:
        raise NotImplementedError


# Класс стратегии поиска палиндрома по одному слову
class SingleWordPolindrome(PalindromeStrategy):
    def __init__(self, word):
        self.word = word

    # Проверка является ли слово палиндромом, если да возвращает True
    def isPalindrome(self, word: str) -> bool:
        if self.word == self.word[::-1]:
            return True
        else:
            return False


# Класс стратегии поиска палиндрома по нескольким словам
class MultiWordPolindrome(PalindromeStrategy):
    def __init__(self, word):
        self.word = word

    # Проверка является ли строка палиндромом (предварительно удалив пробелы), если да возвращает True
    def isPalindrome(self, word: str) -> bool:
        word_ = self.word.replace(' ', '')
        if word_ == word_[::-1]:
            return True
        else:
            return False


# Класс контекст поиска палиндрома
class PolindromeContext:
    def __init__(self):
        self.strategy = None

    # Установка стратегии
    def set_strategy(self, strategy: PalindromeStrategy):
        self.strategy = strategy

    # Проверка является ли строка палиндромом
    def check(self, word: str) -> bool:
        if self.strategy:
            return self.strategy.isPalindrome(word)
        else:
            return False


# Класс фасада
class PalindromeFacade:
    def __init__(self):
        self.context = PolindromeContext()

    # Проверка является ли строка палиндромом
    def check_polindrome(self, word: str):
        if " " in word:
            self.context.set_strategy(MultiWordPolindrome(word))
        else:
            self.context.set_strategy(SingleWordPolindrome(word))
        return self.context.check(word)


# Основная функция
def main():
    facade = PalindromeFacade()
    user_input = input("Введите строку для проверки палиндрома: ")
    result = facade.check_polindrome(user_input)
    if result:
        print(f"Ваша строка '{user_input.upper()}' является палиндромом")
    else:
        print(F"Ваша строка '{user_input.upper()}' не является палиндромом")


if __name__ == "__main__":
    main()
