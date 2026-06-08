# test_grammar.py — interactive interface for testing the parser

from grammar import parse_sentence

print("────────────────────────────────────")
print(" Indonesian Grammar Parser")
print(" Type a sentence or 'exit'")
print("────────────────────────────────────")

while True:
    user_input = input("\nEnter sentence: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    trees = parse_sentence(user_input)

    if trees:
        print("\n ACCEPTED\n")
        print("Parse tree:\n")

        # print first tree only - grammar is unambiguous so one tree is enough
        trees[0].pretty_print()

    else:
        print("\n REJECTED")
