# -*- coding: utf-8 -*-

import requests
from schema import Word, Definition, Payload
from post_to_notion import postDatabase

try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup
    BeautifulSoup.find_all = BeautifulSoup.findAll
    
import ctypes  # An included library with Python install.   
import tkinter as tk
from tkinter import simpledialog


class Dict(object):
    @classmethod
    def translate(cls, word, from_language, to_language):
        response_body = cls._get_response(word, from_language, to_language)
        result = cls._parse_response(response_body, word)

        # return cls._correct_translation_order(result, word)

    @classmethod
    def _get_response(cls, word, from_language, to_language):
        res = requests.get(
            # url="https://" + from_language.lower() + to_language.lower() + ".dict.cc",
            url = "https://www.duden.de/rechtschreibung/" + word,
            params={"s": word.encode("utf-8")},
            headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0'}
        )

        return res.content.decode("utf-8")

    @classmethod
    def _parse_response(cls, response_body, word):
        # try:
            soup = BeautifulSoup(response_body, "html.parser")
            # breakpoint()

            # article
            articles = soup.find_all("span", class_="lemma__determiner")
            if articles:  # Got a noun
                article = articles[0].text  # ignore 1 noun 2 articles case
            else:
                article = None

            # word
            word = soup.find("span", class_="lemma__main")
            url = "https://www.duden.de/rechtschreibung/" + word.text

            # pronunciation
            pronunciation_mp3 = soup.find("a", class_="pronunciation-guide__sound")
            if pronunciation_mp3:
                pronunciation_mp3 = pronunciation_mp3.get("href")

            # definition
            Bedeutungen = soup.find("div", id="bedeutungen").find_all("li", class_="enumeration__item")
            # print(Bedeutungen)

            payload = None
            word_obj = Word(word_id="100", word=word, pronunciation=pronunciation_mp3, link=url, article=article)

            for bedeutung in Bedeutungen:
                if bedeutung.get("id") is None:  # there are multiple sections for this definition. The bedeutung id will be specifies later in subsection

                    sub_bedeutungen = bedeutung.find_all("li", class_="enumeration__sub-item")

                    for sub_bedeutung in sub_bedeutungen:
                        sub_definition = sub_bedeutung.find("div", class_="enumeration__text")

                        sub_examples_container = sub_bedeutung.find_all("dl", class_="note")
                        sub_examples = [container.find("ul", class_="note__list") for container in sub_examples_container if container.find("dt", class_="note__title").text == "Beispiele"]

                        if sub_examples: 
                            sub_examples = sub_examples[0]
                        else:
                            sub_examples = None

                        definition = Definition(word_id="100", definition_id="1000", definition=sub_definition, example=sub_examples, pos="Noun" if article else None)

                        if payload:
                            payload.append_definition_chilren(definition)
                            # pass
                        else:
                            payload = Payload(word_obj, definition)

                        # print(definition)
                        ctypes.windll.user32.MessageBoxW(0, f"{word_obj}\n\n{str(definition)}", word, 1)
                        # break
                    # postDatabase(payload=payload)
                    
                else: # there is only 1 section for this definition
                    # breakpoint()

                    sub_bedeutung = bedeutung
                    sub_definition = sub_bedeutung.find("div", class_="enumeration__text")

                    sub_examples_container = sub_bedeutung.find_all("dl", class_="note")
                    sub_examples = [container.find("ul", class_="note__list") for container in sub_examples_container if container.find("dt", class_="note__title").text == "Beispiele"]

                    if sub_examples:
                        sub_examples = sub_examples[0]
                        definition = Definition(word_id="100", definition_id="1000", definition=sub_definition, example=sub_examples, pos="Noun" if article else None)
                    else:
                        definition = Definition(word_id="100", definition_id="1000", definition=sub_definition, example=None, pos="Noun" if article else None)

                    if payload:
                        payload.append_definition_chilren(definition)
                        # pass
                    else:
                        payload = Payload(word_obj, definition)

                    # print(definition)
                    # postDatabase(payload=Payload(word_obj, definition))
                    ctypes.windll.user32.MessageBoxW(0, f"{word_obj}\n\n{str(definition)}", word, 1)
                # break
                # print(bedeutung.text)
            postDatabase(payload=payload)
        # except Exception as e:
        #     ctypes.windll.user32.MessageBoxW(0, f"Error when looking up {word}:\n{str(e)}", "Error", 1)


if __name__ == "__main__":
    
    root = tk.Tk()
    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
    root.geometry("+{}+{}".format(positionRight, positionDown))  # Root does not move yet
    root.overrideredirect(1)
    root.withdraw()
    root.update_idletasks()  # Run "mainloop" one time.  Changes root location.  Do before making dialog
 
    user_input = simpledialog.askstring(title="Input", prompt="Enter the word:", parent=root)
    user_input = user_input.strip().replace("ü", "ue").replace("ö", "oe").replace("ä", "ae").replace("ß", "ss")
    # user_input = "Haus"
    dictt = Dict()
    result = dictt.translate(user_input, "de", "en")