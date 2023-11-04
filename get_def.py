# -*- coding: utf-8 -*-

import requests

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

        return cls._correct_translation_order(result, word)

    @classmethod
    def _get_response(cls, word, from_language, to_language):
        res = requests.get(
            url="https://" + from_language.lower() + to_language.lower() + ".dict.cc",
            params={"s": word.encode("utf-8")},
            headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0'}
        )

        return res.content.decode("utf-8")

    @classmethod
    def _parse_response(cls, response_body, word):
        try:
            soup = BeautifulSoup(response_body, "html.parser")

            articles = [x for x in soup.find_all("tr") if x.get("title") == "article sg | article pl"] 
            if articles:  # Got a noun
                article = articles[0]  # ignore 1 noun 2 articles case
                word_with_article = article.find("a", href=f"/?s={word.capitalize()}")
                
                print(f"{word_with_article.text}")
            else:
                word_with_article = None
            # breakpoint()
            english_synonyms = [" ".join([y.text for y in x.find_all("a")]) for x in soup.find_all("td", class_="td7nl") if x.find("a")]
            english_synonyms = [x for x in english_synonyms[:10] if not x.isnumeric() and not x == word]

            if not english_synonyms:
                english_synonyms = "Definitions not found. Check if the spelling is correct."
            else:
                english_synonyms = "- " + "\n- ".join(english_synonyms)
            ctypes.windll.user32.MessageBoxW(0, f"{word_with_article.text if word_with_article else word}\n\n{str(english_synonyms)}", word, 1)
        except Exception as e:
            ctypes.windll.user32.MessageBoxW(0, f"Error when looking up {word}:\n{str(e)}", "Error", 1)


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
    
    dictt = Dict()
    result = dictt.translate(user_input, "de", "en")