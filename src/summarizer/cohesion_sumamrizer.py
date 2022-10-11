# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/Summarizer/LICENSE

import nltk
import numpy as np
import os
import collections
from .libs.common import get_logger, out_dir, txt_dir, nltk_data_dir, file_iterator, get_stopwords_file
from .summarizer_algorithm import SummarizerAlgorithm


class CohesionSummarizer(SummarizerAlgorithm):
    name = "Cohesion"

    def __init__(self, nlp, morf):
        self.logger = get_logger('summarizer_coh', __name__, overwrite=False)
        self.nlp = nlp
        self.morf = morf
        nltk.data.path.append(nltk_data_dir)
        if not os.path.exists(os.path.join(nltk_data_dir, 'tokenizers/punkt.zip')):
            nltk.download('punkt', download_dir=nltk_data_dir)

        self.stop_words = self.load_stopwords()
        self.threshold = 30
        self.connectors = (
            'A',
            'a',
            'aby',
            'acz',
            'aczkolwiek',
            'albo',
            'albowiem',
            'ale',
            'ani',
            'aniżeli',
            'aż',
            'ażeby',
            'bądź',
            'bo',
            'bodaj',
            'bowiem',
            'by',
            'choć',
            'choćby',
            'chociaż',
            'chyba',
            'co gorsza',
            'co gorsze',
            'coby',
            'czyli',
            'dlatego',
            'gdyż',
            'I',
            'i',
            'innymi słowy',
            'iż',
            'jednak',
            'jednakowo',
            'jednakowoż',
            'jednakże',
            'lecz',
            'mianowicie',
            'mimo to',
            'natomiast',
            'niemniej jednak',
            'oprócz tego',
            'oraz',
            'ponieważ',
            'poza tym',
            'przy czym',
            'przy tym',
            'tudzież',
            'w sensie',
            'więc',
            'z tym że',
            'zaś',
            'zatem',
            'ze względu',
            'z tego',
            'z czego'
        )
        self.unwanted_pos = ['PRON', 'ADP', 'AUX', 'PUNCT', 'DET', 'ABR']

    def summarize(self, text, limit, unit):
        sep = ' '
        sep_len = 1 if unit == "chars" else 0

        doc = self.nlp(text)
        words = [t for t in doc if t.is_alpha and t.lemma_ not in self.stop_words and t.pos_ not in self.unwanted_pos]
        lemmas_counter = collections.Counter(t.lemma_ for t in words)
        common_lemmas = lemmas_counter.most_common(self.threshold)
        common_lemmas_keys = [k for k, v in common_lemmas]
        n_common_types = [len(set(t.lemma_ for t in sent if t.lemma_ in common_lemmas_keys)) for sent in doc.sents]

        def has_connector(sent):
            return sent.text.startswith(self.connectors) or sent[0].pos_ == 'SCJON'
        has_prefix = [has_connector(sent) for sent in doc.sents]
        has_prefix[0] = False

        def get_pieces():
            data = list(zip(doc.sents, has_prefix, n_common_types))
            while len(data) > 0:
                priority_id = np.argmax(n for _, _, n in data)
                sent, has_pr, _ = data.pop(int(priority_id))
                piece = [sent]
                while has_pr:
                    priority_id = priority_id - 1
                    sent, has_pr, _ = data.pop(priority_id)
                    piece.append(sent)
                yield piece

        summary_sents = []
        curr_len = 0
        for frag in get_pieces():
            frag_len = sum(self.calc_len(f, unit) for f in frag) + (len(frag) - 1) * sep_len
            if curr_len + frag_len + sep_len <= limit:
                summary_sents.extend(frag)
                curr_len += frag_len + sep_len
            else:
                break

        summary_sents.sort(key=lambda x: x[0].i)
        summary = sep.join(s.text for s in summary_sents)
        return summary

    def load_stopwords(self):
        with open(get_stopwords_file(), "r", encoding="utf-8") as stop_words_l:
            stop_words = stop_words_l.read()
            return stop_words

    def word_tokenizer(self, text):
        return [tok.text for tok in self.nlp.tokenizer(text)]

    def calc_len(self, span, unit):
        if unit == 'words':
            return len(span)
        elif unit == 'chars':
            return len(span.text)
        else:
            raise KeyError
