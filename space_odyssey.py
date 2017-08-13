#!/usr/bin/env python

import re


import argparse


def set_args():

    ##
    # decode
    # encode    default

    # message
    #   stdin   default
    #   file

    # text
    #   stdin   default
    #   file

    # output
    #   stdout  default
    #   file

    # args
    parser = argparse.ArgumentParser()
    # stdout (default), outfile, stdin, infile, encode (default), decode
    # true               str      true   str            mutual ex group

    parser.add_argument('-d', '--decode', action='store_true', help='encodes message in whitespace of text')

    group1 = parser.add_mutually_exclusive_group(required=True)
    group1.add_argument('-sm', '--secret-message', type=str, help='message to be secretly hidden in the text')
    group1.add_argument('-sf', '--secret-file', type=str, help='message from file to be secretly hidden in the text')



    in_group = parser.add_mutually_exclusive_group()
    #in_group.add_argument('text', type=str, help='text from stdin to be encoded with hidden message')
    #in_group.add_argument('-i', '--infile', type=str, help='read from the selected file rather than from stdin')
    out_group = parser.add_mutually_exclusive_group()
    out_group.add_argument("-v", "--verbose", action="store_true")

    #parser.add_argument('-d', '--decode', action='store_true', help='decodes a space encoded document')
    parser.add_argument('-o', '--outfile', type=str, help='write output to the selected file, rather than to stdout')




    parser.add_argument('-a', '--alerts', action='store_true', help='retrieves new alerts')
    parser.add_argument('-s', '--systems', action='count', default=0,
                        help='retrieves systems information; ss for FULL details in JSON (NOISY!)')
    parser.add_argument('-i', '--instance', type=str, help='cid for specific customer instance')
    parser.add_argument('-c', '--config-file', type=str, help='select a config file with user credentials')
    parser.add_argument('-l', '--loop', type=int, choices=[1,2,3,4,5,6,7,8,9,10,11,12],
                        help='runs toruk in a loop, for the number of hours passed')
    parser.add_argument('-f', '--frequency', type=int, default=1, help='frequency (in minutes) for the loop to resume')
    parser.add_argument('-q', '--quiet', action='store_true', help='suppresses errors from alert retrieval failures')
    args = parser.parse_args()


# from https://stackoverflow.com/questions/7396849/convert-binary-to-ascii-and-vice-versa
def string2bits(s=''):
    return [bin(ord(x))[2:].zfill(8) for x in s]


def bits2string(b=None):
    return ''.join([chr(int(x, 2)) for x in b])


def set_secret(secret, text):
    lines = text.split()
    lines.reverse()
    print 'Number of letters: {0}\nNumber of spaces needed: {1}\nNumber of possible spaces: {2}'.format(
            len(secret), len(secret) * 8, len(lines) - 1)
    if len(lines) - 1 < len(secret) * 8:
        raise Exception('Secret is too long for the text provided')
    bin_secret = string2bits(secret)
    encoded_message = ''
    count = 0
    for letter in bin_secret:
        for bit in letter:
            if int(bit) == 0:
                encoded_message += lines.pop() + ' '
            elif int(bit) == 1:
                encoded_message += lines.pop() + '  '
        count += 1
    return encoded_message

y = set_secret('hi', 'Its alright to tell me what you think about me. I wont try to argue or hold it against you, I know that youre leaving')
print y


def get_secret(text):
    raw_space = re.findall('\s{1,2}', text)
    #raw_space_count = map(len, raw_space)
    raw_bits = map(lambda z: str(len(z)-1), raw_space)
    bits_list = []
    for i in xrange(len(raw_bits) / 8):
        tmp = (i + 1) * 8
        bits_list.append(''.join(raw_bits[tmp - 8:tmp]))
    return bits2string(bits_list)

print get_secret(y)