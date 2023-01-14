import argparse
from pathlib import Path

from satnogsclient import config, settings
from satnogsclient.waterfall import EmptyArrayError, Waterfall

__version__ = config.VERSION


def main_satnogs_plot_waterfall():
    """
    CLI Script to create SatNOGS Waterfall png Files from SatNOGS Waterfall .dat files.
    """
    parser = argparse.ArgumentParser(
        prog='SatNOGS Client - Plot Waterfalls',
        description='Create a SatNOGS Waterfall Image from a SatNOGS waterfall .dat File.',
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'satnogs-client version {__version__}',
    )
    parser.add_argument(
        'WATERFALL_DAT_FILE',
        type=str,
        help='The input waterfall dat file',
    )
    args = parser.parse_args()

    output_file = Path('./') / (Path(args.WATERFALL_DAT_FILE).stem + '.png')

    vmin = settings.SATNOGS_WATERFALL_MIN_VALUE
    vmax = settings.SATNOGS_WATERFALL_MAX_VALUE
    try:
        waterfall = Waterfall(args.WATERFALL_DAT_FILE)
        waterfall.plot(output_file, vmin, vmax)
    except FileNotFoundError:
        print('No waterfall data file found')
    except EmptyArrayError:
        print('Waterfall data array is empty')
