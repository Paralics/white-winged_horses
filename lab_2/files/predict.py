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

# import sys
# from transformers import AutoModel, AutoTokenizer
#
# # Загружаем модель для анализа тональности
# print("Loading sentiment analysis model...", file=sys.stderr)
#
# # Загружаем из локальной директории
# model = AutoModel.from_pretrained("./model")
# tokenizer = AutoTokenizer.from_pretrained("./model")
# print("Model ready! Send me text for sentiment analysis.", file=sys.stderr)
#
# for line in sys.stdin:
#     line = line.strip()
#     if not line:
#         continue
#     inputs = tokenizer(line, return_tensors="pt")
#     outputs = model(**inputs)
#     print(outputs)
    # try:
    #     text = "I love this product! It's amazing."
    #     inputs = tokenizer(text, return_tensors="pt")
    #     outputs = model(**inputs)
    #     print(outputs)
        # # Если пришел JSON, извлекаем текст
        # if line.startswith('{'):
        #     data = json.loads(line)
        #     text = data.get('text', '')
        # else:
        #     text = line
        #
        # if not text:
        #     result = {"error": "No text provided"}
        # else:
        #     # Делаем предсказание
        #     prediction = classifier(text[:512])  # Ограничиваем длину
        #     result = {
        #         "text": text,
        #         "sentiment": prediction[0]['label'],
        #         "confidence": prediction[0]['score']
        #     }
        #
        # print(json.dumps(result))
    #
    # except Exception as e:
    #     print(json.dumps({"error": str(e)}))
