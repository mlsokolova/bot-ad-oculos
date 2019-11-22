**Telegram bot via Tor socket**  
_Assumptions_  
1.A bot registered from @BotFather in Telegram  
2.Telegram HTTP API token got from @BotFather in Telegram  
3.A bot programmed with Python  

_Files_  
``swearing_bot/`` - bot blasphemer code example (Python, nltk, pymorphy2)  
``tor_socket_echo_bot/`` - CentOS 7 docker container for Tor socket + simple echo bot in Python  

_Build_  
```
cd tor_socket_echo_bot
docker build -m 1G --ulimit nofile=65536:65536 -t tor_socket_echo_bot --build-arg TELEGRAM_HTTP_API_TOKEN=<Telegram HTTP API token> .
```
where ``TELEGRAM_HTTP_API_TOKEN`` - Telegram HTTP API token  

_Run_  
```
docker run --rm tor_socket_echo_bot
```





