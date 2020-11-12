"""
Fixed XOR

Write a function that takes two equal-length buffers and produces their XOR
combination.

If your function works properly, then when you feed it the string:

1c0111001f010100061a024b53535009181c

... after hex decoding, and when XOR'd against:

686974207468652062756c6c277320657965

... should produce:

746865206b696420646f6e277420706c6179
"""

import base64


def fixed_xor(buf1: bytes, buf2: bytes) -> bytes:
    dec_buf1 = base64.b16decode(buf1, True)
    dec_buf2 = base64.b16decode(buf2, True)

    return base64.b16encode(bytes([dec_buf1[i] ^ dec_buf2[i] for i in range(len(dec_buf1))]))
