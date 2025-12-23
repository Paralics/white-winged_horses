import sys
from transformers import pipeline
import warnings
warnings.filterwarnings("ignore")

# Загружаем модель для анализа тональности
print("Loading sentiment analysis model...", file=sys.stderr)

# Use a pipeline as a high-level helper
classifier = pipeline("sentiment-analysis", model="./local_model")

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    result = classifier(line)[0]
    print(f"{str.lower(result['label'])}: {result['score']:.4f}")
