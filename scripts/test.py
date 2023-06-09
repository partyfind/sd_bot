text = input("Введите текст для проверки: ")

if any(char.isalpha() for char in text):
    print(0)
elif any(char.isdigit() or char == '-' for char in text):
    print(1)
else:
    print("Ошибка: в тексте отсутствуют цифры и знак '-'.")