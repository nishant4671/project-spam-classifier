🎯 2. Detailed Phase 1 Plan: Foundations & Preprocessing
Objective
Establish the project workspace, define strict code quality constraints, and build a deterministic text normalization module (src/preprocess.py) complete with automated unit testing.

Deliverables for Phase 1
Directory & Workspace Setup: Standard directory layout with Python virtual environment isolation (venv).

Text Normalization Module (src/preprocess.py):

Lowercased text conversion.

Regex filtering to strip URLs, email addresses, numbers, and special characters.

Tokenization & English Stop-word removal via NLTK.

Stemming via PorterStemmer to reduce words to their base form.

Automated Testing Suite (tests/test_preprocess.py):

Unit tests using pytest to guarantee edge cases (empty strings, pure punctuation, HTML links, and normal text) are handled gracefully without crashing the pipeline.