# coding: utf-8

import logging

from lxml import etree
from io import StringIO


class XML(object):

    def __init__(self, textxml):
        self.original = textxml
        textxml = textxml.strip()
        self.processing_instruction = ''
        if textxml.startswith('<?xml'):
            self.processing_instruction = textxml[:textxml.find('?>')+2]
            textxml = textxml[len(self.processing_instruction):].strip()
        self.text = textxml

    @property
    def text(self):
        if self.tree is None:
            return self.original
        return self.processing_instruction+etree.tostring(
            self.tree, encoding='unicode')

    @text.setter
    def text(self, value):
        self._parse_xml(value)

    def _parse_xml(self, text):
        self.errors = []
        self.tree = None
        try:
            xml = StringIO(text)
            self.tree = etree.parse(xml)
        except etree.XMLSyntaxError as e:
            if hasattr(e, 'message'):
                self.errors.append(e.message)
            else:
                self.errors.append(str(e))
        except Exception as e:
            msg = 'XML._parse_xml(): Unknown error. '
            logging.exception(msg, e)
            self.errors.append(msg)

    @property
    def pretty_text(self):
        if self.tree is None:
            return self.text.replace('<', '\n<').replace('\n</', '</').strip()
        return self.processing_instruction+etree.tostring(
                self.tree, encoding='unicode',
                pretty_print=True)


class XMLValidatorWithSchema(object):

    def __init__(self, xsd_filename):
        self.xml_schema = xsd_filename

    @property
    def xml_schema(self):
        return self._xml_schema

    @xml_schema.setter
    def xml_schema(self, xsd_filename):
        try:
            with open(xsd_filename, 'r') as str_schema:
                schema_doc = etree.parse(str_schema)
                self._xml_schema = etree.XMLSchema(schema_doc)
        except (IOError, ValueError, etree.XMLSchemaError) as e:
            logging.exception('XMLValidatorWithSchema.xml_schema', e)

    def validate(self, tree):
        if self.xml_schema is None:
            return 'XMLSchema is not loaded'

        try:
            self.xml_schema.validate(tree)
        except etree.XMLSyntaxError as e:
            return e.message
        except Exception as e:
            logging.exception('XMLValidatorWithSchema.validate', e)

        try:
            self.xml_schema.assertValid(tree)
        except etree.DocumentInvalid as e:
            return e.message
        except Exception as e:
            logging.exception('XMLValidatorWithSchema.assertValid', e)


class ValidatedXML(object):

    def __init__(self, textxml):
        self._errors = []
        self._original_xml = None
        self._pretty_xml = None
        if textxml is None:
            self.errors = ['Empty XML']
        else:
            self._original_xml = XML(textxml)
            self._pretty_xml = XML(self._original_xml.pretty_text)
            self.errors = self._pretty_xml.errors

    @property
    def tree(self):
        if self._original_xml is not None:
            return self._original_xml.tree

    @property
    def errors(self):
        return self._errors

    @errors.setter
    def errors(self, messages):
        if messages is not None:
            if isinstance(messages, list):
                self._errors.extend(messages)
            else:
                self._errors.append(messages)

    def validate(self, validate_with_schema=None):
        if len(self.errors) == 0:
            if validate_with_schema is not None:
                self.errors = validate_with_schema.validate(
                    self._pretty_xml.tree)

    def display(self, numbered_lines=False):
        if self._original_xml is not None:
            if numbered_lines:
                lines = self._original_xml.pretty_text.split('\n')
                nlines = len(lines)
                digits = len(str(nlines))
                return '\n'.join(
                    [u'{}:{}'.format(str(n).zfill(digits), line)
                     for n, line in zip(range(1, nlines), lines)])
            return self._original_xml.pretty_text
