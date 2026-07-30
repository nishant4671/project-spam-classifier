Engineering Choice: Stemming vs. Lemmatization

Stemming (Porter Stemmer): Uses quick, rule-based algorithms to cut off word endings (e.g., "running" becomes "run", "studies" becomes "studi"). It is extremely fast and light on CPU, but can create non-dictionary words.

Lemmatization (WordNet Lemmatizer): Uses a full dictionary and part-of-speech context to reduce words to real dictionary bases (e.g., "better" becomes "good"). It is more accurate, but noticeably slower and requires more memory.

For a real-time SMS API, speed and low latency are huge priorities. Since Naive Bayes / TF-IDF models don't strictly care if a stem is a real dictionary word as long as it groups related words together, Porter Stemming is standard.