# coding: utf-8

import os


class AssetsValidator:

    def __init__(self, configuration):
        self.configuration = configuration

    def validate(self, article_data, xml_filepath, xml_assets, report_file_path):
        xlinks = article_data.internal_xlink_href
        assets = [os.path.basename(asset) for asset in xml_assets]

        xlinks_set = set(xlinks)
        assets_set = set(assets)

        missingA = assets_set - xlinks_set
        missingB = xlinks_set - assets_set

        pdfs = ['{}.pdf'.format(article_data.name)]
        pdfs += ['{}_{}.pdf'.format(article_data.name, lang) for lang in article_data.languages[1:]]
        missingA = missingA - set(pdfs)

        content = self.report_content(assets, 'Assets')
        content += self.report_content(xlinks, 'xlink:href')
        content += self.report_content(missingB, 'Assets not found')
        content += self.report_content(missingA, 'xlink:href not found')
        content += self.report_content([item for item in pdfs if not pdfs in assets], 'PDF not found')

        with open(report_file_path, 'w') as f:
            f.write(content)

    def report_content(self, items, header):
        if len(items) > 0:
            content = '\n{}\n'.format(header)
            content += [' - {}\n'.format(item) for item in items]
            return content
        return ''
