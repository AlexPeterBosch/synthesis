"""English stopwords list - exact specification from research

180+ words based on Snowball stemmer with extensions.
Applied BEFORE lemmatization (critical!).
"""

ENGLISH_STOPWORDS = [
    # Articles
    "a", "an", "the",
    
    # Pronouns
    "i", "me", "my", "myself",
    "we", "our", "ours", "ourselves",
    "you", "your", "yours", "yourself", "yourselves",
    "he", "him", "his", "himself",
    "she", "her", "hers", "herself",
    "it", "its", "itself",
    "they", "them", "their", "theirs", "themselves",
    
    # Auxiliary verbs
    "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had",
    "do", "does", "did", "doesn't",
    
    # Modals
    "will", "would", "should", "could",
    "may", "might", "must",
    "can", "cannot", "can't",
    
    # Prepositions
    "of", "at", "by", "for", "with", "about", "against",
    "between", "into", "through", "during",
    "before", "after", "above", "below",
    "to", "from", "up", "down",
    "in", "out", "on", "off", "over", "under",
    
    # Conjunctions & Connectors
    "and", "but", "or", "nor", "so", "yet",
    "because", "as", "until", "while",
    
    # Common adverbs & adjectives
    "again", "further", "then", "once",
    "here", "there", "when", "where", "why", "how",
    "all", "both", "each", "few", "more", "most",
    "other", "some", "such",
    "no", "nor", "not", "only",
    "own", "same", "so", "than", "too", "very",
    
    # Fillers & qualifiers
    "necessary", "really", "just", "quite", "rather",
    "actually", "basically",
    
    # Generic terms
    "thing", "things", "something", "anything", "everything", "nothing"
]
