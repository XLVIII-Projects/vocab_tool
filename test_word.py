import json

def test_word(word_to_test, mastery, mastery_level, words_created, lan1, lan2):
    # print(f"Debug - Attempting to test word_to_test: {word_to_test} (type: {type(word_to_test)})")
    # print(f"Debug - Available keys in words_created: {list(words_created.keys())}")

    word_to_test = str(word_to_test)

    # print(f"Debug - After conversion word_to_test: {word_to_test} (type: {type(word_to_test)})")
    
    word = words_created[word_to_test]['word']
    translation = words_created[word_to_test]['translation']
    translation_decoded = words_created[word_to_test]['translation_decoded']
    synonyms = words_created[word_to_test]['synonyms']
    example_sentence_lan1 = words_created[word_to_test]['example_lan1']
    example_sentence_lan1_marked = words_created[word_to_test]['example_lan1'].replace(words_created[word_to_test]['word'], f"'{word}'")
    example_sentence_lan2 = words_created[word_to_test]['example_lan2']
    example_sentence_lan2_hidden = words_created[word_to_test]['example_lan2'].replace(words_created[word_to_test]['translation'], '______')
    
    print("------------------------------------\n")
    print(f"Example sentence: {example_sentence_lan1_marked}")
    print(f"Example translation: {example_sentence_lan2_hidden}")
    print("\n")

    answer = input(f"What is the translation of '{word}' in {lan2}? \n")
    if answer == "":
        incorrect_answer(mastery, mastery_level, word_to_test)
    if answer == translation_decoded or answer in synonyms:
        correct_answer(word, translation, example_sentence_lan2, word_to_test, mastery, mastery_level)
    else:
        incorrect_answer(mastery, mastery_level, word_to_test, translation)
        
def correct_answer(word, translation, example_sentence_lan2, word_to_test, mastery, mastery_level):
    print(f"\nCorrect! {word}: {translation}.\n")
    if mastery_level == 5:
        return
    else:
        mastery[f"mastery_{mastery_level}"].remove(int(word_to_test))
        mastery[f"mastery_{mastery_level + 1}"].append(int(word_to_test))
        with open("mastery.json", "w") as file3:
            json.dump(mastery, file3, indent=4, separators=(',', ': '))
        
def incorrect_answer(mastery, mastery_level, word_to_test, translation):
    print(f"Incorrect. The correct translation is {translation}.\n")
    if mastery_level == 0 or mastery_level == 5:
        return
    else:    
        mastery[f"mastery_{mastery_level}"].remove(int(word_to_test))
        mastery[f"mastery_{mastery_level - 1}"].append(int(word_to_test))
        with open("mastery.json", "w") as file3:
            json.dump(mastery, file3, indent=4, separators=(',', ': '))