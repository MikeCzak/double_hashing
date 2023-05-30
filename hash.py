class HashEntry:
    """
    Wrapper class for hash table entries.
    """
    def __init__(self, key: int, value: object) -> None:
        """
        Constructor for hash table entries.
        :param key: key of hash table entry
        :param value: value of hash table entry
        :return: None
        """
        self.key = key
        self.value = value

    def delete(self) -> None:
        """
        Delete the hash table entry content.
        :return: None
        """
        self.key = None
        self.value = None

    def __str__(self) -> str:
        """
        The string representation for the object is the string representation of the key.
        :return: String representation of key
        """
        return f"{self.key}"


class HashTable:
    """
    Implementation of a hash table based on Open Hashing.
    A hash entries is wrapped in a HashEntry object before being put into the list that represents the hash table:
    -  If the hash table entry is None, the entry is empty
    -  If the hash table contains a HashEntry wrapper object with a None key and value attributes, the entry is "free",
      meaning there was data that has already been deleted
    -  If the hash table contains a HashEntry wrapper object with a valid key and value attributes, the hash table entry
      is in use
    Attributes:
        table: list of HashEntry or None objects
    """
    table: []

    def __init__(self, size: int):
        """
        Initialize a hash table with a given size.
        :param size: hash table size, maximum number of elements that may be stored in the hash table
        :return: None
        """
        self.table = [None] * size
        self.size = size

    def insert(self, key: int, value: object) -> int:
        """
        Insert the given key/value entry into the hash table using double hashing (without Brent).
        :param key: the key that identifies the entry and that is used for the hash function
        :param value: value to insert with the key into the hash table
        :return: table index where the value was successfully inserted, or -1 if table is full or an entry with the
        same key already exists within the table
        """
        # Begin implementation
        for i in range(len(self.table)):
            key_double_hash = self.get_double_hash_value(self.get_hash_value(key), key, i)
            if self.is_free(key_double_hash):
                self.set_key_value(key_double_hash, key, value)
                return key_double_hash
            else:
                if self.table[key_double_hash].key == key:
                    break
        return -1
        # End implementation

    def insert_brent(self, key: int, value: object) -> int:
        """
        Insert a given key/value entry into the hash table using double hashing with Brent.
        :param key: the key that identifies the entry and that is used for the hash function
        :param value: value to insert with the key into the hash table
        :return: table index where the object was successfully inserted, or -1 if table is full or an entry with the
        same key already exists within the table
        """
        # Begin implementation
        for i in range(len(self.table)):
            key_double_hash = self.get_double_hash_value(self.get_hash_value(key), key, i)
            if self.is_free(key_double_hash):
                self.set_key_value(key_double_hash, key, value)
                return key_double_hash
            else:
                if self.table[key_double_hash].key == key:
                    break
                if i == 0:
                    continue
            index_of_existing_key = self.get_double_hash_value(self.get_hash_value(key), key, i - 1)
            existing_key_double_hash = self.get_double_hash_value(index_of_existing_key, self.table[index_of_existing_key].key, 1)
            if self.is_free(existing_key_double_hash):
                self.set_key_value(existing_key_double_hash, self.table[index_of_existing_key].key, self.table[index_of_existing_key].value)
                self.set_key_value(index_of_existing_key, key, value)
                return index_of_existing_key
        return -1
        # End implementation

    def retrieve(self, key: int) -> object:
        """
        Retrieve the key in the hash table and return the value object.
        :param key: the key that identifying the entry
        :return: value object if the was found in the hash table, None otherwise
        """
        # Begin implementation
        for i in range(self.size):
            hash_value = self.get_double_hash_value(self.get_hash_value(key), key, i)
            if self.table[hash_value] is None:
                return None
            if self.table[hash_value].key == key:
                return f"{self.table[hash_value]}"
        return None
        # End implementation

    def delete(self, key: int) -> int:
        """
        Delete an entry from the hash table.
        :param key: key identifying the hash table entry
        :return: table index where the key was found and deleted, or -1 if the key was not found
        """
        # Begin implementation
        for i in range(self.size):
            hash_value = self.get_double_hash_value(self.get_hash_value(key), key, i)
            if self.table[hash_value] is None:
                return -1
            if self.table[hash_value].key == key:
                self.table[hash_value].key = None
                self.table[hash_value].value = None
                return hash_value
        return -1
        # End implementation

    def set_key_value(self, index: int, key: int, value: object):
        """
        Set a key/value entry in the hash table at the given index
        :param index: index in hash table
        :param key: key to set
        :param value: value to set
        :return:
        """
        if self.is_empty(index):
            # insert new HashEntry object at position index
            self.table[index] = HashEntry(key, value)
        else:
            # re-use existing HashEntry object
            self.table[index].key = key
            self.table[index].value = value

    def is_empty(self, index: int) -> bool:
        """
        Check if a given table index is empty, i.e. it contains None instead of a HashEntry object
        @param index: index in hash table to check
        @return: True if the table contains None at the given index, False otherwise
        """
        # check if table index is empty
        if self.table[index] is None:
            return True
        else:
            return False

    def is_free(self, index: int) -> bool:
        """
        Check if a given table index is free, i.e. either empty or it contains a deleted entry
        :param index:
        :return: True if the table index may be used for inserting, False otherwise
        """
        # If table index is empty it is free
        if self.is_empty(index):
            return True
        # If it contains a deleted entry it is also free
        if self.table[index].key is None:
            return True
        else:
            return False

    # Add your auxiliary methods here
    # Begin implementation

    def get_hash_value(self, key):
        hash_value = key % self.size
        return hash_value

    def get_double_hash_value(self, hash_value, key, j):
        double_hash_value = (hash_value - j * (1 + (key % (self.size - 2)))) % self.size
        return double_hash_value
    # End implementation
