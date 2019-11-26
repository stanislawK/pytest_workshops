Run tests::
  $ pytest

Output:
. - test passed
F - test failed
E - Error - exception happend outside of the test function

More information about test run and failure is available with -v (verbose) or -vv (even more verbose)::
    $ pytest -v
    $ pytest -vv

The easiest way to fire up only specific test is -k expresion. It runs only tests which have given phrase in name.
Eg if we have test_one(), test_two() and test_three() and we use command::
  $ pytest -k three
Only test_three() will be fired up

To run only tests which failed last time use --lf (--late-failed)::
  $ pytest --lf

We are able to run debugger inside test function if it failed. It is pretty streightforward. Just add --pbd.
PDB debugger will be set excatly in place where test failed::
  $ pytest --pdb

Run test with code coverage output::
  $ pytest --cov=app
Generate code coverage report to html (htmlcov directory will be created)::
  $ pytest --cov=app --cov-report=html
