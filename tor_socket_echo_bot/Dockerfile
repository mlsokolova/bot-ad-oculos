FROM centos:7
ARG TELEGRAM_HTTP_API_TOKEN
RUN yum install -y python wget epel-release && yum install -y tor python-pip
#RUN locale-gen en_US.UTF-8
#COPY ./default_locale /etc/default/locale
#RUN chmod 0755 /etc/default/locale
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8
ADD . /opt/tor_socket_echo_bot/
WORKDIR /opt/tor_socket_echo_bot
RUN echo -e "[DEFAULT]\ntoken=$TELEGRAM_HTTP_API_TOKEN\nproxy_url=socks5h://127.0.0.1:9050" > /opt/tor_socket_echo_bot/config.ini 
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ./run.sh
