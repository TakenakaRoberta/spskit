# coding: utf-8
from utils.report_manager import ReportManager, Pipe, Pipeline


"""
usa os dados de artigos e journal já registrados
etc

"""


class ArticleDataValidator:

    def __init__(self, configuration):
        self.configuration = configuration
        self.report_manager = ReportManager(configuration, self._plumber_pipeline)

    def validate(self, data, report_file_path):
        data, report = self.report_manager.create(data)
        with open(report_file_path, 'w') as f:
            f.write(report)

    @property
    def _plumber_pipeline(self):
        return Pipeline(
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

    class SetupPipe(Pipe):

        def transform(self, data):
            report = {}
            return data, report

    class EndPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class spsPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class expiration_spsPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class languagePipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class languagesPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class article_typePipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class journal_titlePipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class publisher_namePipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class journal_id_publisher_idPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class journal_id_nlm_taPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class journal_issnsPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class months_seasonsPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class issue_labelPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class article_date_typesPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class toc_sectionPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class doiPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class article_idPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class paginationPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class article_id_otherPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class orderPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class total_of_pagesPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class total_of_equationsPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class total_of_tablesPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class total_of_figuresPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class total_of_referencesPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class ref_display_only_statsPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class contribPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class contrib_idPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class contrib_namesPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class contrib_collabsPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class affiliationsPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class fundingPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class article_permissionsPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class historyPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class titles_abstracts_keywordPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class related_articlesPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class sectionsPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class paragraphsPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class disp_formulasPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class tablewrapPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class validate_xref_reftypePipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class missing_xref_listPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class refstatsPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class refs_sourcesPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed
