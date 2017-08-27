# coding:utf-8
import unittest

import requests

TEST_SERVER = 'https://test.rookiefly.cn/'


# TODO a better TDD is wanted
class TestWeiboSpider(unittest.TestCase):
    def test_get_login_info(self):
        from db import login_info
        infos = login_info.get_login_info()
        self.assertEquals(len(infos), 5)

    def test_login(self):
        import random
        from wblogin.login import get_session
        from db.login_info import get_login_info
        infos = get_login_info()
        if not infos:
            raise Exception('There is no account for login')

        info = random.choice(infos)
        sc = get_session(info.name, info.password)

        if sc:
            print('login successed')
        else:
            raise Exception('login failed')

    def test_freeze_account(self):
        from db import login_info
        login_info.freeze_account('18708103033')
        infos = login_info.get_login_info()
        for info in infos:
            if info[0] == '18708103033':
                self.assertEqual(info.enable, 0)

    def test_delete_cookies(self):
        """
        delete according to key
        """
        from db.redis_db import Cookies
        r = Cookies.delete_cookies('18708103033')
        self.assertEqual(r, True)

    def test_page_get(self):
        """
        test crawling pages
        """
        from page_get import basic
        test_url = 'http://weibo.com/p/1005051764222885/info?mod=pedit_more'
        text = basic.get_page(test_url)
        self.assertIn('深扒娱乐热点', text)

    def test_parse_user_info(self):
        """
        test parsing pages
        """
        from page_parse.user import person, public
        from page_get.user import get_user_detail

        url = TEST_SERVER + 'writer.html'
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        cont = resp.text
        user = person.get_detail(cont)
        user.verify_type = public.get_verifytype(cont)
        self.assertEqual(user.verify_type, 1)
        self.assertEqual(user.description, '韩寒')

        url = TEST_SERVER + 'person.html'
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        cont = resp.text
        user = get_user_detail('222333312', cont)
        self.assertEqual(user.follows_num, 539)

        url = TEST_SERVER + 'excp.html'
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        cont = resp.text
        user = get_user_detail('1854706423', cont)
        self.assertEqual(user.birthday, '1988年2月21日')

    def test_get_url_from_web(self):
        """
        test crawling different kind of users
        """
        from page_get import user as user_get

        normal_user, _ = user_get.get_profile('1195908387')
        self.assertEqual(normal_user.name, '日_推')
        writer, _ = user_get.get_profile('1191258123')
        self.assertEqual(writer.description, '韩寒')
        enterprise_user, _ = user_get.get_profile('1839256234')
        self.assertEqual(enterprise_user.level, 36)

    def test_get_fans(self):
        """
        test parsing fans pages
        """
        from page_parse.user import public
        url = TEST_SERVER + 'fans.html'
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        cont = resp.text
        ids = public.get_fans_or_follows(cont, '2036911095', 1)
        self.assertEqual(len(ids), 9)

    def test_bulk_insert_with_duplicates(self):
        """
        测试批量插入的时候是否会重复插入（请到mysql数据库中查看结果）
        """
        from db.seed_ids import insert_seeds
        ids = ['2891529877', '2891529878', '281296709']
        insert_seeds(ids)

    def test_crawl_person_infos(self):
        """
        test for crawling user infos
        """
        from tasks.user import crawl_person_infos
        crawl_person_infos('2041028560')

    def test_get_search_info(self):
        """
        测试微博搜索结果页面解析功能
        :return: 
        """
        from page_parse import search
        url = TEST_SERVER + 'search.html'
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        cont = resp.text
        infos = search.get_search_info(cont)

        self.assertEqual(len(infos), 20)

    def test_get_keyword(self):
        """
        获取搜索关键词
        :return: 
        """
        from db.search_words import get_search_keywords
        rs = get_search_keywords()
        self.assertEqual(len(rs), 10)

    def test_add_search_cont(self):
        """
        测试批量添加微博信息
        :return: 
        """
        from db.wb_data import insert_weibo_datas
        from page_parse import search
        url = TEST_SERVER + 'search.html'
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        cont = resp.text
        infos = search.get_search_info(cont)
        insert_weibo_datas(infos)

    def test_search_keyword(self):
        """
        test for search
        :return: 
        """
        from tasks.search import search_keyword
        search_keyword('陈羽凡公司发文')

    def test_get_home_page_right(self):
        """
        测试主页右边部分（即微博数据部分）是否可以正常解析
        :return: 
        """
        from page_parse import home
        url = TEST_SERVER + 'enterprisehome.html'
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        html = resp.text
        wbcounts = home.get_wbdata_fromweb(html)
        self.assertEqual(len(wbcounts), 15)

        url = TEST_SERVER + 'personhome.html'
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        html = resp.text
        wbcounts = home.get_wbdata_fromweb(html)
        self.assertEqual(len(wbcounts), 15)

    def test_ajax_home_page_data(self):
        """
        测试通过ajax返回的主页数据是否可以正常解析
        :return: 
        """
        from page_parse import home

        url = TEST_SERVER + 'asyncpersonhome.html'
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        html = resp.text
        datas = home.get_home_wbdata_byajax(html)
        self.assertEqual(len(datas), 15)

    def test_get_total_home_page(self):
        """
        测试获取主页页数
        :return: 
        """
        from page_parse import home

        url = TEST_SERVER + 'asyncpersonhome.html'
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        html = resp.text
        num = home.get_total_page(html)
        self.assertEqual(num, 18)

    def test_parse_comment_page(self):
        """
        测试对评论页的解析
        :return: 
        """
        from page_parse import comment
        url = TEST_SERVER + 'comment.html'
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        html = resp.text
        comment_list = comment.get_comment_list(html, '1123331211')
        self.assertEqual(len(comment_list), 19)

    def test_get_total_comment_page(self):
        """
        测试获取所有评论页数
        :return: 
        """
        from page_parse import comment
        url = TEST_SERVER + 'comment.html'
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        html = resp.text
        total_page = comment.get_total_page(html)
        self.assertEqual(total_page, 227)

    def test_get_total_repost_page(self):
        """
        测试获取所有转发页数
        :return: 
        """
        from page_parse import repost
        url = TEST_SERVER + 'repost.html'
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        html = resp.text
        total_page = repost.get_total_page(html)
        self.assertEqual(total_page, 1580)

    def test_get_total_comment_to_crawl(self):
        from db import wb_data
        weibo_datas = wb_data.get_weibo_comment_not_crawled()
        print(len(weibo_datas))

    def test_get_name(self):
        from db.redis_db import IdNames
        print(IdNames.fetch_uid_by_name('腐剧基地'))

    def test_send_email(self):
        from utils.email_warning import send_email
        send_email()

    def test_get_weibo_detail_cont(self):
        """
        test for get weibo's all cont
        :return:
        """
        from page_get import status
        print(status.get_cont_of_weibo('4129510280252577'))


if __name__ == '__main__':
    unittest.main()