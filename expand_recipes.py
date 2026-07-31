import os
import sys

import yaml


def merge_recipes(base_path, recipe_dir):
    with open(base_path) as f:
        base_config = yaml.safe_load(f)

    for root, dirs, files in os.walk(recipe_dir):
        for file in files:
            if file.endswith((".yml", ".yaml")) and file != "template.yml":
                path = os.path.join(root, file)
                with open(path) as f:
                    recipe_config = yaml.safe_load(f)

                # Create a fresh copy of base and update with recipe specifics
                full_config = base_config.copy()
                full_config.update(recipe_config)

                with open(path, "w") as f:
                    yaml.dump(full_config, f, default_flow_style=False, sort_keys=False)
                print(f"Expanded: {path}")


if __name__ == "__main__":
    base = "config.yml" if os.path.exists("config.yml") else "screengen/config.yml"
    recipes = "recipes" if os.path.exists("recipes") else "screengen/recipes"
    merge_recipes(base, recipes)
