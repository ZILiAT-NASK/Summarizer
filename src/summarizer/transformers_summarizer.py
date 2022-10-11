# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/Summarizer/LICENSE

import numpy as np
import os
import scipy.spatial.distance
import torch

from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
from transformers import AutoTokenizer, AutoModel, BertConfig

from .summarizer_algorithm import SummarizerAlgorithm
from .libs.common import get_logger


class TransformersSummarizer(SummarizerAlgorithm):
    name = "Transformers"

    def __init__(self, nlp):
        self.logger = get_logger('summarizer_tr', __name__, overwrite=False)
        self.meta_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), r"../meta/")
        os.makedirs(self.meta_dir, exist_ok=True)

        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.bert_config = BertConfig.from_pretrained("allegro/herbert-base-cased", output_hidden_states=True)
        self.bert_model = AutoModel.from_pretrained("allegro/herbert-base-cased", config=self.bert_config).to(self.device)
        self.bert_tokenizer = AutoTokenizer.from_pretrained('allegro/herbert-base-cased')

        self.nlp = nlp
        # self.mbc = 3

    def summarize(self, text, limit, unit):
        doc = self.nlp(text)
        sentences = [(sent.text, self.calc_len(sent, unit)) for sent in doc.sents]

        result = np.zeros((len(sentences), 768), dtype=np.float32)
        bs = 10
        for offs_b in range(0, len(sentences), bs):
            offs_e = min(offs_b + bs, len(sentences))
            sentences_b = [x[0] for x in sentences[offs_b:offs_e]]

            encoded_input = self.bert_tokenizer.batch_encode_plus(sentences_b, padding='longest', add_special_tokens=True,
                                                        return_tensors='pt', truncation=True)
            encoded_input = encoded_input.to(self.device)
            outputs = self.bert_model(**encoded_input)
            # out_tensor: torch.Tensor = outputs.last_hidden_state
            out_tensor: torch.Tensor = outputs.hidden_states[-2]        # i.e. 11
            npd = out_tensor.cpu().detach().numpy()
            # npd = npd[:, 0, :]
            npd = np.average(npd, axis=1)

            result[offs_b:offs_e, :] = npd
            torch.cuda.empty_cache()

        bsv = -1
        best_cluster_labels = None
        for ncl in range(2, 10):
            c_model = AgglomerativeClustering(n_clusters=ncl, linkage='complete', affinity='cosine')
            cluster_labels = c_model.fit_predict(result)
            sv = silhouette_score(result, cluster_labels)
            ccounts = self.count_clusters(cluster_labels)
            marker = ''
            if sv > bsv:
                bsv = sv
                marker = ' (*)'
                best_cluster_labels = cluster_labels

                # logger.debug(f'A-{ncl:02d} ---> {sv:5.3f}{marker}\t\t{ccounts}')
        return self.gen_summ(result, best_cluster_labels, sentences, 'cosine', limit, unit)

    def gen_summ(self, result, cluster_labels, sentences, affinity, limit, unit):
        sep = ' '
        sep_len = 1 if unit == "chars" else 0

        ncl = np.unique(cluster_labels).shape[0]
        centers = np.zeros((ncl, result.shape[1]), dtype=result.dtype)
        distances = np.zeros((result.shape[0],), dtype=result.dtype)
        for clid in range(ncl):
            centers[clid, :] = np.average(result[cluster_labels == clid, :], axis=0)

        for rid in range(result.shape[0]):
            if affinity == 'euclidean':
                distances[rid] = np.linalg.norm(result[rid, :] - centers[cluster_labels[rid], :])
            elif affinity == 'cosine':
                distances[rid] = scipy.spatial.distance.cosine(result[rid, :], centers[cluster_labels[rid], :])
            else:
                raise ValueError('affinity must be either euclidean or cosine')

        xx = list(range(result.shape[0]))
        xx.sort(key=lambda x: distances[x])

        twc = 0
        for s in sentences:
            twc += s[1]
        twc += len(sentences) * (sep_len - 1)

        good_ones = set(range(len(sentences)))
        idx = len(sentences)
        while twc > limit:
            idx -= 1
            twc -= sentences[xx[idx]][1] + sep_len
            good_ones.remove(xx[idx])

        ret = []
        for j, s in enumerate(sentences):
            if j in good_ones:
                ret.append(s[0])

        return sep.join(ret)

    def word_tokenizer(self, text):
        return [tok.text for tok in self.nlp.tokenizer(text)]

    def count_clusters(self, cluster_labels):
        counts = {}
        for j in range(cluster_labels.shape[0]):
            if cluster_labels[j] not in counts:
                counts[cluster_labels[j]] = 1
            else:
                counts[cluster_labels[j]] += 1
        return counts

    def calc_len(self, span, unit):
        if unit == 'words':
            return len(span)
        elif unit == 'chars':
            return len(span.text)
        else:
            raise KeyError
