import os

from spskit.sps.article_data import ArticleData


def get_article_packages(xml_packages):
    article_packages = []
    for xml_pkg in xml_packages:
        xmlfile = xml_pkg['xml']
        files = xml_pkg['related_files']
        with open(xmlfile, 'rb') as fp:
            xmlcontent = fp.read().decode('utf-8')
        article_data = ArticleData(xmlcontent, 'file')

        assets = []
        attachments = []
        for f in files:
            basename = os.path.basename(f)
            if basename in article_data.internal_xlink_href:
                assets.append(f)
            else:
                attachments.append(f)
        xml_pkg['assets'] = assets
        xml_pkg['attachments'] = attachments
        article_packages.append((xml_pkg))
    return article_packages
