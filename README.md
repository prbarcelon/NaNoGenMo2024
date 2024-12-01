This is my [NaNoGenMo 2024](https://github.com/NaNoGenMo/2024) Entry. The goal was to generate a fictitious book using various text generation techniques.

The book is a historical collection of research journal entries by a famous wizard that documents their discovery of various foundational spells in their world. Each entry goes into detail about the spell's incantation, its effects, and the wizard's thoughts on its potential applications.

I used the following approaches:
- A Markov Chain based text generator for the spell incantation. I used synthetic data from a few years ago to train the model.
- Tracery to generate the introduction sentence for each entry. I wanted to give each entry a unique feel and tracery was a good fit for this. I found that just for a single sentence, I ended up writing a lot of rules.
- The rest of the journal entry was generated using an LLM, specifically the llama3.2 3b model through ollama.

# Setup
- Setup virtual environment for Python 3.10.11
- Install ollama
- Download llama3.2 3b model (https://ollama.com/library/llama3.2) via `ollama run llama3.2` command
`
```
pip install -r requirements.txt
```

# Run
Run the script from repository root directory

```
python ./src/entry.py
```