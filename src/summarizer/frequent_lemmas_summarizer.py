# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/Summarizer/LICENSE

import collections
import re
from .summarizer_algorithm import SummarizerAlgorithm
from .libs.common import get_logger


class FrequentLemmasSummarizer(SummarizerAlgorithm):
    name = "Frequent Lemmas"

    def __init__(self, nlp, morf):
        self.logger = get_logger('summarizer_fl', __name__, overwrite=False)
        self.nlp = nlp
        self.morf = morf

    def summarize(self, text, limit, unit):
        frq_lemmas = self.get_frequent_lemmas(text)
        sentences = self.sentence_tokenizer(text)

        s2hc = {}  # sentence to hit count
        s2wc = {}  # sentence to word count

        twc = 0  # total word count
        for (i, sentence) in enumerate(sentences):
            words = self.word_tokenizer(sentence.lower())
            lemmas = set()
            for word in words:
                analysis = self.morf.analyse(word)
                for interpretation in analysis:
                    lemmas.add(re.sub(r":.*", "", interpretation[2][1]))
            hit_count = len(lemmas.intersection(frq_lemmas))
            s2wc[i] = self.count_len(sentence, unit)
            s2hc[i] = hit_count
            twc += s2wc[i]

        ret = None
        owc = 0
        for req in range(1, len(frq_lemmas) + 1):
            sid = [i for i in s2hc.keys() if s2hc[i] >= req]
            wc = sum([s2wc[i] for i in sid])

            # logger.debug(f'Require at least {req} hit(s) per sentence')
            # logger.debug(f'{len(sid):03d} / {sc:03d} sentences, having {wc} words.')

            if wc == owc:
                continue
            else:
                owc = wc
                if wc <= limit:
                    ret = '\n'.join([re.sub(r'\n+', ' ', sentences[i]) for i in sid])
                    return ret

            if len(sid) == 0:
                # logger.warning('summarizer failed, length too big or zero.')
                break

        # logger.warning('summarizer failed, need more frequent lemmas.')
        return ret

    def get_frequent_lemmas(self, txt, n=30):
        words = self.word_tokenizer(txt.lower())

        words_alpha = [word for word in words if word.isalpha()]
        words_no_stop = [word for word in words_alpha if not self.nlp.vocab[word].is_stop]

        fdist = collections.Counter(words_no_stop)
        fdist_most = [elem[0] for elem in fdist.most_common()]

        r_words = set()
        r_lemmas = set()

        for word in fdist_most:
            wll = []
            analysis = self.morf.analyse(word)
            for interpretation in analysis:
                i_word = interpretation[2][0]
                i_lemma = re.sub(r":.*", "", interpretation[2][1])
                wll.append((i_word, i_lemma))
                # logger.debug(f'{i_word} --> {i_lemma}')

            checks = [wl[1] in r_lemmas for wl in wll]
            if not any(checks):  # none of the lemmas known
                for i_word, i_lemma in wll:
                    r_words.add(i_word)
                    r_lemmas.add(i_lemma)

            if len(r_words) >= n:
                break

        return r_lemmas

    def sentence_tokenizer(self, text):
        patt_wc = re.compile(r'\w')
        doc = self.nlp(text)
        return [sent.text.strip() for sent in doc.sents if re.match(patt_wc, sent.text)]

    def word_tokenizer(self, text):
        return [tok.text for tok in self.nlp.tokenizer(text)]

    def count_len(self, text, unit):
        if unit == 'words':
            return len(self.word_tokenizer(text))
        elif unit == 'chars':
            return len(text)
        else:
            raise KeyError
