#!/usr/bin/env python3

"""BIP-39 Mnemonic Generator.

Prints mnemonic and seed hex to stdout on one line each respectively."""

import hashlib
import argparse
import sys, termios, time, tty, random
from mnemonic import Mnemonic

def get_hw_rng_entropy(size):
    """Fetch entropy from /dev/hwrng or /dev/random."""
    try:
        with open("/dev/hwrng", "rb") as f:
            return f.read(size // 8)
    except:
        with open("/dev/random", "rb") as f:
            return f.read(size // 8)


def get_user_entropy(entropy, size):
    """Get user input and hash it to derive entropy."""
    return hashlib.sha256(entropy.encode()).digest()[: size // 8]


def get_keyboard_entropy(size):
    """Get keyboard keystrokes and timing as entropy."""
    print(f"Type random keys\n", end="", flush=True)
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    timings = []
    chars = []
    last_time = time.time()

    try:
        tty.setraw(fd)
        new_settings = termios.tcgetattr(fd)
        new_settings[3] = new_settings[3] & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)

        for _ in range(size // 8):
            current_time = time.time()
            # Randomly throw out some characters
            char = sys.stdin.read(1)
            while random.random() < 0.5:
                char = sys.stdin.read(1)
            chars.append(char)
            timings.append(current_time - last_time)
            last_time = current_time
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    # Combine both character and timing data for entropy
    combined = ''.join(chars).encode() + b''.join(str(t).encode() for t in timings)
    return hashlib.sha256(combined).digest()[: size // 8]

def get_mnemonic_and_seed(entropy_size, language, user_entropy, keyboard_entropy, passphrase):
    # Generate entropy
    hw_rng_entropy = get_hw_rng_entropy(entropy_size)
    entropy = bytearray(hw_rng_entropy)

    if user_entropy:
        user_entropy = get_user_entropy(user_entropy, entropy_size)
        entropy = bytes(a ^ b for a, b in zip(entropy, user_entropy))

    if keyboard_entropy:
        keyboard_entropy = get_keyboard_entropy(entropy_size)
        entropy = bytes(a ^ b for a, b in zip(entropy, keyboard_entropy))

    # Generate mnemonic and seed

    mnemo = Mnemonic(language)
    mnemonic = mnemo.to_mnemonic(entropy)
    seed = mnemo.to_seed(mnemonic, passphrase=passphrase).hex()

    return mnemonic, seed


def main():
    parser = argparse.ArgumentParser(description="BIP39 Mnemonic Generator")
    parser.add_argument(
        "-e",
        "--entropy-size",
        choices=[128, 256],
        type=int,
        default=128,
        help="Number of entropy bits (128 or 256). Default: 128",
    )
    parser.add_argument(
        "-l",
        "--language",
        default="english",
        help="Language for mnemonic words (default: english, available: english, chinese_simplified, chinese_traditional, french, italian, japanese, korean, spanish, turkish, czech, portuguese)",
    )
    parser.add_argument(
        "-u",
        "--user-entropy",
        default="",
        help="Include user input as additional entropy (as string enclosed in 'single quotes')",
    )
    parser.add_argument(
        "-k",
        "--keyboard-entropy",
        action="store_true",
        help="Use keyboard keystrokes (keys pressed as well as timing) as additional entropy",
    )
    parser.add_argument(
        "-p",
        "--passphrase",
        default="",
        help="Optional BIP-39 passphrase for mnemonic seed (as string enclosed in 'single quotes')",
    )

    args = parser.parse_args()
    mnemonic, seed = get_mnemonic_and_seed(args.entropy_size, args.language, args.user_entropy, args.keyboard_entropy, args.passphrase)

    # Output format: First line is mnemonic, second line is seed hex
    print(mnemonic)
    print(seed)


if __name__ == "__main__":
    main()

