# can-i-observe
Utilities for picking out observing days

## Usage

To use the basic utility, install with `setup.py`:
```
python setup.py install
pip install -e .
```

This exposes the command line utility `caniobserve`. An example command:
```
caniobserve calendar 0 0 -d 30
```
will generate calendar events in a `.ics` file for Galactic coordinates (0, 0) over the next 30 days.
