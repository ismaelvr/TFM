import binascii
import unittest
import hashlib
from ddt import ddt, data
import algorithms.blake2 as b2

@ddt
class TestBlake2(unittest.TestCase):

    @data("Hash_test")
    def test_hashes_are_equal(self, value):
        # Hash with oficial library
        original_hash = hashlib.blake2b(value.encode('utf8')).hexdigest()

        #Hash with own implementation
        self.b2 = b2.BLAKE2b(digest_size=64, debug = True)
        self.b2.update(value.encode('utf8'))
        digest = self.b2.final()
        own_hash = binascii.hexlify(digest).decode()

        self.assertEqual(original_hash, own_hash)

if __name__=='__main__':
    unittest.main(verbosity=2)