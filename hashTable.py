#Creating hash table
class MyHashTable:
    def __init__(self, initial_capacity=10):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

        self.table.append([])

    # Inserts new item into the hash table.
    def insert(self, key, item):  # does both insertion and update
        # get the bucket list where this item will go.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # update key if it is already in the bucket
        for ky in bucket_list:
            # print (key_value)
            if ky[0] == key:
                ky[1] = item
                return True

        # if not, insert the item to the end of the bucket list.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    def lookup(self, key):
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # print(bucket_list)

        # search for the key in the bucket list
        for ky in bucket_list:
            # print (key_value)
            if ky[0] == key:
                return ky[1]  # value
        return None

    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # remove the item from the bucket list if it is present.
        for ky in bucket_list:
            # print (key_value)
            if ky[0] == key:
                bucket_list.remove([ky[0], ky[1]])