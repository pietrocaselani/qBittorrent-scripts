import unittest
from qbt_utils import has_all_tags, has_any_tags

class MockTorrent:
    def __init__(self, tags):
        self.tags = tags

class TestQbtUtils(unittest.TestCase):
    def test_has_all_tags_single(self):
        torrent = MockTorrent(tags='tag1, tag2, tag3')
        self.assertTrue(has_all_tags(torrent, 'tag1'))
        self.assertFalse(has_all_tags(torrent, 'tag4'))

    def test_has_all_tags_multiple(self):
        torrent = MockTorrent(tags='tag1, tag2, tag3')
        self.assertTrue(has_all_tags(torrent, 'tag1', 'tag2'))
        self.assertFalse(has_all_tags(torrent, 'tag1', 'tag4'))

    def test_has_any_tags_multiple(self):
        torrent = MockTorrent(tags='tag1, tag2, tag3')
        self.assertTrue(has_any_tags(torrent, 'tag1', 'tag2'))
        self.assertTrue(has_any_tags(torrent, 'tag1', 'tag4'))
        self.assertFalse(has_any_tags(torrent, 'tag4', 'tag5'))

if __name__ == '__main__':
    unittest.main()