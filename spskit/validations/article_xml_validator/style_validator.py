# coding: utf-8
import packtools


class StyleValidator:

    def __init__(self, configuration):
        self.configuration = configuration

    def validate(self, xml_filepath, report_file_path):
        parsed_xml = packtools.XML(xml_filepath)
        xml_validator = packtools.XMLValidator.parse(parsed_xml)
        sps_is_valid, sps_errors = xml_validator.validate_style()

        with open(report_file_path, 'w') as f:
            f.write('\n'.join(sps_errors))

        return sps_is_valid

    def sps_and_dtd_versions(self):
        return True


class SPSversions(object):

    def __init__(self):
        self.versions = {}
        self.dtd_infos = {}
        self.dtd_id_items = [
            '-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN',
            '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN',
            '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.1 20151215//EN',
        ]
        self.versions[self.dtd_id_items[0]] = [
            'None',
            'sps-1.0',
            'sps-1.1',
            ]
        self.versions[self.dtd_id_items[1]] = [
            'sps-1.2',
            'sps-1.3',
            'sps-1.4',
            'sps-1.5',
            'sps-1.6',
            'sps-1.7',
            'sps-1.8',
            ]
        self.versions[self.dtd_id_items[2]] = [
            'sps-1.7',
            'sps-1.8',
            ]

        for name, dtd_info in xml_versions.XPM_FILES.items():
            dtd_id = dtd_info.get('dtd id')
            if dtd_id not in self.dtd_infos.keys():
                self.dtd_infos[dtd_id] = {}
            self.dtd_infos[dtd_id]['url'] = [
                dtd_info.get('remote'),
                dtd_info.get('remote').replace('https:', 'http:')]
            self.dtd_infos[dtd_id]['sps'] = self.versions.get(dtd_id)
