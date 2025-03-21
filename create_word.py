from translate import Translator
from unidecode import unidecode
from langchain_openai import ChatOpenAI
import json
llm = ChatOpenAI(model="gpt-4o-mini")

def create_word(mastery, words_list, words_created, lan1, lan2):
    
    # Checking if there are words to be created
    word_index = mastery["list_index"] + 1
    if word_index > len(words_list):
        print("All words have been created.")
        return

    # Creating word list_index + 1    
    word = words_list[mastery["list_index"]][2]
    word_translation = words_list[mastery["list_index"]][3]
    example = create_example(word, word_translation, lan1, lan2)
    example_translation = translate_text(example, lan2)
    synonyms = create_synonyms(word, word_translation, lan1, lan2, lan_to=lan2)

    words_created[str(word_index)] = {"word": word,
                                "translation": word_translation,
                                "translation_decoded": unidecode(word_translation),
                                "synonyms": unidecode(synonyms),
                                "example_lan1": example,
                                "example_lan2": example_translation}
    with open("words_created.json", "w") as file2:
        json.dump(words_created, file2, indent=4, separators=(',', ': '))

    # Updating mastery.json
    mastery[f"list_index"] += 1
    mastery[f"mastery_0"].append(word_index)
    with open("mastery.json", "w") as file3:
        json.dump(mastery, file3, indent=4, separators=(',', ': '))

    print(f"New word created: {word} / {word_translation}\n")


def create_example(word, word_translation, lan1, lan2):
    prompt = f"""Give a short example sentence in {lan1} based on the following word pair: {word}/{word_translation}
                    The short example has to be only in language: {lan1}
                    Only provide the example sentence.
                    The translation is only provided to understand the meaning."""         
    output = llm.invoke(prompt)
    return output.content

def create_synonyms(word, word_translation, lan1, lan2, lan_to):
    prompt = f"""Give 3 synonyms in {lan_to} word pair: {word}/{word_translation}
                Only give the 3 synonyms in this format [synonym1, synonym2, synonym3]
                Only provide the synonyms in this format.
                The translation is only provided to understand the meaning."""
    output = llm.invoke(prompt)
    return output.content

def translate_text(text, lan):
    translator = Translator(to_lang=lan)
    translation = translator.translate(text)
    return translation