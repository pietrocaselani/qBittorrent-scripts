import unittest
from qbt_utils import has_all_tags, has_any_tags, is_torrent_really_private, PRIVATE_TAG, NO_PRIVATE_TAG

class MockTorrent:
    def __init__(self, tags="", private=False):
        self.tags = tags
        self.private = private

class TestQbtUtils(unittest.TestCase):
    TAGS_1_2_3 = 'tag1, tag2, tag3'

    def test_has_all_tags_single(self):
        torrent = MockTorrent(tags=self.TAGS_1_2_3)
        self.assertTrue(has_all_tags(torrent, 'tag1'))
        self.assertFalse(has_all_tags(torrent, 'tag4'))

    def test_has_all_tags_multiple(self):
        torrent = MockTorrent(tags=self.TAGS_1_2_3)
        self.assertTrue(has_all_tags(torrent, 'tag1', 'tag2'))
        self.assertFalse(has_all_tags(torrent, 'tag1', 'tag4'))

    def test_has_any_tags_multiple(self):
        torrent = MockTorrent(tags=self.TAGS_1_2_3)
        self.assertTrue(has_any_tags(torrent, 'tag1', 'tag2'))
        self.assertTrue(has_any_tags(torrent, 'tag1', 'tag4'))
        self.assertFalse(has_any_tags(torrent, 'tag4', 'tag5'))

    def test_private_torrents(self):
        # All valid permutations of tags and private flag
        permutations = [
            ("", False, False),
            ("", True, False),
            (PRIVATE_TAG, False, True),
            (PRIVATE_TAG, True, True),
            (NO_PRIVATE_TAG, False, False),
            (NO_PRIVATE_TAG, True, False),
        ]

        for tags, private, expected in permutations:
            with self.subTest(tags=tags, private=private):
                torrent = MockTorrent(tags=tags, private=private)
                self.assertEqual(is_torrent_really_private(torrent), expected)

if __name__ == '__main__':
    unittest.main()