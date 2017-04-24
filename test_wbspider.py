import unittest


class TestWeiboSpider(unittest.TestCase):
    def test_login(self):
        from wblogin.login import get_session
        sc = get_session()
        if sc:
            print('登陆成功')
        else:
            raise Exception('登录失败')

    def test_get_timeout(self):
        from config.get_config import get_timeout
        self.assertEqual(get_timeout(), 200)

    def test_getrepostcounts(self):
        from page_parse.wbpage import wbparse
        with open('./tests/reposts_root.html') as f:
            cont = f.read()
            repost_count = wbparse.get_repostcounts(cont)
            self.assertEqual(repost_count, 0)

        with open('./tests/reposts_sub.html') as f:
            cont = f.read()
            repost_count = wbparse.get_repostcounts(cont)
            self.assertEqual(repost_count, 38)

    def test_getcomments(self):
        from page_parse.wbpage import wbparse
        with open('./tests/reposts_root.html') as f:
            cont = f.read()
            repost_count = wbparse.get_commentcounts(cont)
            self.assertEqual(repost_count, 0)

        with open('./tests/reposts_sub.html') as f:
            cont = f.read()
            repost_count = wbparse.get_commentcounts(cont)
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
        # 数据库中存在的数据
        user = get_user('3858873234')
        self.assertEqual(user.get('name'), '景区宝')

        # 数据库中不存在的数据
        user2 = get_user('2674334272')
        self.assertEqual(isinstance(user2, dict), True)

    def test_get_user_from_web(self):
        from wblogin.login import get_session
        from page_get.user import get_profile
        from headers import headers

        user_id = '2674334272'
        sc = get_session()
        if sc:
            session = sc.get('session', '')

            if session:
                # 数据库已有的数据
                user = get_profile(user_id, session, headers)
                self.assertNotEqual(user.description, '')
                # 数据库没有的数据
                user2 = get_profile('3614046244', session, headers)
                self.assertEqual(user2.status_count, 35)
        else:
            raise Exception('模拟登录失败')

