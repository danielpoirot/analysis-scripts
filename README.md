analysis-scripts
================

Scripts to facilitate import of third-party analysis results into Coverity
Connect, via the third-party integration toolkit.  The toolkit requires at
least version 6.5 with an appropriate license; please contact your Coverity
sales team if you would like to import third-party analysis results into your
Coverity platform.

These scripts will generally translate the output from the third-party
analysis tool into a JSON format that Coverity's cov-import-defects command
understands.  Your workflow will typically look like this:

0. Optionally run cov-build on your codebase to improve analysis results
1. Run third-party analysis tool, generating appropriate output
2. Run one of these scripts to translate the third-party output for Coverity
3. Run cov-import-defects to import the defects
4. Run cov-commit-defects to commit all the issues to Coverity Connect

Command-line options
--------------------
These scripts share a common command line format.  You'll want to run the
scripts with a command line like this:

    python <script> [ - | file ... ]

Where '-' indicates that the input should be read from stdin

Note that the filenames listed in the analysis output need to be absolute
paths.  Normally, specifying an absolute path to the analysis command will
ensure that the output uses the absolute path.

coverity_import.py
------------------
Script providing generic support for the Coverity import.  You won't typically
run this script directly; it will be imported by the main script.

cppcheck_import.py
------------------
Script providing support for importing Cppcheck results (see
http://cppcheck.sourceforge.net).

You'll need to use the --xml-version=2 option when you run cppcheck.  Note
that the XML output goes to stderr, so you'll typically redirect stderr to a
file or pipe so that it can be processed by cppcheck_import.py.

valgrind_import.py
------------------
Script providing support for importing Valgrind results (see
http://valgrind.org).

You'll need to use the --xml=yes option when you run valgrind.  This script
has only been used with the memcheck tool; others may or may not work.

vera++_import.py
------------------
Script providing support for importing Vera++ Community Edition results (see
http://www.inspirel.com/vera/).

You'll need to use the -showrules option when you run vera++.

