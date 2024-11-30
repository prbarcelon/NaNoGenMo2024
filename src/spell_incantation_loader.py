# This file loads ./data/spell_incantations.tsv, a tab-separated file with the
# following columns:
# - color_element
# - spell_incantation
#
# It then creates a dictionary of spell incantations, with the key being the
# color element and the value being a list of incantations.
#
# Current count of incantations per color element:
# black: 258 incantations
# blue: 258 incantations
# green: 258 incantations
# orange: 258 incantations
# purple: 258 incantations
# red: 258 incantations
# yellow: 258 incantations

import csv
from typing import Dict, List

def load_incantations(file_path: str) -> Dict[str, List[str]]:
    """
    Loads spell incantations from a tab-separated file of color_element and spell_incantation.

    Returns a dictionary of color_element to list of spell incantations.
    """
    incantations = {}
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            color_element = row["color_element"]
            incantation = row["spell_incantation"]
            if color_element not in incantations:
                incantations[color_element] = []
            incantations[color_element].append(incantation)
    return incantations

# Example usage
if __name__ == "__main__":
    incantations = load_incantations("./data/spell_incantations.tsv")
    for color_element, spells in incantations.items():
        print(f"{color_element}: {len(spells)} incantations")
