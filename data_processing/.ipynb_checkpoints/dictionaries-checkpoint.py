import collections
import pathlib as Path
import json
import errno
import os

# function to create dictionaries for words and urls for all datasets at once
def create_merged_dictionaries(all_examples, target_publication):
    counter = collections.Counter()
    url_counter = collections.Counter()
    publication_counter = collections.Counter()
    urls = []
    publications = []
    publications.append(target_publication)

    for example in all_examples:
        counter.update(example['text'])
        counter.update(example['title'])
        urls.append(example['url'])
        publications.append(example['model_publication'])

    url_counter.update(urls)
    publication_counter.update(publications)
    word_to_id = {word: id for id, word in enumerate(counter.keys())}
    article_to_id = {word: id for id, word in enumerate(url_counter.keys())}
    publication_to_id = {publication: id for id, publication in enumerate(publication_counter.keys())}
    word_to_id.update({"miscellaneous": len(word_to_id)})
    article_to_id.update({"miscellaneous": len(article_to_id)})
    publication_to_id.update({"miscellaneous": len(publication_to_id)})
    return word_to_id, article_to_id, publication_to_id


# save dictionary files for future use and ease of access
def save_dictionaries(final_word_ids, final_url_ids, final_publication_ids, dict_path):
    word_dict_path = dict_path / "word_dictionary.json"
    article_dict_path = dict_path / "article_dictionary.json"
    publication_dict_path = dict_path / "publication_dictionary.json"
    
    with open(word_dict_path, "w") as file:
        json.dump(final_word_ids, file)

    with open(article_dict_path, "w") as file:
        json.dump(final_url_ids, file)

    with open(publication_dict_path, "w") as file:
        json.dump(final_publication_ids, file)
    
    print("Dictionaries saved to /dictionary folder.")
    
    
def load_dictionaries(dictionary_dir):
    word_dict_path = abs_dictionary_dir / "word_dictionary.json"
    url_id_path = abs_dictionary_dir / "article_dictionary.json"
    publication_id_path = abs_dictionary_dir / "publication_dictionary.json"

    if Path(word_dict_path).is_file() and Path(url_id_path).is_file() and Path(publication_id_path).is_file():
        with open(word_dict_path, "r") as file:
            final_word_ids = json.load(file)

        with open(url_id_path, "r") as file:
            final_url_ids = json.load(file)

        with open(publication_id_path, "r") as file:
            final_publication_ids = json.load(file)

        print("Dictionaries Loaded")
    else:
        raise FileNotFoundError
    return final_word_ids, final_url_ids, final_publication_ids