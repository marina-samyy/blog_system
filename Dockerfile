

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


FROM python:3.11-slim

WORKDIR /code

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# بنسخ الـ requirements من مكانها (اللي هو دلوقتي جوه app بالنسبة للـ context الجديد)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# بنسخ كل حاجة في الفولدر الرئيسي
COPY . .

EXPOSE 8000

# بنشغل الـ main اللي جوه فولدر app
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]