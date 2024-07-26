# Используем официальный образ Python в качестве базового образа
FROM python:3.10.14-alpine3.18

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBEFFERED 1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app
# Копируем файл requirements.txt внутрь контейнера
COPY /requirements.txt .
COPY /deployment/app/entrypoint.sh /entrypoint.sh

# Устанавливаем зависимости, описанные в файле requirements.txt
RUN pip install -r requirements.txt

RUN chmod +x /entrypoint.sh
COPY . .
ENTRYPOINT ["/entrypoint.sh"]
