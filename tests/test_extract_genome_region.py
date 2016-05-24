"""Provide functions to test this library."""
from __future__ import absolute_import, print_function

import types
import pyfaidx

import pytest

import extract_genome_region.__main__ as egr


def gfui049232_info():
    """Provide true data that we can use to confirm correctness."""
    real = pyfaidx.Fasta("tests/data/real.fa")

    no_flanks = real[0]
    yes_flanks = real[1]

    i = no_flanks.name.split('|')
    no_flanks_info = {"start": i[3],
                      "stop": i[4],
                      "scaffold": i[2],
                      "sequence": no_flanks[:].seq,
                      }

    i = yes_flanks.name.split('|')
    yes_flanks_info = {"start": i[3],
                       "stop": i[4],
                       "scaffold": i[2],
                       "sequence": yes_flanks[:].seq,
                       }

    return no_flanks_info, yes_flanks_info


## Test Data
no_flanks_info, yes_flanks_info = gfui049232_info()

infasta = pyfaidx.Fasta("tests/data/GfusI1.3contigs.fa", strict_bounds=False)

bad_headers_csv = "tests/data/bad_headers.csv"
extra_headers_csv = "tests/data/extra_headers.csv"
missing_headers_csv = "tests/data/missing_headers.csv"
pass_csv = "tests/data/pass.csv"
start_stop_switched_csv = "tests/data/start_stop_switched.csv"



# Begin tests

def test_gen_rec_is_generator(path=pass_csv):
    """Should return a generator."""
    records = egr.gen_records(path=path)
    assert isinstance(records, types.GeneratorType)

def test_gen_rec_expected_headers_expected(path=pass_csv):
    """Freakout if the code has changed what headers we expect."""
    expected_headers = set('record_name,scaffold,start,stop,left_bfr,right_bfr'.split(','))
    records = egr.gen_records(path=path)
    assert expected_headers == set(next(records)._fields)


@pytest.mark.parametrize("path", [bad_headers_csv,
                                   extra_headers_csv,
                                   missing_headers_csv])
def test_gen_rec_headers_csv(path):
    with pytest.raises(ValueError):
        next(egr.gen_records(path=path))
