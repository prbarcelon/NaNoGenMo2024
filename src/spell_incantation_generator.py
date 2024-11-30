# Uses corpus of spells to generate incantations

from typing import Dict, List

import markovify

from spell_incantation_loader import load_incantations


class SpellIncantationGenerator:
    def __init__(
        self,
        file_path: str,
        character_limit: int = 500,
        state_size: int = 3,
    ) -> None:
        """
        Initializes the SpellIncantationGenerator with a file path to a TSV file of incantations.

        Uses random, so you may want to set a seed for reproducibility (import random; random.seed(42)).

        :param file_path: The file path to the TSV file of incantations.
        :param character_limit: The character limit for the generated incantations.
        :param state_size: The state size for the Markov chain model.
        """
        self.character_limit = character_limit
        self.state_size = state_size
        self.incantations: Dict[str, List[str]] = load_incantations(file_path)
        self.models: Dict[str, markovify.Text] = self._build_models()

    def generate_incantation(self, color_element: str) -> str:
        """
        Generates an incantation for a given color element.
        """
        assert color_element in self.incantations, f"Color element '{color_element}' not found in incantations."
        # return self.models[color_element].make_short_sentence(self.character_limit)
        return self.models[color_element].make_sentence()

    def _build_models(self) -> Dict[str, markovify.Text]:
        models = {}
        for color_element, spell_incantations in self.incantations.items():
            text_model = markovify.Text("\n".join(spell_incantations), state_size=self.state_size)
            models[color_element] = text_model
        return models
