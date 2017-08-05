FROM tensorflow/tensorflow:latest

# python code
RUN pip install flask
ADD flaskapp /flaskapp
WORKDIR /flaskapp
RUN python setup.py install
WORKDIR /

# server
ADD startup.sh /
ADD server.py /
ADD patch_tensorboard.py /
EXPOSE 6007
# TODO: move from cmd to entrypoint
ENTRYPOINT ["/bin/bash", "/startup.sh"]
