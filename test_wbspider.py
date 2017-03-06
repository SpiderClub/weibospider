import unittest


class TestWeiboSpider(unittest.TestCase):
    def test_getrepostcounts(self):
        from data_process.do_statusprocess import status_parse
        with open('./tests/reposts_root.html') as f:
            cont = f.read()
            repost_count = status_parse.get_repostcounts(cont)
            self.assertEqual(repost_count, 0)

        with open('./tests/reposts_sub.html') as f:
            cont = f.read()
            repost_count = status_parse.get_repostcounts(cont)
            self.assertEqual(repost_count, 38)

    def test_getcomments(self):
        from data_process.do_statusprocess import status_parse
        with open('./tests/reposts_root.html') as f:
            cont = f.read()
            repost_count = status_parse.get_commentcounts(cont)
            self.assertEqual(repost_count, 0)

        with open('./tests/reposts_sub.html') as f:
            cont = f.read()
            repost_count = status_parse.get_commentcounts(cont)
            self.assertEqual(repost_count, 9)

    def test_update_repost_comment(self):
        from db_operation.weibosearch_dao import update_repost_comment, get_repost_comment
        mid = '3791583457149221'
        reposts = 42
        comments = 9
        rs = get_repost_comment(mid)
        self.assertNotEqual(rs, (reposts, comments))
        update_repost_comment(mid=mid, reposts=reposts, comments=comments)
        rs = get_repost_comment(mid)
        self.assertEqual(rs, (reposts, comments))

    def test_get_user_from_db(self):
        from db_operation.user_dao import get_user
        user = get_user('385887323')
        self.assertEqual(user.get('name'), '景区宝')

    def test_get_user_from_web(self):
        from weibo_login import login_info
        session = login_info.get_session().get('session', '')
        if session:
            pass

