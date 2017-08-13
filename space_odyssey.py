#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


import argparse



# args
parser = argparse.ArgumentParser(description='encode message in whitespace of the message\n'
                                             '')
parser.add_argument('-d', '--decode', action='store_true', help='decodes message from whitespace of message')
parser.add_argument('-o', '--outfile', type=str, help='write output to the selected file, rather than to stdout')

group1 = parser.add_mutually_exclusive_group()
group1.add_argument('-s', '--secret', type=str, help='secret to be hidden in the message')
group1.add_argument('-sf', '--secret-file', type=str, help='secret text from file to be hidden in the message')

group2 = parser.add_mutually_exclusive_group(required=True)
group2.add_argument('-t', '--message', type=str, help='message where secret will be hidden via whitespace')
group2.add_argument('-tf', '--message-file', type=str,
                    help='message text from file where secret will be hidden via whitespace')
args = parser.parse_args()



# from https://stackoverflow.com/questions/7396849/convert-binary-to-ascii-and-vice-versa
def string2bits(s=''):
    return [bin(ord(x))[2:].zfill(8) for x in s]


# from https://stackoverflow.com/questions/7396849/convert-binary-to-ascii-and-vice-versa
def bits2string(b=None):
    return ''.join([chr(int(x, 2)) for x in b])


def set_secret(secret, text):
    """
    :param secret: the message to be hidden
    :param text: the text to hide the message in
    :return: the white-space encoded message
    """
    lines = text.split()
    lines.reverse()
    # checks to ensure that there are enough potential white spaces for the message in binary
    if len(lines) - 1 < len(secret) * 8:
        raise Exception('Secret is too long for the text provided')
    bin_secret = string2bits(secret)
    encoded_message = ''
    for letter in bin_secret:
        for bit in letter:
            if int(bit) == 0:
                # zero represented by single space
                encoded_message += lines.pop() + ' '
            elif int(bit) == 1:
                # one represented by double space
                encoded_message += lines.pop() + '  '
    lines.reverse()
    # concatenate the remainder of the original message
    encoded_message += ' '.join(lines)
    return encoded_message


def get_secret(text):
    """
    :param text: the white-space encoded message
    :return: the secret message
    """
    # make a list of all of the white space 1-2 wide
    raw_space = re.findall('\s{1,2}', text)
    # decrement them all by 1 (to represent binary)
    raw_bits = map(lambda z: str(len(z)-1), raw_space)
    # assemble a new list consisting of lists 8 wide (byte)
    bits_list = []
    for i in xrange(len(raw_bits) / 8):
        tmp = (i + 1) * 8
        bits_list.append(''.join(raw_bits[tmp - 8:tmp]))
    return bits2string(bits_list)


def space_secret():
    if args.message is not None:
        local_message = args.message
    else:
        with open(args.message_file, 'rb') as f:
            local_message = f.read()

    # decode
    if args.decode:
        if args.outfile is not None:
            with open(args.outfile, 'wb') as f:
                f.write(get_secret(local_message))
        else:
            print get_secret(local_message)
    else:
        # encoode
        if args.secret is not None:
            local_secret = args.secret
        else:
            with open(args.secret_file, 'rb') as f:
                local_secret = f.read()
        if args.outfile is not None:
            with open(args.outfile, 'wb') as f:
                try:
                    f.write(set_secret(local_secret, local_message))
                except Exception as e:
                    print 'There was an error: {0}'.format(e)
                    exit(2)
        else:
            print 'Number of letters: {0}\nNumber of spaces needed: {1}\nNumber of possible spaces: {2}'.format(
                len(local_secret), len(local_secret) * 8, len(local_message.split()) - 1)
            try:
                print set_secret(local_secret, local_message)
            except Exception as e:
                print 'There was an error: {0}'.format(e)
                exit(2)

space_secret()
