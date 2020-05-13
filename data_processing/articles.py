import torch
import json
import numpy as np
import re
import collections

# define Articles dataset class for easy sampling, iteration, and weight creating
class Articles(torch.utils.data.Dataset):
    def __init__(self, json_file):
        super().__init__()
        with open(json_file, "r") as data_file:
            self.examples = json.loads(data_file.read())

    def __getitem__(self, idx):
        return self.examples[idx]

    def __len__(self):
        return len(self.examples)

    def tokenize(self):
        for idx, example in enumerate(self.examples):
            self.examples[idx]['text'] = re.findall('[\w]+', self.examples[idx]['text'].lower())

    def create_positive_sampler(self, target_publication):
        prob = np.zeros(len(self))
        for idx, example in enumerate(self.examples):
            if example['model_publication'] == target_publication:
                prob[idx] = 1
        return torch.utils.data.WeightedRandomSampler(weights=prob, num_samples=len(self), replacement=True)

    def create_negative_sampler(self, target_publication):
        prob = np.zeros(len(self))
        for idx, example in enumerate(self.examples):
            if example['model_publication'] != target_publication:
                prob[idx] = 1
        return torch.utils.data.WeightedRandomSampler(weights=prob, num_samples=len(self), replacement=True)

    def map_items(self, word_to_id, url_to_id, publication_to_id, filter=False, min_length=0):
        min_length_articles = []
        for idx, example in enumerate(self.examples):
            self.examples[idx]['text'] = [word_to_id.get(word, len(word_to_id)) for word in example['text']]
            self.examples[idx]['text'] = [word for word in example['text'] if word != len(word_to_id)]
            if filter:
                if len(self.examples[idx]['text']) > min_length:
                    min_length_articles.append(self.examples[idx])
            self.examples[idx]['url'] = url_to_id.get(example['url'], url_to_id.get("miscellaneous"))
            self.examples[idx]['model_publication'] = publication_to_id.get(example['model_publication'], publication_to_id.get("miscellaneous"))
        return min_length_articles
