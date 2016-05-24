=====
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
