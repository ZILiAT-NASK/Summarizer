# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/Summarizer/LICENSE

import morfeusz2
import spacy

from .frequent_lemmas_summarizer import FrequentLemmasSummarizer
from .transformers_summarizer import TransformersSummarizer
from .cohesion_sumamrizer import CohesionSummarizer
from .preprocessing import preprocess
from .libs.common import get_logger


class Summarizer:
    event_messages = {
        0: None,
        1: "Limit wyrazów jest zbyt wysoki. Utworzono podsumowanie zawierające {} wyrazów.",
        2: "Limit wyrazów jest zbyt niski. Utworzono podsumowanie zawierające {} wyrazów.",
        10: "Nie udało się przetworzyć tekstu.",
        11: "Przesłano zbyt krótki tekst.",
        12: "Limit liczby wyrazów jest zbyt wysoki. Nie udało się stworzyć podsumowania.",
        13: "Limit liczby wyrazów jest zbyt niski. Nie udało się stworzyć podsumowania.",
    }

    def __init__(self, preprocess=True, min_words=30, nlp_model=None):
        self.logger = get_logger('summarizer_class', __name__, overwrite=False)
        self.preprocess = preprocess
        self.min_words = min_words

        self.morf = morfeusz2.Morfeusz()
        if nlp_model is None:
            self.logger.info("Loading model...")
            self.nlp = spacy.load('pl_nask')
            self.logger.info("Model loaded")
        else:
            self.nlp = nlp_model
        self.nlp.max_length = 3_000_000

        self.cohesion_alg = CohesionSummarizer(self.nlp, self.morf)
        self.frequent_lemmas_alg = FrequentLemmasSummarizer(self.nlp, self.morf)
        self.transformers_alg = TransformersSummarizer(self.nlp)
        self.algorithms = {self.cohesion_alg, self.frequent_lemmas_alg, self.transformers_alg}

    def get_names(self):
        """Cohesion
        Frequent Lemmas
        Transformers"""
        return [alg.name for alg in self.algorithms]

    def summarize(self, text, algorithm_str, limit, unit):
        """throws KeyError"""
        algorithm = {alg.name: alg for alg in self.algorithms}[algorithm_str]
        if unit not in ['words', 'chars']:
            raise KeyError("For 'unit' possible options are 'words' and 'chars'.")
        return self._process(text, algorithm, limit, unit)
    #
    # def frequent_lemmas(self, text, max_words=500):
    #     return self._process(text, max_words, self.frequent_lemmas_alg)
    #
    # def transformer(self, text, max_words=500):
    #     return self._process(text, max_words, self.transformers_alg)
    #
    # def cohesion(self, text, max_words=500):
    #     return self._process(text, max_words, self.cohesion_alg)

    def _process(self, text, algorithm, limit, unit):
        out = {
            'status': 'correct',
            'summary': None,
            'event_id': 0,
            'message': None,
            'algorithm': algorithm.name,
        }
        try:
            if self.preprocess:
                text = preprocess(text)
            n_tokens = len(algorithm.word_tokenizer(text))
            if n_tokens <= 30:
                raise TooShortInputError
            if n_tokens <= limit:
                raise MaxWordsTooLowError

            summary = algorithm(text, limit, unit)
            if len(summary) < 10:
                raise EmptySummaryError
            out['summary'] = summary
        except (SummarizerError, AttributeError, ArithmeticError, NameError, TypeError, ValueError) as ex:
            out['status'] = 'failed'
            if isinstance(ex, SummarizerError):
                out['message'] = self.event_messages[ex.event_id]
                out['event_id'] = ex.event_id

            else:
                out['message'] = self.event_messages[10]
                out['event_id'] = 10
            if isinstance(ex, EmptySummaryError):
                out['summary'] = '[Uwaga: najkrótsze możliwe streszczenie przekracza zadaną długość maksymalną.]'
            else:
                out['summary'] = '[Nie utworzono podsumowania]'
            self.logger.debug(f"Failed at {algorithm.name} algorithm", exc_info=True)
            print(ex)
        return out


class SummarizerError(Exception):
    event_id: int


class TooShortInputError(SummarizerError):
    event_id = 10


class MaxWordsTooLowError(SummarizerError):
    event_id = 11


class EmptySummaryError(SummarizerError):
    event_id = 12


