# coding: utf-8

import os


class AssetsValidator:

    def __init__(self, configuration):
        self.configuration = configuration

    def validate(self, article_data, xml_filepath, xml_assets, report_file_path):
        xlinks = article_data.internal_xlink_href
        asset_file_names = [os.path.basename(asset) for asset in xml_assets]

        content = self.format_report(asset_file_names, 'Files')
        content += self.format_report(xlinks, 'xlink:href')

        content += self.report_content(xlinks, asset_file_names, 'xlink:href not found')
        content += self.report_content(asset_file_names, xlinks, 'Assets not found')
        content += self.report_content(article_data.pdf_items, asset_file_names, 'PDFs not found')

        with open(report_file_path, 'w') as f:
            f.write(content)

    def find_items_in_list(self, items, _list):
        found = []
        notfound = []
        for f in items:
            if f in _list:
                found.append(f)
            else:
                notfound.append(f)
        return found, sorted(notfound)

    def report_content(self, items, _list, header):
        found, notfound = self.find_items_in_list(items, _list)
        return self.format_report(notfound, header)

    def format_report(self, items, header):
        if len(items) > 0:
            content = '\n{}\n'.format(header)
            content += [' - {}\n'.format(item) for item in items]
            return content
        return ''
