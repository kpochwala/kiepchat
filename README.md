### Kiepchat

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r ./requirements.txt
```

Run listener first

optional argument: `--chat_file path/to/chat/file.json`
```
python listener.py
```

Then send message

optional argument: `--chat_file path/to/chat/file.json`
optional argument: `--message "kiep?"`

```
python kiep.py
```
