
# answer validation system'
def valid_answer(question: str) -> bool:
    answer = input(question + " (s/n): ")
    while not is_valid(answer):
        print("\nATTENZIONE, la risposta inserita non e' valida!\n")
        answer = input(question + " (s/n): ")

    answer = answer.lower()
    return answer == "s"


def is_valid(answer: str) -> bool:
    answer = answer.lower()
    return answer == "s" or answer == "n"


# management of menu choices
def menu(title: str, options: list[str]) -> int:
    choice = 0
    while choice == 0:
        print(title)
        i = 1
        for option in options:
            print(str(i) + ") " + option)
            i = i + 1

        answer = input("\nDigita il numero corrispondente alla scelta: ")
        if not answer.isdigit():
            print("\nATTENZIONE, il valore inserito non e' valido!")
            choice = 0
        else:
            choice = int(answer)
            if (choice < 1) or (choice > len(options)):
                choice = 0
                print("\nATTENZIONE, il valore inserito non e' valido!")

    return choice


# keeping program in pause for user reading
def wait(): input("\nPremi qualsiasi tasto per continuare...")
