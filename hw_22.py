from abc import ABC, abstractmethod
import os
os.system('cls')


# Абстрактный класс для управления ингредиентами
class IngredientFactory(ABC):
    @abstractmethod
    # Метод для создания ингредиента сыра
    def create_cheese(self, cheese: str) -> str:
        pass

    # Метод для создания ингредиента соуса
    @abstractmethod
    def create_sauce(self, sauce: str) -> str:
        pass


# Класс управления ингредиентами для пиццы Dodo
class DodoIngredientFactory(IngredientFactory):
    # Метод для создания ингредиента сыра
    def create_cheese(self, cheese: str) -> str:
        return cheese

    # Метод для создания ингредиента соуса
    def create_sauce(self, sauce: str) -> str:
        return sauce


# Класс для управления размерами пиццы
class SizeFactory:
    def create_size(self, size: str) -> str:
        return size


# Класс для сборки пиццы
class PizzaBuilder:
    def __init__(self, ingredient_factory: IngredientFactory, size_factory: SizeFactory):
        self.ingredient_factory = ingredient_factory
        self.size_factory = size_factory

    # Метод для сборки пиццы
    def build_pizza(self, cheese: str, sauce: str, size: str) -> str:
        self.cheese = cheese
        self.sauce = sauce
        self.size = size
        return f'{self.size} пицца с ингредиентами: {self.cheese} и {self.sauce}.'


# Метод для создания пиццы
def create_pizza():
    ingredient_factory = DodoIngredientFactory()
    size_factory = SizeFactory()
    builder = PizzaBuilder(ingredient_factory, size_factory)
    pizza = builder.build_pizza('Пармезан', 'Кетчуп', 'Большая')
    return pizza


if __name__ == "__main__":
    pizza = create_pizza()
    print(pizza)
