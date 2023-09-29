import spacy
import collections

def get_keywords(texts, max_words):
    nlp = spacy.load('pl_nask')
    nlp.add_pipe('coreferencer')
    out = {'texts': list(),
           'keywords': list()}
    
    for text in texts:
        doc = nlp(text)

        words = [t for t in doc if t.is_alpha and t.lemma_ not in get_stopwords() and t.pos_ not in get_unwanted_pos()]
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
        common = counter.most_common(max_words)
        return common


def get_stopwords():
    path = 'C:\Users\adamn\Desktop\Summarizer-1\src\summarizer\libs\stopwords.txt'
    with open(path, "r", encoding="utf-8") as stop_words_l:
        stop_words = stop_words_l.read()
        return stop_words
    
def get_unwanted_pos():
    return ['PRON', 'ADP', 'AUX', 'PUNCT', 'DET', 'ABR']