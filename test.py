from main import sbox, byte_substitution, rotation, xor, galois28, rcon

def main():
    # col = [219, 19, 83, 69]
    # col2 = [242, 10, 34, 92]
    # col3 = [1, 1, 1, 1]
    # col4 = [198, 198, 198, 198]
    # col5 = [212, 212, 212, 213]
    # col6 = [45, 38, 49, 76]
    #
    # col7 = [212, 224, 184, 30]
    # print(mix_column(col))
    # print(mix_column(col2))
    # print(mix_column(col3))
    # print(mix_column(col4))
    # print(mix_column(col5))
    # print(mix_column(col6))
    # state = mix_column(col7)
    # print([hex(i) for i in state])
    key = "2B7E151628AED2A6ABF7158809CF4F3C"
    exp_keys = key_expansion(key)
    for key in exp_keys:
        print([hex(i) for i in key])

def rc(index):
    if index <= 1:
        return 1
    tmp_num = rc(index-1)
    return galois28[tmp_num]

def key_expansion(key) -> list:
    expanded_key = []
    while key:
        expanded_key.append(int(key[0:2], 16))
        key = key[2:]

    round_num = 4
    tmp = [0]*4
    while round_num < 44:
        from_4_rounds_ago = expanded_key[4 * (round_num - 4): 4 * (round_num - 3)]
        prev_round = expanded_key[4 * (round_num-1): 4 * round_num]
        if round_num % 4 == 0:
            prev_round = byte_substitution(rotation(prev_round))
            for i in range(0, 4):
                tmp[i] = xor(from_4_rounds_ago[i], prev_round[i])
            tmp[0] = xor(tmp[0], rc(round_num // 4))
        else:
            for i in range(0, 4):
                tmp[i] = xor(from_4_rounds_ago[i], prev_round[i])
        expanded_key = expanded_key + tmp
        round_num += 1
    return [expanded_key[i: i+16] for i in range(0, len(expanded_key), 16)]


def mix_column(col):
    tmp_col = [0]*4
    tmp_col[0] = mult(2, col[0]) ^ mult(3, col[1]) ^ col[2] ^ col[3]
    tmp_col[1] = col[0] ^ mult(2, col[1]) ^ mult(3, col[2]) ^ col[3]
    tmp_col[2] = col[0] ^ col[1] ^ mult(2, col[2]) ^ mult(3, col[3])
    tmp_col[3] = mult(3, col[0]) ^ col[1] ^ col[2] ^ mult(2, col[3])
    return tmp_col


# def mult(num1, num2):  # Galois zmienic na lookup
#     p = 0x00
#     for i in range(0, 8):
#         if (num2 & 1) != 0:
#             p ^= num1
#
#         hi_bit_set = (num1 & 0x80) != 0
#         num1 <<= 1
#         if hi_bit_set:
#             num1 = num1 ^ 0x1b  # x^8 + x^4 + x^3 + x + 1
#         num2 >>= 1
#     return p

def mult(b, a):
    p = 0
    hi_bit_set = 0
    for i in range(8):
        if b & 1 == 1: p ^= a
        hi_bit_set = a & 0x80
        a <<= 1
        if hi_bit_set == 0x80: a ^= 0x1b
        b >>= 1
    return p % 256


if __name__ == '__main__':
    main()