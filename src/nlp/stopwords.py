"""English Stopwords List

Exact 180+ word stopwords list based on InfraNodus specifications.
Derived from Snowball stopwords with additions.
"""

ENGLISH_STOPWORDS = [
    # Articles
    "a", "an", "the",
    # Pronouns
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves",
    "you", "your", "yours", "yourself", "yourselves",
    "he", "him", "his", "himself", "she", "her", "hers", "herself",
    "it", "its", "itself", "they", "them", "their", "theirs", "themselves",
    # Auxiliary verbs
    "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "doesn't",
    # Modals
    "will", "would", "should", "could", "may", "might", "must", "can", "cannot", "can't",
    # Prepositions
    "of", "at", "by", "for", "with", "about", "against", "between", "into",
    "through", "during", "before", "after", "above", "below", "to", "from",
    "up", "down", "in", "out", "on", "off", "over", "under",
    # Conjunctions
    "and", "but", "or", "because", "as", "until", "while", "nor", "so", "yet",
    # Adverbs
    "again", "further", "then", "once", "here", "there", "when", "where",
    "why", "how", "very", "too", "really", "just", "quite", "rather", "actually", "basically",
    # Quantifiers
    "all", "both", "each", "few", "more", "most", "other", "some", "such",
    # Negations
    "no", "nor", "not", "only",
    # Common adjectives
    "own", "same", "necessary",
    # Other
    "than", "thing", "things", "something", "anything", "everything", "nothing"
]


def load_stopwords(custom_stopwords: List[str] = None, 
                   remove_stopwords: List[str] = None) -> set:
    """Load stopwords with custom additions/removals.
    
    Args:
        custom_stopwords: Additional stopwords to add
        remove_stopwords: Stopwords to remove from default list
    
    Returns:
        Set of stopwords
    """
    stopwords = set(ENGLISH_STOPWORDS)
    
    if custom_stopwords:
        stopwords.update(custom_stopwords)
    
    if remove_stopwords:
        stopwords -= set(remove_stopwords)
    
    return stopwords
