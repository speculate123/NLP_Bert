import torch
from transformers import AutoTokenizer, AutoModel
from torch.nn.functional import softmax
from torch.utils.data import DataLoader
from transformers import DistilBertForSequenceClassification, AdamW

class BertModel(): 
    def __init__(self):
        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    def loadmodel(self, path):
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(path)
            self.model = DistilBertForSequenceClassification.from_pretrained(path)
            self.model.to(self.device)
        except Exception as e:
            print(e)
        else:
            print('Loaded model.')   
    def predict(self, sentence):
        encoded = self.tokenizer.encode_plus(sentence, return_tensors='pt').to(self.device)
        seq_relationship_logits = self.model(**encoded)[0]
        probs = softmax(seq_relationship_logits, dim=1)
        _, preds = torch.max(probs.data, dim=1)
        preds = preds.tolist()[0]
        return preds