class Byte:
    byte_ = ''

    def set_byte(self, data):
        self.byte_ = data

    def get_byte(self):
        return self.byte_


class Word:
    word_ = []

    def __init__(self, byte_count):
        self.word_ = [Byte() for x in range(0, byte_count)]

    # takes in a list of bytes and saves them to the word list
    def set_word(self, data):
        self.word_.clear()
        counter = 0

        if len(data) != len(self.word_):
            pass

        for byte in self.word_:
            byte.set_byte(data[counter])
            counter += 1

    # returns a list of the bytes
    def get_bytes(self):
        read = []
        for byte in self.word_:
            read.append(byte.get_byte())

        return read

class Block:
    def __init__(self, block_number, words_pblock, bytes_pword):
        self.words_ = []
        self.tag_ = block_number
        self.valid_ = 0
        self.timer_ = 0
        self.words_pblock_ = words_pblock
        self.bytes_pword_ = bytes_pword
        self.create_block()

    def create_block(self):
        self.words_ = [Word(self.bytes_pword_) for x in range(0, self.words_pblock_)]

    # mapping code
    def set_tag(self, tag):
        self.tag_ = tag

    def get_tag(self):
        return self.tag_

    def set_valid(self, valid):
        self.valid_ = valid

    def get_valid(self):
        return self.valid_

    # data code
    def set_word(self, offset, data):
        self.words_[offset].set_word(data)

    def get_word(self, offset):
        return self.words_[offset]

    def get_bytes(self, offset):
        return self.words_[offset].get_bytes()

    # timer code
    def reset_timer(self):
        self.timer_ = 0

    def increment_timer(self):
        self.timer_ += 1

    def get_timer(self):
        return self.timer_


class Set:
    def __init__(self, set_number, block_number, blocks_pset, words_pblock, bytes_pword):
        self.block_table_ = []
        self.set_index_ = set_number
        self.block_number_ = block_number
        self.blocks_pset_ = blocks_pset
        self.words_pblock_ = words_pblock
        self.bytes_pword_ = bytes_pword

        self.create_set()

    def create_set(self):
        for x in range(self.block_number_, (self.block_number+self.blocks_pset_)):
            self.block_table_.append(Block(x, self.words_pblock_, self.bytes_pword_))

    def get_set_index(self):
        return self.set_index_

    def increment_timers(self):
        if len(self.block_table_) > 0:
            for x in self.block_table_:
                x.increment_timer()


class Sets:
    def __init__(self, set_count, blocks_pset, words_pblock, bytes_pword):
        self.set_count_ = set_count
        self.blocks_pset_ = blocks_pset
        self.words_pblock_ = words_pblock
        self.bytes_pword_ = bytes_pword
        self.block_number_ = 0
        self.set_table_ = []
        create_set_table()

    def create_set_table(self):
        for x in range(0, self.set_count_):
            self.set_table_.append(Set(x, self.block_number_, self.blocks_pset_, self.words_pblock_, self.bytes_pword_))
            self.block_number_ = self.block_number_ + self.blocks_pset_  # update block number for the next set

    def read_block(self, tag, index, offset):
        full_set = True
        result = ""

        if len(self.set_table_) > 0:
            for x in range(0, len(self.set_table_)):
                x.increment_timers()
                if x.get_set_index == index:
                    for y in self.set_table_[x]:
                        if y.get_valid() == 0:
                            full_set = False
                        elif y.get_tag == tag:
                            result = "HIT"
                            data_item = y.get_data
                            y.reset_timer()

            if result == "HIT":
                return result, data_item
            elif full_set is False:
                return "MISS", None
            else:
                return "REPLACE", None

    def write_block(self, tag, index, offset, data):
        full_set = True
        result = ""

        if len(self.set_table_) > 0:
            for set_item in self.set_table_:
                # increment the timer for each item
                set_item.increment_timers()
                # if the valid bit is false, then the block is not full
                # and the loop can move on to the next item
                if set_item.get_set_index == index:
                    for block_item in self.set_table_[x]:
                        if block_item.get_valid() == 0:
                            full_set = False
                        elif block_item.get_tag == tag:
                            result = "HIT"
                            block_item.set_word(offset, data)
                            block_item.reset_timer()

            if result == "" and full_set is True:
                return "REPLACE"
            elif result == "":
                return "MISS"

            return result