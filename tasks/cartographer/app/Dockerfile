FROM imachug/kyzylborda_lib
RUN pip install gunicorn
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /private
RUN wget https://upload.wikimedia.org/wikipedia/commons/7/7b/Vegetation-no-legend.PNG -O biome_map.png
COPY geotag.py .
COPY prepare.py .
RUN python3 prepare.py
WORKDIR /app
CMD ["gunicorn", "-b", "unix:/tmp/app.sock", "server:app"]
