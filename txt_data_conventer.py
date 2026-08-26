import csv

def select_data(input_file: str, delimiter: str = None) -> None:
    """
    Преобразует данные, записанные ввиде таблицы с разделителями и переносом строк в csv таблицу
    Args:
        input_file(str): Путь до файла с данными
        delimiter(str): Разделитель
    Returns:
        None
    """
    delimiters = [delimiter] if delimiter != None else ["|", ";", "-", ":"]
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            data = file.read()
            line = []
            word = ""
            with open("output_file.csv", 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_MINIMAL)
                for char in data:
                    if char not in delimiters and char != "\n":
                        word += char
                    elif char in delimiters and char != "\n":
                        line.append(word)
                        word = ''
                    else:
                        line.append(word)
                        word = ""
                        writer.writerow(line)
                        line = []
        return None
    except Exception as e:
        return e
