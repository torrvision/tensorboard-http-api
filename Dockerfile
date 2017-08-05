FROM tensorflow/tensorflow:latest

# python code
RUN pip install flask
ADD flaskapp /flaskapp
WORKDIR /flaskapp
RUN python setup.py install
WORKDIR /

# server
ADD startup.sh /
ADD patch_tensorboard.py /
EXPOSE 6006 6007
ENTRYPOINT ["/bin/bash", "/startup.sh"]
