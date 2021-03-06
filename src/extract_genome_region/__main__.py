"""Given a CSV file of variable information defining the regions of interest along with input and output fasta file paths, write a file that contains a fasta-formatted representation of these regions."""

import sys
import click as cli

import csv
from collections import namedtuple
import textwrap as tw

from pyfaidx import Fasta

# Why does this file exist, and why __main__?
# For more info, read:
# - https://www.python.org/dev/peps/pep-0338/
# - https://docs.python.org/2/using/cmdline.html#cmdoption-m
# - https://docs.python.org/3/using/cmdline.html#cmdoption-m



def gen_records(path):
    """Given the csv `path`, yield each record as a `namedtuple`.

    Args:
        path (str): location of the "regions" CSV file.

    Yields:
        namedtuple: each row info from the "regions" CSV file.
    """
    expected_headers = 'record_name,scaffold,start,stop,left_bfr,right_bfr'
    Record = namedtuple('Record', expected_headers)

    with open(path, 'r') as records:
        reader = csv.reader(records)
        actual_headers = next(reader)

        if set(actual_headers) != set(Record._fields):
            raise ValueError("Your csv column headers should be: {headers}.".format(headers=Record._fields))

        for rec in reader:
            yield Record(*rec)



def gen_coords(records):
    """Given records as a ``namedtuple``, yield coordinate information as a ``namedtuple``.

    Args:
        records (namedtuple): each row info from the "regions" CSV file.

    Yields:
        namedtuple: the actual coordinates for slicing the fasta sequence (accounting for any buffers) for a single row in the "regions" CSV file.

    Note:
        The coordinates in each yielded ``namedtuple`` will assume slicing indexing of standard python strings (zero-based).
    """
    Coord = namedtuple('Coord', 'record_name,scaffold,start,stop')

    for rec in records:
        rec_start = int(rec.start) - 1
        rec_end = int(rec.stop)
        left_bfr = int(rec.left_bfr)
        right_bfr = int(rec.right_bfr)

        start = rec_start - left_bfr
        stop = rec_end + right_bfr

        if start < 0:
            start = 0

        yield Coord(record_name=rec.record_name,
                    scaffold=rec.scaffold,
                    start=start,
                    stop=stop)

def gen_faidx_objs(fasta, coords, naming_strategy=None):
    """Given the pyfaidx fasta obj and the coords generator, yield each sequence slice as ``pyfaidx.Sequence`` objs.

    Args:
        fasta (faidx.Fasta): faidx fasta object.
        coords (generator): of row information from "regions" CSV file.
        naming_strategy (str): [csv|seq_range|csv_seq_range] how to name each record. If ``None``, use coord.record_name as string.

    Yields:
        generator: of faidx sequence objects (``faidx.Sequence``) for each row in the "regions" CSV file.
    """
    for coord in coords:
        if naming_strategy is None:
            naming_strategy = 'csv'

        if naming_strategy == 'csv':
            seq_obj = fasta[coord.scaffold][coord.start:coord.stop]
            seq_obj.myname = coord.record_name
            yield seq_obj

        if naming_strategy == 'seq_range':
            seq_obj = fasta[coord.scaffold][coord.start:coord.stop]
            seq_obj.myname = seq_obj.longname
            yield seq_obj

        if naming_strategy == 'csv_seq_range':
            try:
                seq_obj = fasta[coord.scaffold][coord.start:coord.stop]
            except ValueError as exc:
                if "imply a diffent length than sequence" in str(exc):
                    raise ValueError("Make sure all coordinate values, and buffers in the `regions` csv file are rational. Offending record: {coord}".format(coord=coord))
            seq_name = "{record_name} {scaffold}:{start}-{end}".format(record_name=coord.record_name,
                                                                       scaffold=seq_obj.name,
                                                                       start=seq_obj.start,
                                                                       end=seq_obj.end)
            seq_obj.myname = seq_name
            yield seq_obj

def gen_out_rec_strings(faidx_objs):
    """Yield the fasta formated record: ready for writing out.

    Args:
        faidx_objs (generator): of ``faidx.Sequence`` objects representing the described region of each row in "regions" CSV file.

    Yields:
        generator: of formated ``str`` objects representing the fasta record of the described region of each row in "regions" CSV file.
    """
    for rec in faidx_objs:
        yield ">{myname}\n{seq}\n".format(myname=rec.myname,
                                          seq=tw.fill(rec.seq, width=70))


@cli.command()
@cli.option("-n", "--naming", type=cli.Choice(['csv', 'seq_range', 'csv_seq_range']), default='csv',
            help="Options regarding how each new fasta record will be named. See main help-text for explainations of options. [default='csv']")
@cli.argument("regions", type=cli.Path(exists=True))
@cli.argument('in_fasta', type=cli.Path(exists=True))
@cli.argument('out_fasta', type=cli.File(mode='w'))
def main(naming, regions, in_fasta, out_fasta):
    """Given a CSV file of variable information defining the regions of interest along with input and output fasta file paths, write a file that contains a fasta-formatted representation of these regions.

    Structure of the `regions` CSV file:

    \b
      record_name   The name you want the seq to have in the new fasta.
         scaffold   The name of the seq record in the source fasta (chromosome, scaffold, contig, etc).
            start   The first bp of the seq feature you want in the new fasta.
             stop   The last bp of the seq feature you want in the new fasta.
         left_bfr   How many "extra" bp with coords smaller than `start` you want (0 for none).
        right_bfr   How many "extra" bp with coords larger than `stop` you want (0 for none).

    Naming Strategies:

    \b
              csv   use only the contents of the `record_name` field in the csv file (>CPR23).
        seq_range   use only the `scaffold` name and sequence range (>scaffold1:230-679).
    csv_seq_range   use both the contents of the `record_name` field and the `scaffold`.
                    name and sequence range (>CPR23 scaffold1:230-679).
    """
    infasta = Fasta(in_fasta, strict_bounds=False)

    records = gen_records(path=regions)
    coords = gen_coords(records=records)
    faidx_objs = gen_faidx_objs(fasta=infasta, coords=coords, naming_strategy=naming)
    out_rec_strings = gen_out_rec_strings(faidx_objs=faidx_objs)

    for rec in out_rec_strings:
        out_fasta.write(rec)



if __name__ == "__main__":
    sys.exit(main())
