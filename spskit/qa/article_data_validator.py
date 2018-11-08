# coding: utf-8

import plumber

"""
usa os dados de artigos e journal já registrados
etc
"""
class ArticleDataValidator:

    def __init__(self, configuration):
        self.configuration = configuration

    def validate(self, data, report_file_path):
        data, report = self._plumber_pipeline.run(data, rewrap=True)
        with open(report_file_path, 'w') as f:
            f.write(report)
        return report

    @property
    def _plumber_pipeline(self):
        return plumber.Pipeline(
            self.SetupPipe(),
            self.spsPipe(),
            self.expiration_spsPipe(),
            self.languagePipe(),
            self.languagesPipe(),
            self.article_typePipe(),
            self.journal_titlePipe(),
            self.publisher_namePipe(),
            self.journal_id_publisher_idPipe(),
            self.journal_id_nlm_taPipe(),
            self.journal_issnsPipe(),
            self.months_seasonsPipe(),
            self.issue_labelPipe(),
            self.article_date_typesPipe(),
            self.toc_sectionPipe(),
            self.doiPipe(),
            self.article_idPipe(),
            self.paginationPipe(),
            self.article_id_otherPipe(),
            self.orderPipe(),
            self.total_of_pagesPipe(),
            self.total_of_equationsPipe(),
            self.total_of_tablesPipe(),
            self.total_of_figuresPipe(),
            self.total_of_referencesPipe(),
            self.ref_display_only_statsPipe(),
            self.contribPipe(),
            self.contrib_idPipe(),
            self.contrib_namesPipe(),
            self.contrib_collabsPipe(),
            self.affiliationsPipe(),
            self.fundingPipe(),
            self.article_permissionsPipe(),
            self.historyPipe(),
            self.titles_abstracts_keywordsPipe(),
            self.related_articlesPipe(),
            self.sectionsPipe(),
            self.paragraphsPipe(),
            self.disp_formulasPipe(),
            self.tablewrapPipe(),
            self.validate_xref_reftypePipe(),
            self.missing_xref_listPipe(),
            self.refstatsPipe(),
            self.refs_sourcesPipe(),
            self.endPipe()
        )

    class SetupPipe(plumber.Pipe):

        def transform(self, data):
            report = {}
            return data, report

    class EndPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class spsPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class expiration_spsPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class languagePipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class languagesPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class article_typePipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class journal_titlePipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class publisher_namePipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class journal_id_publisher_idPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class journal_id_nlm_taPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class journal_issnsPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class months_seasonsPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class issue_labelPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class article_date_typesPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class toc_sectionPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class doiPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class article_idPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class paginationPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class article_id_otherPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class orderPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class total_of_pagesPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class total_of_equationsPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class total_of_tablesPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class total_of_figuresPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class total_of_referencesPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class ref_display_only_statsPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class contribPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class contrib_idPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class contrib_namesPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class contrib_collabsPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class affiliationsPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class fundingPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class article_permissionsPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class historyPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class titles_abstracts_keywordPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class related_articlesPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class sectionsPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class paragraphsPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class disp_formulasPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class tablewrapPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class validate_xref_reftypePipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class missing_xref_listPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class refstatsPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class refs_sourcesPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed
