#!/usr/bin/env python3
import os
import click
from astropy import units as u
from astropy.time import Time, TimeDelta
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, get_sun
from datetime import datetime
from ics import Calendar, Event
import numpy as np

from ._version import __version__


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__, '-V', '--version')
@click.pass_context
def cli(ctx):
    """
    Observability tools
    """
    pass 


@click.command(short_help='Make calendar entries for target and telescope',
               no_args_is_help=True,)
@click.argument('l', type=float)
@click.argument('b', type=float)
@click.option('-d', '--day-num', type=int, 
              help='Number of days forward to parse')
@click.option('-t', '--telescope', default='GBT',
              help='Which telescope to use')
def calendar(l, b, day_num, telescope='GBT'):
    """
    Make calendar entries for target and telescope
    """
    target = SkyCoord(f'{l} {b}', unit=(u.deg, u.deg), frame='galactic')
    target = target.icrs

    gbt = EarthLocation(lat=38.4*u.deg, lon=-79.8*u.deg, height=808*u.m)

    ts = np.linspace(0, 24*day_num, 24*day_num*60, endpoint=False) * u.hour
    ts = Time.now() + ts

    altazframe_gbt = AltAz(obstime=ts, location=gbt)
    targetaltazs_gbt = target.transform_to(altazframe_gbt)
    alts = targetaltazs_gbt.alt
    altz = alts.deg - 5.

    starts = []
    ends = []

    for i in range(len(ts)):
        if altz[i] >= 0:
            if i == 0 or altz[i-1] < 0:
                starts.append(ts[i])
            elif i == len(ts) - 1:
                ends.append(ts[i])
        elif altz[i-1] >= 0:
            ends.append(ts[i])
    assert len(starts) == len(ends)

    c = Calendar()

    for i in range(len(starts)):
        e = Event()
        e.name = "Target is in the sky!"
        e.description = (
            f"(l, b) = ({l}, {b}) \n\n"
            f"Weather: https://www.google.com/search?q=green+bank+weather \n\n"
            f"GBT Pizza Plot: https://www.gb.nrao.edu/~rmaddale/Weather/AllOverviews.html#RestOverview \n\n"
            f"GBT Guide: https://github.com/UCBerkeleySETI/bl_docs/wiki/NEW-GBT-Observing-guide"
        )
        e.begin = starts[i].utc.datetime
        e.end = ends[i].utc.datetime
        e.location = "Green Bank, WV"
        c.events.add(e)
    
    with open("target.ics", "w") as f:
        f.write(c.serialize())

    

cli.add_command(calendar)

if __name__ == '__main__':
    cli()