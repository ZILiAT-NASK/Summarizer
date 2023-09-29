# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/Summarizer/LICENSE

import nltk
import numpy as np
import os
import collections
import coreferencer
from .libs.common import get_logger, nltk_data_dir, get_stopwords_file
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

    def summarize(self, text, limit, unit, alg_type):
        sep = ' '
        sep_len = 1 if unit == "chars" else 0
        if alg_type == 'coreferences':
            self.nlp.add_pipe('coreferencer')
        doc = self.nlp(text)
        words = [t for t in doc if t.is_alpha and t.lemma_ not in self.stop_words and t.pos_ not in self.unwanted_pos]
        # freq_words_counter = collections.Counter(t for t in words) # słowa w odmianie książka / książce
        if alg_type == 'lemmas':
            counter = collections.Counter(t.lemma_ for t in words)
        if alg_type == 'words':
            threshold = 0.9
            similarity_finds = dict()
            counter = collections.Counter(t.text for t in words)
            for w1 in doc:
                similarity_finds[w1.text] = 0
                for w2 in doc:
                    if w1 is not w2:
                        similarity = w1.similarity(w2)
                        if similarity > threshold:
                            similarity_finds[w1.text] += counter[w2.text]
            for w in similarity_finds:
                counter[w] += similarity_finds[w]
        if alg_type == 'coreferences':
            counter = collections.Counter(t.lemma_ for t in words)
            coref_clusters = doc._.coref.clusters
            for w in counter:
                cluster_count = 0
                for cluster in coref_clusters:
                    mention_flg = False
                    for mention in cluster.mentions:
                        mention_count = 0
                        mention_lemmas = [t.lemma_ for t in mention.span]
                        if w in mention_lemmas:
                            mention_count += 1
                        else:
                            mention_flg = True
                        if mention_flg:
                            cluster_count += mention_count
                counter[w] += cluster_count              
        common = counter.most_common(self.threshold)
        common_keys = [k for k, v in common]

        sent_common_counter = list()
        sent_with_connectors = list()
        for i, sent in enumerate(doc.sents):
            sent_common = 0
            for key in common_keys:
                if alg_type == 'words' and key in [w.text for w in sent]:
                    sent_common += 1
                elif alg_type in ['coreferences', 'lemmas'] and key in [w.lemma_ for w in sent]:
                    sent_common += 1
            if sent.text.lower().startswith(tuple([c+' ' for c in self.connectors])) or sent[0].pos_ == 'SCJON' and i != 0:
                sent_common_counter.append(-1)
                sent_with_connectors.append('')
                for j in range(i-1, -1, -1):
                    if sent_common_counter[j] >= 0:
                        sent_common_counter[j] = max(sent_common, sent_common_counter[j])
                        sent_with_connectors[j] = ' '.join([sent_with_connectors[j], sent.text])
                        break
            else:
                sent_common_counter.append(sent_common)
                sent_with_connectors.append(sent.text)
        _, sent_with_connectors = zip(*sorted(zip(sent_common_counter, sent_with_connectors), reverse=True))
        out = ''
        out_count = 0
        for i, sent in enumerate(sent_with_connectors):
            if unit == 'words':
                sent_len = len(sent.split())
            elif unit == 'chars':
                sent_len = len(sent)
            if out_count + sent_len <= limit:
                out = ' '.join([out, sent])
                out_count += sent_len
            else:
                if out_count == 0:
                    continue
                else:
                    break
        return out

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
