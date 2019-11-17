class FBBook:
    def __init__(self, title, texts):
        self.title = title
        self.texts = texts
        self.words = []
        self.parse_words()

    def parse_words(self):
        chars = "!@#$%^&*()[]{};:,./<>\\?\"\'…|`~-=_+—«»"
        words = []
        for p in self.texts:
            if p is not None:
                words.extend(p.translate({ord(c): " " for c in chars}).split())
        self.words = sorted(words, key=lambda word: word.lower())
