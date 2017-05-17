# coding:utf-8
import unittest


class TestWeiboSpider(unittest.TestCase):
    # 这单元测试写得我很尴尬...
    def test_get_login_info(self):
        from db import login_info
        infos = login_info.get_login_info()
        self.assertEquals(len(infos), 5)

    def test_login(self):
        """
        是测试是否能成功登录的，然后登录后会把cookie保存到redis中
        """
        import random
        from wblogin.login import get_session
        from db.login_info import get_login_info
        infos = get_login_info()
        if not infos:
            raise Exception('未获取到登陆信息')

        info = random.choice(infos)
        sc = get_session(info.name, info.password)

        if sc:
            print('登陆成功')
        else:
            raise Exception('登录失败')

    def test_freeze_account(self):
        """
        测试账号被封后是否会去查找还有可用账号没有，这里如果需要测试请换成自己数据库中的账号
        """
        from db import login_info
        login_info.freeze_account('18708103033')
        infos = login_info.get_login_info()
        for info in infos:
            if info[0] == '18708103033':
                self.assertEqual(info.enable, 0)

    def test_delete_cookies(self):
        """
        测试根据键来删除cookie
        """
        from db.redis_db import Cookies
        r = Cookies.delete_cookies('18708103033')
        self.assertEqual(r, True)

    def test_page_get(self):
        """
        测试页面抓取功能
        """
        from page_get import basic
        test_url = 'http://weibo.com/p/1005051764222885/info?mod=pedit_more'
        text = basic.get_page(test_url)
        self.assertIn('深扒娱乐热点', text)

    def test_parse_user_info(self):
        """
        测试解析页面功能
        """
        from page_parse.user import person, public
        from page_get.user import get_user_detail
        with open('./tests/writer.html', encoding='utf-8') as f:
            cont = f.read()
        user = person.get_detail(cont)
        user.verify_type = public.get_verifytype(cont)
        self.assertEqual(user.verify_type, 1)
        self.assertEqual(user.description, '韩寒')
        with open('./tests/person.html', encoding='utf-8') as f:
            cont = f.read()
        user = get_user_detail('222333312', cont)
        self.assertEqual(user.follows_num, 539)
        with open('./tests/excp.html', encoding='utf-8') as f:
            cont = f.read()
        user = get_user_detail('1854706423', cont)
        self.assertEqual(user.birthday, '1988年2月21日')

    def test_get_url_from_web(self):
        """
        测试不同类型的用户抓取功能
        """
        from page_get import user as user_get
        normal_user = user_get.get_profile('1195908387')
        self.assertEqual(normal_user.name, '日_推')
        writer = user_get.get_profile('1191258123')
        self.assertEqual(writer.description, '韩寒')
        enterprise_user = user_get.get_profile('1839256234')
        self.assertEqual(enterprise_user.level, 36)

    def test_get_fans(self):
        """
        测试用户粉丝获取功能
        """
        from page_parse.user import public
        with open('./tests/fans.html', encoding='utf-8') as f:
            cont = f.read()
        public.get_fans_or_follows(cont)
        ids = public.get_fans_or_follows(cont)
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
        测试用户信息抓取
        """
        from tasks.user import crawl_person_infos
        crawl_person_infos('2041028560')

    def test_get_search_info(self):
        """
        测试微博搜索结果页面解析功能
        :return: 
        """
        from page_parse import search
        with open('tests/search.html', encoding='utf-8') as f:
            cont = f.read()
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
        with open('tests/search.html', encoding='utf-8') as f:
            cont = f.read()
        infos = search.get_search_info(cont)
        insert_weibo_datas(infos)

    def test_search_keyword(self):
        """
        测试搜索功能
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
        with open('tests/enterprisehome.html', encoding='utf-8') as f:
            html = f.read()
        wbcounts = home.get_wbdata_fromweb(html)
        self.assertEqual(len(wbcounts), 15)

        with open('tests/personhome.html', encoding='utf-8') as f:
            html = f.read()
        wbcounts = home.get_wbdata_fromweb(html)
        print(wbcounts)
        self.assertEqual(len(wbcounts), 15)

    def test_ajax_home_page_data(self):
        """
        测试通过ajax返回的主页数据是否可以正常解析
        :return: 
        """
        from page_parse import home
        with open('tests/asyncpersonhome.html', encoding='utf-8') as f:
            html = f.read()
        datas = home.get_home_wbdata_byajax(html)
        self.assertEqual(len(datas), 15)

    def test_get_total_home_page(self):
        """
        测试获取主页页数
        :return: 
        """
        from page_parse import home
        with open('tests/asyncpersonhome.html', encoding='utf-8') as f:
            html = f.read()
        num = home.get_total_page(html)
        self.assertEqual(num, 18)

    def test_parse_comment_page(self):
        """
        测试对评论页的解析
        :return: 
        """
        from page_parse import comment
        with open('tests/comment.html', encoding='utf-8') as f:
            html = f.read()
        comment_list = comment.get_comment_list(html, '1123331211')
        self.assertEqual(len(comment_list), 19)

    def test_get_total_comment_page(self):
        """
        测试获取所有评论页数
        :return: 
        """
        from page_parse import comment
        with open('tests/comment.html', encoding='utf-8') as f:
            html = f.read()
        total_page = comment.get_total_page(html)
        self.assertEqual(total_page, 227)

    def test_get_total_repost_page(self):
        """
        测试获取所有转发页数
        :return: 
        """
        from page_parse import repost
        with open('tests/repost.html', encoding='utf-8') as f:
            html = f.read()
        total_page = repost.get_total_page(html)
        self.assertEqual(total_page, 1580)

    def test_get_total_comment_to_crawl(self):
        from db import wb_data
        weibo_datas = wb_data.get_weibo_comment_not_crawled()
        print(len(weibo_datas))

    def test_get_name(self):
        from db.redis_db import IdNames
        print(IdNames.fetch_uid_by_name('腐剧基地'))


if __name__ == '__main__':
    unittest.main()