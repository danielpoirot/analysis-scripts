import re
import sys
import os.path
from coverity_import import CoverityIssueCollector, main, get_opts

class AdaControlCollector(CoverityIssueCollector):
    '''
    A simple collector for AdaControl reports.
    '''
    _report_re = re.compile(r'^(?P<file>.+):(?P<line>\d+):\d+:\s*.+:\s*(?P<subcategory>.+): (?P<description>.*)$', re.M)

    def process(self, f):
        '''
        This method assumes that reports are isolated to a single line.
        If your tool reports issues on multiple lines, or for some other
        reason the report lines may not be reordered, you'll need to override
        this method to handle things appropriately.
        '''
        for l in f:
            if not l.strip(): continue
            m = self._report_re.match(l)
            if m:
                f = m.groupdict()
                msg = self.create_issue(checker='AdaControl',
                            tag = f['description'],
                            description = f['description'],
                            subcategory = f['subcategory'],
                           )
                msg.add_location(f['line'], f['file'])
                self.add_issue(msg)
            elif l.strip() == 'Counts summary:':
                break
            else:
                print 'Unrecognized input format:', l
                sys.exit(-1)

if __name__ == '__main__':
    opts = get_opts('adacontrol_import.py', sys.argv)
    print AdaControlCollector(**opts).run(sys.argv[-1])
