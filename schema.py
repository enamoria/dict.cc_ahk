from pprint import pprint
from bs4.element import Tag

class Word:
    def __init__(self, word_id, word, pronunciation, link, article=None):
        self.word_id = word_id
        self.word = word.text if isinstance(word, Tag) else word
        self.pronunciation = pronunciation.text if isinstance(pronunciation, Tag) else pronunciation
        self.link = link
        self.article = article.text if isinstance(article, Tag) else article

    def __repr__(self):
        return f"Word: {self.word}" if self.article is None else f"Word: {self.article} {self.word.capitalize()}"
    
    def __str__(self) -> str:
        return f"Word: {self.word}" if self.article is None else f"Word: {self.article} {self.word.capitalize()}"
    

class Definition:
    def __init__(self, word_id, definition_id, definition, example, pos):
        self.word_id = word_id
        self.definition_id = definition_id
        self.definition = definition.text if isinstance(definition, Tag) else definition

        if example is not None:
            self.example = example.text if isinstance(example, Tag) else example
        else:
            self.example = "NA"
        self.pos = pos

    def __repr__(self) -> str:
        return f"{self.definition}: {self.example}"

    def __str__(self) -> str:
        example_str = "\n- " + self.example.strip().replace("\n", "\n- ")
        return f"Definition: {self.definition}: \n \nExample: {example_str}"
    

class Payload(dict):
    def __init__(self, word, definition):
        parent = {"database_id": None, "type": "database_id"}
        properties = {
            "Vocab": {
                "id": "title",
                "type": "title",
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": word.word if word.article is None else f"{word.article} {word.word.capitalize()}",
                        },
                        "annotations": {
                            "bold": True,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default"
                        },
                        "plain_text": word.word,
                    }
                ]
            },
            "Example Sentence": {
                "type": "rich_text", 
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": definition.example.split("\n")[0],
                    },
                    "plain_text": definition.example.split("\n")[0],
                }]
            },
            "Part of Speech": {
                "type": "multi_select",
                "multi_select": [
                    {
                        "name": definition.pos if definition.pos else "Unknown",
                    }
                ] 
            },
            "Similar Words": {
                "id": "ezpD",
                "type": "rich_text",
                "rich_text": []
            },
            "Definition": {
                "type": "rich_text",
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": definition.definition,
                        },
                        "plain_text": definition.definition,
                    }
                ]
            },
            "Link": {
                "type": "rich_text",
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": word.link,
                            "link": {
                                "url": word.link,
                            },
                        },
                        "plain_text": word.link,
                    }
                ]
            },
        }
        # children: the rendered content of the page
        children = [
            # Pronunciation
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{ "type": "text", "text": { "content": "Pronunciation" } }]
                }
            },
            {
                "object": "block",
                "type": "embed",
                "embed": {
                    "url": word.pronunciation,
                }
            } if word.pronunciation else {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{
                        "type": "text",
                        "text": {
							"content": "NA",
							"link": None
						}
                    }]
                }
            },

            # definition, example Sentence
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{ "type": "text", "text": { "content": "Definition 1" } }]
                }
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{ "type": "text", "text": { "content": "Definition" } }]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{
                        "type": "text",
                        "text": {
							"content": "- " + definition.definition,
							"link": None #{ "url": "https://en.wikipedia.org/wiki/Lacinato_kale" }
						}
                        # "plain_text": definition.example,
                        # "href": None
                    }]
                }
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{ "type": "text", "text": { "content": "Example" } }]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{
                        "type": "text",
                        "text": {
							"content": "- " + definition.example.replace("\n", "\n- "),
							"link": None #{ "url": "https://en.wikipedia.org/wiki/Lacinato_kale" }
						}
                        # "plain_text": definition.example,
                        # "href": None
                    }]
                }
            },
        ]

        self["parent"] = parent
        self["properties"] = properties
        self["children"] = children
        self.curr_num_definition = (len(self["children"]) - 2) // 5

    def append_definition_chilren(self, definition):
        self.curr_num_definition += 1
        if len(self["children"]) + 5 > 100:
            return

        self["children"].extend([
            # definition, example Sentence
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{ "type": "text", "text": { "content": f"Definition {self.curr_num_definition}" } }]
                }
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{ "type": "text", "text": { "content": "Definition" } }]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{
                        "type": "text",
                        "text": {
							"content": "- " + definition.definition,
							"link": None #{ "url": "https://en.wikipedia.org/wiki/Lacinato_kale" }
						}
                        # "plain_text": definition.example,
                        # "href": None
                    }]
                }
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{ "type": "text", "text": { "content": "Example" } }]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{
                        "type": "text",
                        "text": {
							"content": "- " + definition.example.replace("\n", "\n- "),
							"link": None #{ "url": "https://en.wikipedia.org/wiki/Lacinato_kale" }
						}
                        # "plain_text": definition.example,
                        # "href": None
                    }]
                }
            },
        ])
