# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/Summarizer/LICENSE

from abc import ABC, abstractmethod


class SummarizerAlgorithm(ABC):
    name: str
    nlp = None

    def __call__(self, text, limit, unit):
        return self.summarize(text, limit, unit)

    @abstractmethod
    def summarize(self, text, limit, unit):
        pass

    def rows(self, text):
        return text.strip().split('\n')

    def word_tokenizer(self, text):
        return [tok.text for tok in self.nlp.tokenizer(text)]
