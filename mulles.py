from pathlib import Path

category_name = "bible"

Path(f"./{category_name}/finished").mkdir(parents=True, exist_ok=True)
Path(f"./{category_name}/words").mkdir(parents=True, exist_ok=True)
Path(f"./{category_name}/formatted_words").mkdir(parents=True, exist_ok=True)
Path(f"./{category_name}/output").mkdir(parents=True, exist_ok=True)
