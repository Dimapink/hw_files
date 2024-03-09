import os


def parse_data_from_book(filename):
    recipes = []
    with open(f"{filename}", "r", encoding="UTF-8") as cookbook:
        book_data = []
        for line in cookbook:
            if line == "\n":
                recipes.append(book_data)
                book_data = []
            else:
                book_data.append(line.rstrip("\n"))
    return recipes


def create_dict(data: list[list[str]]):
    parsed_dict = {}
    for dish in data:
        for i in dish:
            if "|" in i:
                parsed_dict.setdefault(dish[0], []).append(parse_ingredient(i))
    return parsed_dict


def parse_ingredient(ingredient):
    ingredient = list(map(lambda x: x.rstrip(), ingredient.split("|")))
    return {'ingredient_name': ingredient[0], 'quantity': int(ingredient[1]), 'measure': ingredient[2][1:]}


book = create_dict(parse_data_from_book("recipes.txt"))
print(book)


def get_shop_list_by_dishes(dishes: list[str], person_count) -> dict:
    """
    Функция формирования списка покупок
    :param dishes: Список блюд для формирования списка покупок, если в списке есть блюдо,
    которого нет в кулинарной книге, то оно не учитывается, если в списке нет ни одного блюда из книги, будет ValueError
    :param person_count: количество персон для формирования списка
    :return: Словарь - список покупок
    """
    if all(map(lambda x: x not in book.keys(), dishes)):
        raise ValueError("Не нашли ни одного блюда из книги")
    else:
        shop_list = {}
        for dish in dishes:
            dish = book.get(dish)
            if dish:
                for ing in dish:
                    ingredient = ing.get("ingredient_name")
                    ing_quantity = ing.get("quantity")
                    ing_mes = ing.get("measure")
                    shop_list.setdefault(ingredient, {}).update({"measure": ing_mes,
                                                                 "quantity": ing_quantity * person_count})
    return shop_list


print("-" * 100)
print(get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2))


def get_files():
    files = os.listdir("sorted")
    return files


def parse_file_data(files: list):
    payload = []
    for file in files:
        with open(f"sorted/{file}", "r") as file:
            lines = list(map(lambda x: x.rstrip(), file.readlines()))
        payload.append((file.name.split("/")[-1], len(lines), lines))
    return sorted(payload, key=lambda x: x[1])


data = parse_file_data(get_files())
# print(data)
with open("solution.txt", "w", encoding="utf-8") as solution:
    for i in data:
        solution.write(i[0] + "\n")
        solution.write(str(i[1]) + "\n")
        solution.writelines(i[2])
        solution.write("\n")