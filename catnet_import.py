#!/usr/bin/python
# -*- coding: utf-8 -*-
from coverity_import import CoverityIssueCollector, main, Issue

import xml.etree.ElementTree as ET


class CatNETCollector(CoverityIssueCollector):

    '''
    A simple collector for Cat.NET reports
    '''

    def process(self, f):
        tree = ET.parse(f)
        root = tree.getroot()
        for e in root.findall('.//Rule'):
            name = e.findtext('Name')
            identifier = e.findtext('Identifier')

            for res in e.findall('.//Result'):
                entry_variable = res.findtext('EntryVariable')
                res_id = res.findtext('Identifier')
                suppressed = res.findtext('Suppressed') != 'false'
                confidence_level = res.findtext('ConfidenceLevel')
                problem = res.findtext('ProblemDescription')

                msg = Issue(
                    checker='Cat.NET',
                    subcategory=identifier,
                    description=problem,

                    tag=name,
                    extra=res_id
                )

                for trans in res.find('./Transformations'):
                    line = trans.get('line')
                    filename = trans.get('file')
                    description = trans.findtext('StatementType')
                    msg.function = trans.findtext('StatementMethod')

                    msg.add_location(line, filename, description)

                print confidence_level, suppressed

                if confidence_level != 'Low' and not suppressed:
                    self._issues.add(msg) 
                    self._files |= set([x.filename for x in msg._locs])

if __name__ == '__main__':
    import sys
    print CatNETCollector().run(sys.argv[-1])
