palindrome = input("Введите слово: ")
if palindrome.upper() == palindrome[::-1].upper():
    print(f"Введеное слово '{palindrome}' является палиндромом.")
else:
    print(f"Введеное слово '{palindrome}' не является палиндромом!")
