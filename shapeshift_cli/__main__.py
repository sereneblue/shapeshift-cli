"""
shapeshift-cli
An unofficial cli for https://shapeshift.io

Usage:
	shapeshift-cli email <email_address> <transaction_id>
	shapeshift-cli info <have_currency> <want_currency>
	shapeshift-cli ls
	shapeshift-cli rate <have_currency> <want_currency>
	shapeshift-cli shift [-f=<amount> | -a] [-e=<email>] <have_currency> <want_currency> <refund_address> <withdraw_address>
	shapeshift-cli status <address>
	shapeshift-cli time <address>
	shapeshift-cli valid <currency> <address>

Options:
	-h --help                Show this screen.
	-e                       Email address to send receipt to
	-f=<amount>              Specify a fixed transaction (shifting)
	-a                       Automated shifting
	--version                Show version

Examples:
	shapeshift-cli -a shift ltc btc -e your.email@domain.com
	shapeshift-cli ls
	shapeshift-cli valid btc 1dice8EMZmqKvrGE4Qc9bUFf9PX3xaYDp
"""

from inspect import getmembers, isclass
from docopt import docopt

from . import __version__ as VERSION

def main():
		"""Main CLI entrypoint."""
		from shapeshift_cli.shapeshift_cli import ShapeShift

		client = ShapeShift()
		options = docopt(__doc__, version=VERSION)

		if options['email']:
			client.get_receipt(options['<email_address>'], options['<transaction_id>'])
		elif options['info']:
			client.get_market_info("_".join((options['<have_currency>'], options['<want_currency>'])))
		elif options['ls']:
			client.get_coins()
		elif options['rate']:
			client.get_rate("_".join((options['<have_currency>'], options['<want_currency>'])))
		elif options['shift']:
			if options['-f']:
				try:
					amt = float(options['-f'])
					client.shift_fixed_amount(
						amt, "_".join((options['<have_currency>'], options['<want_currency>'])),
						options['<refund_address>'], options['<withdraw_address>']
					)
				except ValueError:
					print('The fixed amount is not a valid value.')
			elif options['-a']:
				client.auto_shift(
						"_".join((options['<have_currency>'], options['<want_currency>'])),
						options['<refund_address>'], options['<withdraw_address>'],
						options.get('-e', None)
					)
			else:
				client.shift_coins(
						"_".join((options['<have_currency>'], options['<want_currency>'])),
						options['<refund_address>'], options['<withdraw_address>']
					)
		elif options['status']:
			client.get_tx_status(options['<address>'])
		elif options['time']:
			client.get_time_remaining(options['<address>'])
		elif options['valid']:
			client.is_valid_address(options['<currency>'], options['<address>'])