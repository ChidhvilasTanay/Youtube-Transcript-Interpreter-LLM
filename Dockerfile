FROM python


COPY requirements.txt /langchain-yt-app/requirements.txt
COPY .venv /langchain-yt-app/
COPY .env /langchain-yt-app/
COPY main.py /langchain-yt-app/
COPY langchain_helper.py /langchain-yt-app/



WORKDIR /langchain-yt-app

RUN pip install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]



