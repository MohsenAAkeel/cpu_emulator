import math
# from cache import *

byte_count_ = int('4')
block_count_ = 4
set_count_ = 2
index_size_ = math.log2(set_count_)
offset_size_ = math.log2(byte_count_)
tag_size_ = 16 - offset_size_ - index_size_
cache_table_ = {}
addy = '1001010001010011'
tag = ''
index = ''
offset = ''

#print(tag_size_)
#print(index_size_)
#print(offset_size_)

for x in range(0, 15):
    if x < tag_size_:
        tag += addy[x]
    elif x >= tag_size_ and x < tag_size_ + index_size_:
        index += addy[x]
    elif x >= tag_size_ + index_size_:
        offset += addy[x]

#print(tag + '\n')
#print(index + '\n')
#print(offset)

#print(int(addy, 2))



class Test:
    def run(self):
        print('worked')

listvar = []

for x in range(0, 2):
    listvar.append(Test())
    listvar[x].run()

cache_size_ = int(64000)
block_size_ = int(2)
nway_set_ = int(16)

# calculate the number of blocks
total_blocks_ = cache_size_/block_size_
set_count_ = math.floor(total_blocks_/nway_set_)

# calculate bit indices for markers
offset_size_ = math.floor(math.log2(block_size_))
index_size_ = math.floor(math.log2(set_count_))
tag_size_ = 32 - offset_size_ - index_size_

print(offset_size_, index_size_, tag_size_)

tag_bin = ''
index_bin = ''
offset_bin = ''
address = '10010110100101101110010011100100'


# parse the binary string for tag, index, and offset
for x in range (0, 32):
    if x < tag_size_:
        tag_bin += address[x]
    elif x >= tag_size_ and x < tag_size_ + index_size_:
        index_bin += address[x]
    elif x >= tag_size_ + index_size_:
        offset_bin += address[x]

# convert binary values to decimal values
tag = int(tag_bin, 2)
index = int(index_bin, 2)
offset = int(offset_bin, 2)

# print(tag, tag_bin)
# print(index, index_bin)
# print(offset, offset_bin)

a = [Test(), Test()]
a[0].run()
a = ["10001111", '01010101', '01110000']
# print(''.join(a))

count = 4

list = [Test() for x in range(0, count)]

print(list)