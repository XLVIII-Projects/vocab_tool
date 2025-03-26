from translate import Translator
from unidecode import unidecode
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import json
import csv

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini")

class Creator:
    def __init__(self):
        self.lan1 = "en"
        self.lan2 = "esp"

    # def file_words_list(self):
    #     with open("words_list_exp.csv", "r") as file1:
    #         words_list = list(csv.reader(file1))
    #     return words_list

    # def file_mastery(self):
    #     with open("mastery.json", "r") as file3:
    #         mastery = json.load(file3)
    #     return mastery

    # def file_words_created(self):
    #     with open("words_created.json", "r") as file2:
    #         words_created = json.load(file2)
    #     return words_created
        
    def create_word(self, mastery, words_list, words_created):
        # Checking if there are words to be created
        word_index = mastery["list_index"] + 1
        if word_index > len(words_list):
            print("All words have been created.")
            return

        # Creating word list_index + 1    
        word = words_list[mastery["list_index"]][2]
        word_translation = words_list[mastery["list_index"]][3]
        example = self.create_example(word, word_translation, self.lan1)
        example_translation = self.translate_text(example, self.lan2)
        synonyms = self.create_synonyms(word, word_translation, lan_to=self.lan2)

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


    def create_example(self, word, word_translation, lan1):
        prompt = f"""Give a short example sentence in {lan1} based on the following word pair: {word}/{word_translation}
                        The short example has to be only in language: {lan1}
                        Only provide the example sentence.
                        The translation is only provided to understand the meaning."""         
        output = llm.invoke(prompt)
        return output.content

    def create_synonyms(self, word, word_translation, lan_to):
        prompt = f"""Give 3 synonyms in {lan_to} word pair: {word}/{word_translation}
                    Only give the 3 synonyms in this format [synonym1, synonym2, synonym3]
                    Only provide the synonyms in this format.
                    The translation is only provided to understand the meaning."""
        output = llm.invoke(prompt)
        return output.content

    def translate_text(self, text, lan):
        translator = Translator(to_lang=lan)
        translation = translator.translate(text)
        return translation