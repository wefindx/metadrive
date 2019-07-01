import logging
import sys

import click

from metadrive.core.runner import MetaDriveRunner

logging.basicConfig(
    level=logging.WARNING,
    format="%(message)s",
    stream=sys.stderr
)


@click.command()
@click.argument(
    'resource',
    required=True,
    metavar='<resource>'
)
@click.argument(
    'mountpoint',
    required=False,
    metavar='<mountpoint>'
)
@click.option(
    '-u', '--user',
    required=False,
    type=str,
    help='Reuse a drive by name.'
)
@click.option(
    '-p', '--period',
    required=False,
    type=float,
    help='Period of resynchronization in number of seconds.'
)
def connect(resource, mountpoint=None, user=None, period=900):
    runner = MetaDriveRunner(
        resource,
        mountpoint=mountpoint,
        session=user,
    )
    try:
        runner.run()
    except KeyboardInterrupt:
        sys.exit(0)
