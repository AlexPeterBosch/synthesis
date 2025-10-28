"""Sample texts for testing"""

SAMPLE_TEXT_1 = """Companies are analyzing customer feedback using AI tools. 
The research shows that machine learning improves sentiment analysis.
Laboratories are developing new algorithms for natural language processing."""

SAMPLE_TEXT_2 = """Artificial intelligence transforms how businesses understand customer needs.
Data analysis reveals patterns in user behavior and preferences.
Automation tools streamline the feedback collection process."""

SAMPLE_TOKENS_1 = ["company", "analyze", "customer", "feedback", "use", "ai", "tool"]

SAMPLE_NGRAMS_1 = [
    ("company", "analyze", 3),  # bigram
    ("analyze", "customer", 3),
    ("customer", "feedback", 3),
    ("company", "customer", 2),  # distance 1
    ("analyze", "feedback", 2),
    ("company", "feedback", 1),  # distance 2
]
