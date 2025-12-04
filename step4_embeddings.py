# https://semantle.com/junior


# pip install gensim umap-learn
# pip install --no-cache-dir spacy && python -m spacy download en_core_web_md

from gensim.models import Word2Vec
import umap
import matplotlib.pyplot as plt
from gensim.utils import simple_preprocess
import steps.step0_setup
from ramda import *


# Define training data
import yaml

with open('steps/step4_sentences.yaml', 'r') as file:
    sentences = yaml.safe_load(file)

# Create a dictionary for word frequencies
# Tokenize the sentences and update word frequency
def get_embeddings(key, vector_size, distances):
    distances = map(split(' '), reject(is_empty, split('\n', distances)))
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    tokenized_sentences = [[word for word in simple_preprocess(sentence) if word not in stop_words] for sentence in sentences[key]]

    # Train the Word2Vec model
    model = Word2Vec(tokenized_sentences, vector_size=vector_size, sg=0, negative=100, seed=42, window=100, min_count=1, epochs=1000)

    # Extract the words & their vectors, as numpy arrays
    words = list(model.wv.index_to_key)
    vectors = model.wv[words]

    for w in words:
        print(w, '\t', join('\t', map(str, model.wv[w])))

    for one, two in distances:
        distance = model.wv.distance(one, two)
        print(f'"{one}" -> "{two}": {distance}')
            

    show_UMAP(vectors, words)

def show_UMAP(vectors, words):
    # Reduce dimensions to 2D using UMAP
    umap_model = umap.UMAP(n_neighbors=5, min_dist=0.3, n_components=2)
    umap_result = umap_model.fit_transform(vectors)

    # Plotting the result
    plt.figure(figsize=(10, 7))
    plt.scatter(umap_result[:, 0], umap_result[:, 1], alpha=0.7)
    for i, word in enumerate(words):
        plt.annotate(word, xy=(umap_result[i, 0], umap_result[i, 1]))
    plt.title('Word Embeddings visualized with UMAP')
    plt.show()




def draw_simple_graph(points, labels):
    import matplotlib.pyplot as plt
    x = [point[0] for point in points]
    y = [point[1] for point in points]
    plt.figure(figsize=(10, 7))
    plt.scatter(x, y, alpha=0.7)
    for i, label in enumerate(labels):
        plt.annotate(label, xy=(x[i], y[i]))
    plt.title('Simple Graph')
    plt.show()

draw_simple_graph(
    [[1,0], [0,1], [-1,-1], [.1,.9], [.9,0.1]], 
    ['cat', 'dog', 'mouse', 'bark', 'meow']
)

get_embeddings('easy', 2, """
dog cat
dog barks
cat barks
dog meows
cat meows
""")

get_embeddings('simple', 2, """
dog cat
dog mouse
cat mouse
dog afraid
cat afraid
dog barked
cat barked
dog tail
cat tail
dog mailman
cat mailman
""")

get_embeddings('pets_and_law', 10, """
amendment constitution
dog cat
amendment cat
constitution dog
""")


import spacy

def get_embeddings(prompt, samples):
    nlp = spacy.load("en_core_web_md")
    prompt_doc = nlp(prompt)
    sample_docs = [nlp(sample) for sample in samples.split('\n') if sample.strip() != '']
    for doc in sample_docs:
        print(doc, '\n', prompt, prompt_doc.similarity(doc), doc.vector, '\n')

get_embeddings(
    'The recent amendment to the constitution was challenged in the high court due to concerns about its legality.',
    """The recent amendment to the constitution was challenged in the high court due to concerns about its legality.
    The recent decision to the constitution was challenged in the JUDGE due to concerns about its legality.
    Legal experts gathered at the conference to discuss the implications of international law on trade agreements.
    He taught his dog to fetch the newspaper every morning, making it a helpful part of the family routine.
    """
)