============
Installation
============

With Conda
==========

Add package channels to your configuration
------------------------------------------

.. note:: Our goal here is to make sure you have a couple anaconda.org channels in your ``.condarc`` file. If you know you have these, you can skip this section.
    The channels are: bioconda, r, gusdunn.

Lets see what your conda installation looks like to see what needs to be tweaked in order for the installation scripts to
"see" the package channels that we will need. To do this, issue the following command at the terminal::

    $ conda info

Here is mine::

    $ conda info
    Using Anaconda Cloud api site https://api.anaconda.org
    Current conda install:

                 platform : linux-64
            conda version : 4.0.6
      conda-build version : 1.20.2
           python version : 3.5.1.final.0
         requests version : 2.10.0
         root environment : /home/gus/.anaconda  (writable)
      default environment : /home/gus/.anaconda/envs/jupyter
         envs directories : /home/gus/.anaconda/envs
            package cache : /home/gus/.anaconda/pkgs
             channel URLs : https://conda.anaconda.org/bioconda/linux-64/
                            https://conda.anaconda.org/bioconda/noarch/
                            https://conda.anaconda.org/gusdunn/linux-64/
                            https://conda.anaconda.org/gusdunn/noarch/
                            https://conda.anaconda.org/t/<TOKEN>/r/linux-64/
                            https://conda.anaconda.org/t/<TOKEN>/r/noarch/
                            https://conda.anaconda.org/t/<TOKEN>/pandas/linux-64/
                            https://conda.anaconda.org/t/<TOKEN>/pandas/noarch/
                            https://repo.continuum.io/pkgs/free/linux-64/
                            https://repo.continuum.io/pkgs/free/noarch/
                            https://repo.continuum.io/pkgs/pro/linux-64/
                            https://repo.continuum.io/pkgs/pro/noarch/
                            https://conda.anaconda.org/davidbgonzalez/linux-64/
                            https://conda.anaconda.org/davidbgonzalez/noarch/
              config file : /home/gus/.condarc
        is foreign system : False

Right now, we want to see what is in your "config file".  The second to last line tells me that mine is located at ``/home/gus/.condarc``.
If you have a brand new installation, you might not have one yet. If the report says ``None``, we can create one and add the channels easily::

    $ conda config --add channels gusdunn --add channels r --add channels pandas --add channels bioconda

.. note:: Even if you **do** have one, you can run the same command to add the channels. If any channel exists already, it will be skipped.

Install extract_genome_region
-----------------------------

Now you will want to activate the conda environment where you want to install ``extract_genome_region``.  You do that by
running the following (substituting the name of your environment for ``ENVNAME``)::

    $ source activate ENVNAME

Next lets run the install::

    $ conda install extract_genome_region



With pip
========

.. note:: I recommend that you use ``conda`` rather than ``pip``, but ``pip`` should also work.


.. code-block:: shell

    $ pip install git+https://github.com/xguse/extract-genome-region


Confirming  success
===================

Let's make sure it worked by calling the program's help text. You should get something similar to this::

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
                      name and sequence range (>CPR23_scaffold1:230-679).

    Options:
      -n, --naming [csv|seq_range|csv_seq_range]
                                      Options regarding how each new fasta record
                                      will be named. See main help-text for
                                      explainations of options. [default='csv']
      --help                          Show this message and exit.
