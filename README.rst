=====================
Extract genome region
=====================

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor|
        |
    * - package
      - |version| |downloads|

.. |docs| image:: https://readthedocs.org/projects/extract-genome-region/badge/?style=flat
    :target: https://readthedocs.org/projects/extract-genome-region
    :alt: Documentation Status

.. |travis| image:: https://img.shields.io/travis/xguse/extract-genome-region/master.svg?style=flat&label=Travis
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/xguse/extract-genome-region

.. |appveyor| image:: https://img.shields.io/appveyor/ci/xguse/extract-genome-region/master.svg?style=flat&label=AppVeyor
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/xguse/extract-genome-region





.. |version| image:: https://img.shields.io/pypi/v/extract_genome_region.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/extract_genome_region

.. |downloads| image:: https://img.shields.io/pypi/dm/extract_genome_region.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/extract_genome_region

Given a CSV file of variable information defining the regions of interest, return a file that contains a fasta-formatted representation of these regions.

* Free software: BSD license



Usage
=====

::

    $ extract_genome_region --help
    Usage: extract_genome_region [OPTIONS] REGIONS IN_FASTA OUT_FASTA

      Given a CSV file of variable information defining the regions of interest
      along with input and output fasta file paths, write a file that contains a
      fasta-formatted representation of these regions.

      Structure of the `regions` CSV file:

        record_name   The name you want the seq to have in the new fasta.
           scaffold   The name of the seq record in the source fasta (chromosome, scaffold, contig, etc).
              start   The first bp of the seq feature you want in the new fasta.
               stop   The last bp of the seq feature you want in the new fasta.
           left_bfr   How many "extra" bp with coords smaller than `start` you want (0 for none).
          right_bfr   How many "extra" bp with coords larger than `stop` you want (0 for none).

      Naming Strategies:

                csv   use only the contents of the `record_name` field in the csv file (>CPR23).
          seq_range   use only the `scaffold` name and sequence range (>scaffold1:230-679).
      csv_seq_range   use both the contents of the `record_name` field and the `scaffold`.
                      name and sequence range (>CPR23 scaffold1:230-679).

    Options:
      -n, --naming [csv|seq_range|csv_seq_range]
                                      Options regarding how each new fasta record
                                      will be named. See main help-text for
                                      explainations of options. [default='csv']
      --help                          Show this message and exit.


Installation
============

::

    $ conda install -c bioconda -c gusdunn extract_genome_region

Or

::

    $ pip install extract_genome_region

Documentation
=============

https://extract-genome-region.readthedocs.org/

Development
===========

To run the all tests run::

    tox
