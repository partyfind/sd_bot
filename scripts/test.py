text = input("Введите текст для проверки: ")
def match_value(text):
    if '-' in text:
        tokens = text.split('-')
        if all(token.isdigit() for token in tokens):
            return "digit"
    if text.isdigit():
      return "digit"
    if text.replace('.', '').replace(',', '').isdigit():
      return "digit"
print(match_value('22'))
print(match_value('22-22'))
print(match_value('22-22 23'))
print(match_value('aa dd'))
print(match_value('aa-dd'))
print(match_value('aa2dd'))
print(match_value('aa2dd 3e'))
print(match_value('d-d'))