FROM python:3.9

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN python -m spacy download en_core_web_sm

RUN python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet'); nltk.download('omw-1.4')";

COPY . .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]