
from hashlib import new


class SpellMaster:
    global CODEWORDSIZE
    global WORDBUFSIZE 

    CODEWORDSIZE = 8
    WORDBUFSIZE = 26

    def __init__(self):
        self.code_word = "FRANKLIN"
        self.encode_xlate_table = [7, 14, 22, 0,
                                    0, 0, 0, 0,
                                    0, 0, 0, 0,
                                    0, 0, 0, 0,
                                    0, 0, 0, 0,
                                    0, 0, 0, 0,
                                    0, 0, 0, 0]

        self.decode_xlate_table = [4, 0, 0, 0,
                                    0, 0, 0, 0,
                                    0, 0, 0, 2,
                                    0, 1, 0, 0,
                                    0, 0, 0, 0,
                                    0, 0, 0, 0,
                                    0, 0, 0, 0]
        self.special_idx = [2, 3, 7, 10, 15, 18, 20, 21,23]
        self.special_dict = {2: 5,
                            3: 25,
                            7: 17,
                            10: 13,
                            15: 21,
                            18: 18,
                            20: 17,
                            21: 5,
                            23: 13}
        
    def store_code_word(self, code_word):
        length = len(code_word)
        j = 0

        new_code_word = ''
        for i in range(CODEWORDSIZE):
            new_code_word += code_word[j]
            j += 1
            if j >=length: j = 0
        self.code_word = new_code_word

    def encode_xlate(self, val):
        return(self.encode_xlate_table[val])
    
    def decode_xlate(self, val):
        return(self.decode_xlate_table[val])
        
    def do_cipher(self, do_decode_flag, in_text):
        length = len(in_text)
        if length > WORDBUFSIZE:
            print("Error: Input text too long!\n")
            return -1

        # Convert input text to 0-27 range
        if ~do_decode_flag:
            word_buf = [self.encode_xlate(ord(char)-ord('A')) for char in in_text]
        else:
            word_buf = [ord(char)-ord('A') for char in in_text]

        # print(word_buf)
        # Take a copy of the key
        tempcode = [ord(char) for char in self.code_word]
        
        # Initialize working word
        work_word = [None]*length
        # Encrypt or decrypt the text
        for i in range(length):
            key = 0
            for j in range(CODEWORDSIZE):
                key += tempcode[j] - ord('A')
            
            key = key % 28 # key mod 28, vs 26 in reference code
            # print('Key: {}'.format(key))
            # Apply key
            work_word[i] =  (key - word_buf[i]) % 28
            # print('P: {}'.format(word_buf[i]))
            # print('W: {}'.format(work_word[i]))
            # Modify key
            if i in self.special_idx:
                key = self.special_dict[i]
            else:
                if ~do_decode_flag:
                    key = (key + word_buf[i]) % 28
                else:
                    key = (key + work_word[i]) % 28
            # if ~do_decode_flag:

            #     key = ((key + word_buf[i]) % 28 )
            # else:
            #     key = (key + work_word[i]) % 27
            
            for i in range(CODEWORDSIZE-1):
                tempcode[i] = tempcode[i+1]
            tempcode[CODEWORDSIZE-1] = key
            # print('Mod key: {}'.format(key))
        # Convert result back to ASCII range
        for i in range(length):
            if ~do_decode_flag:
                work_word[i] += ord('A')
            else:
                work_word[i] = self.decode_xlate(work_word[i]+ord('A'))
            
        print([chr(num) for num in work_word])

    def encode_word(self, text):
        self.do_cipher(0, text)

    def decode_word(self, text):
        print(self.do_cipher(1, text))
        

if __name__ == '__main__':
    sm = SpellMaster()
    sm.store_code_word('AAAA')
    sm.encode_word('AAAAAAAAAA')
    sm.encode_word('BBBBBBBBBBBBBBBBBBBBBBBBB')
    sm.encode_word('ABCDEFGHIJKLMNOPQRSTUVWXY')
    sm.encode_word('BCDEFGHIJKLMNOPQRSTUVWXYZ')
    sm.encode_word('CDEFGHIJKLMNOPQRSTUVWXYZA')
    sm.encode_word('DEFGHIJKLMNOPQRSTUVWXYZAB')

    # sm.store_code_word('B')
    # sm.
    # sm.encode_word('IS-SPELLMASTER-ALIVE?')

    # sm.store_code_word('CATS')
    # sm.encode_word('DOGSDOGSDOGSDOGS')

    # sm.store_code_word('CAT')
    # sm.encode_word('DOGSDOGSDOGSDOGS')