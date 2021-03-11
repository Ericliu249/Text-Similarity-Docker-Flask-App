import re
import string
import math 

class Similarity(object):

    def __init__(self, stop_words=True):
        self.stop_words = stop_words

    def tokenize(self, text):
        tokens = re.findall(r"\w+", text)
        stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 
        'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 
        'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 
        'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 
        'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 
        'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 
        'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 
        'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 
        'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 
        'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 
        'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 
        'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 
        'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 
        'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 
        'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 
        're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', 
        "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven',
        "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 
        'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 
        'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", 'film', 'films']
        if self.stop_words:
            tokens = [token for token in tokens if token not in stop_words]
        return tokens

    def get_all_chars(self, text_list):
        tokenized_texts = [self.tokenize(text) for text in text_list]
        all_chars = list(set().union(*tokenized_texts))
        return all_chars

    def get_work_frequency(self, words, all_chars):
        word_dict = dict.fromkeys(all_chars, 0)
        for word in words:
            word_dict[word] += 1
        return word_dict

    def compute_tf(self, word_dict, words):
        tf = {}
        for word, frequency in word_dict.items():
            tf[word] = frequency/float(len(words))
        return tf

    def compute_idf(self, doc_list):
        idf = dict.fromkeys(doc_list[0].keys(), 0)
        for word, value in idf.items():
            doc_with_word_count =  sum([1 if doc[word] > 0 else 0 for i, doc in enumerate(doc_list)])
            idf[word] = math.log10((len(doc_list) + 1) / (float(doc_with_word_count) + 1) + 1)
        return idf

    def compute_tfidf(self, tf, idf):
        tfidf_dict = {}
        for word, value in tf.items():
            tfidf_dict[word] = value * idf[word]
        tfidf = list(tfidf_dict.values())
        return tfidf

    def compute_similarity(self, tfidf_a, tfidf_b):
        numerator = 0
        for i in range(len(tfidf_a)):
            numerator += tfidf_a[i] * tfidf_b[i]
        print(numerator)
        denominator = math.sqrt(sum([i ** 2 for i in tfidf_a])) * math.sqrt(sum([i ** 2 for i in tfidf_b]))
        print(denominator)
        similarity = round(numerator / denominator, 2)
        return similarity

    def get_result(self, text_list):
        sample_a = self.tokenize(text_list[0])
        sample_b = self.tokenize(text_list[1])
        all_chars = self.get_all_chars(text_list)
        word_dict_a = self.get_work_frequency(sample_a, all_chars)
        word_dict_b = self.get_work_frequency(sample_b, all_chars)
        tf_a = self.compute_tf(word_dict_a, sample_a)
        tf_b = self.compute_tf(word_dict_b, sample_b)
        doc_list = [word_dict_a, word_dict_b]
        idf = self.compute_idf(doc_list)
        tfidf_a = self.compute_tfidf(tf_a, idf)
        tfidf_b = self.compute_tfidf(tf_b, idf)
        result = self.compute_similarity(tfidf_a, tfidf_b)
        return result


# text_list = [
#         "The easiest way to earn points with Fetch Rewards is to just shop for the products you already love. If you have any participating brands on your receipt, you'll get points based on the cost of the products. You do not need to clip any coupons or scan individual barcodes. Just scan each grocery receipt after you shop and we'll find the savings for you.",
#         "The easiest way to earn points with Fetch Rewards is to just shop for the items you already buy. If you have any eligible brands on your receipt, you will get points based on the total cost of the products. You do not need to cut out any coupons or scan individual UPCs. Just scan your receipt after you check out and we will find the savings for you.",
#         "We are always looking for opportunities for you to earn more points, which is why we also give you a selection of Special Offers. These Special Offers are opportunities to earn bonus points on top of the regular points you earn every time you purchase a participating brand. No need to pre-select these offers, we'll give you the points whether or not you knew about the offer. We just think it is easier that way."
#     ]

# text_case = Similarity(False).get_result(text_list)
# print(text_case)