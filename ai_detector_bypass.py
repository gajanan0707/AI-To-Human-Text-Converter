import spacy
from nltk.corpus import wordnet

# Load SpaCy's English model
nlp = spacy.load("en_core_web_sm")


# Function to get a synonym for a word based on its part of speech
def get_synonym(word, pos_tag):
    if pos_tag.startswith("N"):  # Nouns
        wordnet_pos = wordnet.NOUN
    elif pos_tag.startswith("V"):  # Verbs
        wordnet_pos = wordnet.VERB
    elif pos_tag.startswith("J"):  # Adjectives
        wordnet_pos = wordnet.ADJ
    elif pos_tag.startswith("R"):  # Adverbs
        wordnet_pos = wordnet.ADV
    else:
        return None

    synonyms = wordnet.synsets(word, pos=wordnet_pos)
    if synonyms:
        # Choose a synonym that makes sense contextually
        synonym = synonyms[0].lemmas()[0].name()
        if synonym.lower() != word.lower() and len(synonym.split()) == 1:
            return synonym.replace("_", " ")
    return None


# Function to replace words with synonyms without distorting meaning
def replace_with_synonyms(text):
    doc = nlp(text)
    new_words = []
    for token in doc:
        # Only replace certain word types
        if (
            token.pos_ in ["ADJ", "ADV", "NOUN", "VERB"]
            and not token.ent_type_
            and not token.is_stop
        ):
            synonym = get_synonym(token.text, token.tag_)
            if synonym:
                new_words.append(synonym)
            else:
                new_words.append(token.text)
        else:
            new_words.append(token.text)
    return " ".join(new_words)


# Function to lightly restructure sentences without altering meaning
def restructure_sentences(text):
    doc = nlp(text)
    new_sentences = []
    for sent in doc.sents:
        words = [token.text for token in sent]
        # Only apply minor changes to longer sentences
        if len(words) > 6:
            new_sentence = " ".join(words)
            new_sentences.append(new_sentence)
        else:
            new_sentences.append(" ".join(words))
    return " ".join(new_sentences)


# Main function to humanize AI writing
def humanize_ai_text(text):
    text = replace_with_synonyms(text)
    text = restructure_sentences(text)
    return text


# Example AI-generated text
ai_text = """The rain started as a soft drizzle, barely noticeable at first, but soon it turned into a steady downpour, drenching the streets. Umbrellas popped open like flowers blooming, as people hurried to find shelter. The sound of raindrops hitting the pavement created a rhythmic beat, soothing yet melancholic. In the park, the leaves glistened under the rain, and puddles formed in the low spots, reflecting the gray sky above. Somewhere in the distance, the faint hum of traffic blended with the rain, creating a symphony of the city's life. Despite the wet and cold, there was something comforting about the rain's embrace.
"""

# Convert AI text to a more human-like version
humanized_text = humanize_ai_text(ai_text)

print("Original AI Text:\n", ai_text)
print("\nHumanized Text:\n", humanized_text)
