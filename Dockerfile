FROM pytorch/pytorch:1.6.0-cuda10.1-cudnn7-runtime

USER root

# Обновляем пакеты и устанавливаем необходимые системные зависимости
RUN apt-get update && \
    apt-get install -y ffmpeg libsm6 libxext6 && \
    pip install --upgrade pip

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir \
    jupyter==1.0.0 \
    pandas==1.2.2 \
    nltk==3.5 \
    opencv-python==4.4.0.46 \
    tpu-star==0.0.1-rc10 \
    pre-commit==2.10.1 \
    bezier==2020.5.19 \
    augmixations==0.1.2 \
    albumentations==0.1.12 \
    neptune-client==0.5.1 \
    psutil==5.8.0 \
    tqdm==4.56.2 \
    gdown==3.12.2 \
    torch==1.6.0+cu101 torchvision==0.7.0+cu101 -f https://download.pytorch.org/whl/torch_stable.html

# Создаём рабочую директорию и копируем в неё весь репозиторий
WORKDIR /workspace
COPY . /workspace

# Опционально: если требуется настроить переменные для работы с CUDA
ENV NVIDIA_VISIBLE_DEVICES 0
ENV PATH /usr/local/cuda-10.1/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/cuda-10.1/lib:/usr/local/cuda-10.1/lib64:${LD_LIBRARY_PATH}

EXPOSE 8888

# Запускаем Jupyter Notebook с рабочим каталогом /workspace
CMD ["jupyter", "notebook", "--notebook-dir=/workspace", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--NotebookApp.password=''", "--NotebookApp.token=''", "--allow-root"]
