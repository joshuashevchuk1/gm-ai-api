# gm-ai-api
Ai api for google meets transcribe/audio/saving

This project can be installed with the following commands

```commandline
docker build -t gm-ai-api .
```

```commandline
docker run -d -p 8020:8020 gm-ai-api
```

Once a meet key has been established and a session properly introduced,
a new websocket connection can be made with /ws:{meet_key}

testing out the poc can be done by running client_poc_test.py

```commandline
python3 client_poc_test.py
```

contributors:
-josh shevchuck
-michael baart
-george spake