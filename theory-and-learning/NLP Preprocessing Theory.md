2. The Text Normalization Pipeline
Before converting words to numbers, we clean and standardise the text to reduce noise and lower the vocabulary size:

Tokenization: Breaking down a continuous string of text into discrete atomic units (tokens), such as individual words, punctuation, or sub-words.

Stop-Word Removal: Eliminating ultra-common grammatical filler words (e.g., "and", "the", "is", "at"). These words carry almost zero domain-specific signal for spam vs. non-spam (ham) distinction, and removing them dramatically reduces feature dimension.

Stemming vs. Lemmatization:

Stemming uses crude heuristic rules to chop off the ends of words (e.g., "running", "runs", "runner" all become "runn"). It is fast but often produces non-real words.

Lemmatization uses a morphological vocabulary and dictionary analysis to map words back to their dictionary base form (lemma) (e.g., "better" becomes "good")



What Exactly is Lemmatization?
Lemmatization is the process of taking a word and reducing it to its dictionary root form, which is called a lemma.

Think of the lemma as the "headword" you would look up in a physical dictionary. If you looked up "running," you'd find it under "run." If you looked up "mice," you'd find it under "mouse." That’s exactly what lemmatization does.

How Does It Actually Work? (The Mechanics)
Lemmatization is not just a set of chop-rule hacks. It is a linguistically-informed process that requires two things:

A Lexicon (Dictionary/Vocabulary): The algorithm has a massive built-in dictionary (like WordNet) that contains all known base forms of words. It maps inflected words back to these base entries.

Part-of-Speech (POS) Tagging: This is the secret sauce. To choose the correct lemma, the algorithm must know the grammatical role of the word in the sentence.

Why does POS matter?
Consider the word "saw":

If it's used as a verb ("I saw a bird"), the lemma is "see".

If it's used as a noun ("I used a saw to cut wood"), the lemma is "saw" (because it's already a base noun).

If you don't provide POS tags, the lemmatizer usually defaults to treating everything as a noun, which leads to errors. So, your earlier example ("better" → "good") only works if the lemmatizer knows that "better" is being used as an adjective (JJ in tagger-speak). If it defaults to a noun, it leaves "better" unchanged.

Lemmatization vs. Stemming (The Classic Confusion)
People mix these up all the time. Here is the easiest way to remember the difference:

Feature	Stemming	Lemmatization
What it does	Uses crude, hard-coded rules to chop off the ends of words.	Uses a dictionary and grammar rules to look up the real base word.
Speed	Very fast (just string manipulation).	Slower (requires POS tagging and a dictionary lookup).
Output	May produce non-real words (e.g., "running" → "runn").	Always produces a real, valid dictionary word.
Examples	"studies" → "studi"
"better" → "better" (no change)	"studies" → "study"
"better" → "good" (if POS is adjective)
In short: Stemming is a blunt axe; lemmatization is a scalpel.

Why Do We Use Lemmatization in NLP?
Reduces Vocabulary Size: Instead of your model treating "run," "running," and "ran" as three completely different words, lemmatization groups them into one feature ("run"). This makes the model more efficient and reduces noise.

Improves Meaning Extraction: Because it understands context (via POS tags), it preserves actual meaning better than stemming.

Crucial for Search Engines and Chatbots: If a user searches for "better results," and your system lemmatizes it to "good results," you can match documents that use the word "good" even if they don't use "better."

When Should You NOT Use It?
When processing massive, real-time streams (e.g., live Twitter data): Stemming is faster and "good enough."

When working with slang, usernames, or new technical jargon: Lemmatizers rely on standard dictionaries. If a word isn't in the dictionary (like "deepfake" a few years ago, or "yeet"), the lemmatizer gives up and leaves it unchanged.

When your model is fine-tuned for exact wording: Some transformer models (like BERT) actually prefer raw, un-lemmatized text because they learn context from the exact inflected forms during pre-training.

Popular Tools/Libraries to Do It
NLTK (WordNet Lemmatizer): The classic Python library. You have to manually pass in the POS tag (e.g., wnl.lemmatize('better', pos='a') for adjective).

spaCy: The gold standard for production. It automatically does POS tagging and lemmatization in one go (e.g., token.lemma_).

TextBlob: A simpler wrapper over NLTK, easier for beginners.

Final Summary Rule of Thumb
Use Lemmatization when you care about the linguistic meaning of the word and have the processing power to handle it.
Use Stemming when you just need to group similar words together quickly and don't mind a few spelling errors.