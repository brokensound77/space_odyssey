#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
from string import printable
import random

parser = argparse.ArgumentParser(description='encode secret in the characters of a message (light stego)')
parser.add_argument('-i', '--in-text', description='message to use to hide secret')
parser.add_argument('-s', '--secret', description='the secret message')
parser.add_argument('-d', '--decode', action='store_true', description='decode using a code and the original message')
parser.add_argument('-c', '--code', description='the code provided from the encoding')
args = parser.parse_args()


def encode_secret(intext, secret):
    letter_catalog = {}

    for letter in printable:
        letter_catalog[letter] = []

    count = 0
    for letter in intext:
        try:
            letter_catalog[letter].append(count)
        except KeyError:
            # character outside of 'printable' range
            pass
        count += 1

    secret_code = ''
    secret_code_letter_lengths = ''

    for letter in secret:
        letter_locations = letter_catalog.get(letter)
        # TODO: come up with a better solution; perhaps obvious substitution and verbose reporting to user
        # no letter present in the catalog
        if len(letter_locations) == 0:
            #letter_locations = None
            print 'Error! "{0}" does not occur in the text snippet provided'.format(letter)
            exit(2)
        this_letter_location = str(random.choice(letter_locations))
        secret_code += this_letter_location
        secret_code_letter_lengths += str(len(this_letter_location))

    return '{0}:{1}'.format(secret_code, secret_code_letter_lengths)


def decode_secret(intext, code):
    code_loc, code_len = code.split(':')
    each_locs = []
    total_len = 0
    for each_len in code_len:
        each_locs.append(code_loc[total_len:int(each_len) + total_len])
        total_len += int(each_len)

    decoded_message = ''

    for this_len in each_locs:
        decoded_message += intext[int(this_len)]

    return decoded_message


if __name__ == '__main__':
    if args.decode:
        if not args.code:
            print 'You must provide a code (-c) to decode with!'
            exit(2)
        print decode_secret(args.in_text, args.code)
    else:
        if not args.secret:
            print 'You must provide a secret (-s) to encode!'
            exit(2)
        print encode_secret(args.in_text, args.secret)
