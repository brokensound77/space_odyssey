# space_odyssey

## usage

```
usage: space_odyssey.py [-h] [-d] [-o OUTFILE] [-s SECRET | -sf SECRET_FILE]
                        (-t MESSAGE | -tf MESSAGE_FILE)

encode message in whitespace of the message

optional arguments:
  -h, --help            show this help message and exit
  -d, --decode          decodes message from whitespace of message
  -o OUTFILE, --outfile OUTFILE
                        write output to the selected file, rather than to
                        stdout
  -s SECRET, --secret SECRET
                        secret to be hidden in the message
  -sf SECRET_FILE, --secret-file SECRET_FILE
                        secret text from file to be hidden in the message
  -t MESSAGE, --message MESSAGE
                        message where secret will be hidden via whitespace
  -tf MESSAGE_FILE, --message-file MESSAGE_FILE
                        message text from file where secret will be hidden via
                        whitespace
```

# message_scrambler

## usage

```
usage: message_scrambler.py [-h] [-i IN_TEXT] [-s SECRET] [-d] [-c CODE]

encode secret in the characters of a message (light stego)

optional arguments:
  -h, --help            show this help message and exit
  -i IN_TEXT, --in-text IN_TEXT
                        message to use to hide secret
  -s SECRET, --secret SECRET
                        the secret message
  -d, --decode          decode using a code and the original message
  -c CODE, --code CODE  the code provided from the encoding
```