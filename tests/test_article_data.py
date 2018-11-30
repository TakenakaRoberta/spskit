import unittest
import os

from spskit.sps.article_data import ArticleData


TEST_PATH = os.path.dirname(os.path.abspath(__file__))
PKG_PATH = os.path.join(TEST_PATH, 'fixtures/markup_xml/scielo_package')

with open(os.path.join(PKG_PATH, '0034-8910-rsp-48-01-0001.xml')) as f:
    xml_content = f.read()


class ArticleDataTest(unittest.TestCase):

    def test_article_data_sps_version(self):
        article_data = ArticleData('<article specific-use="sps-1.8"/>', 'a01')
        result = article_data.sps_version
        self.assertEqual(result, 'sps-1.8')

    def test_pdf_items(self):
        article_data = ArticleData(xml_content, '0034-8910-rsp-48-01-0001')
        result = article_data.pdf_items
        self.assertEqual(result, ['0034-8910-rsp-48-01-0001.pdf'])

    def test_node_info(self):
        article_data = ArticleData(xml_content, '0034-8910-rsp-48-01-0001')
        result = article_data.nodes_info('.//contrib')
        expected = [
            ('/article/front/article-meta/contrib-group/contrib[1]', 1)]
        self.assertEqual(result[0][0], expected[0][0])

    def test_node(self):
        article_data = ArticleData(xml_content, '0034-8910-rsp-48-01-0001')
        result = article_data.nodes('.//contrib')
        self.assertEqual('Hortale', result[0].findtext('.//surname'))

    def test_xlink_href(self):
        article_data = ArticleData(xml_content, '0034-8910-rsp-48-01-0001')
        result = article_data.xlink_href
        self.assertIn('http://creativecommons.org/licenses/by-nc/3.0/', result)

    def test_internal_xlink_href(self):
        article_data = ArticleData(xml_content, '0034-8910-rsp-48-01-0001')
        result = article_data.internal_xlink_href
        self.assertEqual([], result)

    def test_languages(self):
        article_data = ArticleData(xml_content, '0034-8910-rsp-48-01-0001')
        result = article_data.languages
        self.assertEqual(['en'], result)
