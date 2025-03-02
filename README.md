# bip39-generator
BIP39 Mnemonic Generator with optional user provided and keyboard entropy

Prints mnemonic and seed hex to stdout on one line each respectively.

Example output:
```
joke august travel pledge lobster switch segment middle mean abandon spoon blouse
97498e4d0c34ae17436b71ce3c325dc33a235cc263119c1503ced55cbc3cc05574c6b21e21649d7b022a09aef75744152244bcd3fc6f8db7e25a7df48034e26e
```

# Installation
```
pip install -r requirements.txt
```

# Usage
```
usage: bip39.py [-h] [-e {128,256}] [-l LANGUAGE] [-u USER_ENTROPY] [-k] [-p PASSPHRASE]

BIP39 Mnemonic Generator

options:
  -h, --help            show this help message and exit
  -e, --entropy-size {128,256}
                        Number of entropy bits (128 or 256). Default: 128
  -l, --language LANGUAGE
                        Language for mnemonic words (default: english, available: english, chinese_simplified, chinese_traditional, french, italian, japanese, korean, spanish, turkish, czech, portuguese)
  -u, --user-entropy USER_ENTROPY
                        Include user input as additional entropy (as string enclosed in 'single quotes')
  -k, --keyboard-entropy
                        Use keyboard keystrokes (keys pressed as well as timing) as additional entropy
  -p, --passphrase PASSPHRASE
                        Optional BIP-39 passphrase for mnemonic seed (as string enclosed in 'single quotes')`
```
