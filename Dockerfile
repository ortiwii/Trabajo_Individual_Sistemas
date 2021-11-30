FROM python:3.8-slim
RUN useradd --create-home --shell /bin/bash app_user
WORKDIR /home/app_user
COPY aplicacion_cliente.py ./
RUN pip install rethinkdb
RUN pip install readchar
USER app_user
CMD ["bash"]