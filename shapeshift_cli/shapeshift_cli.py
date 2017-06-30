import datetime
import requests
from time import sleep

class ShapeShift:
	def __init__(self):
		"""
		https://shapeshift.io/api
		"""

		self.base_url = "https://shapeshift.io"
		self.session = requests.session()
		self.session.headers.update({
				"User-Agent":"shapeshift-cli/1.0"
			})

	def is_valid_address(self, currency, address):
		"""
		Check if an address is valid for a specific currency
		"""

		url = "/".join((self.base_url, "validateAddress", address, currency))
		response = self.session.get(url).json()

		# check for unknown pair
		if response.get('error', None):
			print(response['error'])
		else:
			print('{} is a valid {} address!'.format(
					address, currency.upper()
				))

	def get_market_info(self, pair):
		"""
		Get the market info for a specified pair
		"""

		url = "/".join((self.base_url, "marketinfo", pair))
		response = self.session.get(url).json()

		# check for unknown pair
		if response.get('error', None):
			print(response['error'])
		else:
			have, want = response['pair'].upper().split('_')
			print('Current rate: 1 {} = {} {}'.format(
					have, response['rate'], want
				))
			print('Miner fee: {} {}'.format(
					response['minerFee'], have
				))
			print('Deposit limit: {} {}'.format(
					response['limit'], have
				))
			print('Minimum limit: {} {}'.format(
					response['minimum'], have
				))

	def get_coins(self):
		"""
		Get available coins and display in columns
		"""

		url = "/".join((self.base_url, "getcoins"))
		coins = self.session.get(url).json()
		coins = ["{} - {}".format(coins[i]['symbol'], coins[i]['name']) for i in coins.keys() if coins[i]['status'] == "available"]

		print('Available coins: ')
		for c1, c2 in zip(coins[:int(len(coins)/2)], coins[int(len(coins)/2):]):
			print("{:30} {:30}".format(c1, c2))

	def get_rate(self, pair):
		"""
		Get the rate for a specfied pair
		"""

		url = "/".join((self.base_url, "rate", pair))
		response = self.session.get(url).json()

		# check for unknown pair
		if response.get('error', None):
			print(response['error'])
			return (False, None)
		else:
			have, want = response['pair'].upper().split('_')
			print('Current rate: 1 {} = {} {}'.format(
					have, response['rate'], want
				))
			return (True, response['rate'])

	def get_receipt(self, email, tx_id):
		"""
		Request an email to be sent to specified email address for a specific transaction
		"""

		url = self.base_url + "/mail"
		response = self.session.post(url, data={
				"email": email,
				"txid": tx_id
			}).json()

		if response.get('error', None):
			print(response['error'])
		else:
			if response['status'] == "success":
				print('An email will be sent to {}.'.format(email))

	def get_time_remaining(self, address):
		"""
		Get the time remaining for a fixed amount transaction
		"""

		url = "/".join((self.base_url, "timeremaining", address))
		response = self.session.get(url).json()

		# check for unknown pair
		if response.get('error', None):
			print(response['error'])
		else:
			response['seconds_remaining'] = int(response['seconds_remaining'])
			if response['status'] == "pending":
				print('{:02d}:{:02d} minute(s) left before transaction expires.'.format(
						*(divmod(response['seconds_remaining'], 60))
					))
				if response['seconds_remaining'] < 60:
					print('Be careful, you only have less then a minute left for the deposit window.\nWhy not create a new transaction instead? :)')
			elif response['status'] == "expired":
				print('The deposit address has expired. Please created a new transaction.')

	def get_tx_status(self, address):
		"""
		Get the status of a transaction by address
		"""

		url = "/".join((self.base_url, "txStat", address))
		response = self.session.get(url).json()

		# check for unknown pair
		if response.get('error', None):
			print(response['error'])
			return (False, None)
		else:
			if response['status'] == "no_deposits":
				print('There are no deposits for address: {}'.format(address))
			elif response['status'] == "received":
				print('{} The deposit has been received.'.format(datetime.datetime.now()))
			elif response['status'] == "complete":
				print("Processing complete. {} {} is being sent to {}.\nTransaction ID: {}".format(
						response['outgoingCoin'], response['outgoingType'],
						response['withdraw'], response['transaction']
					))
				return (True, None)
			elif response['status'] == "failed":
				print(response['error'])
			return (False, response)

	def shift_coins(self, pair, refund_address, withdraw_address):
		"""
		Generate deposit address to shift currencies
		"""

		url = self.base_url + "/shift"
		response = self.session.post(url, data={
				"withdrawal": withdraw_address,
				"pair": pair,
				"returnAddress": refund_address
			}).json()

		if response.get('deposit', None):
			self.get_market_info(pair)
			print("Please send your funds to this {} address:\n{}".format(
					response['depositType'], response['deposit']
				))

			return (True, response)

		if response.get('error', None):
			print(response['error'])
		return (False, None)

	def shift_fixed_amount(self, amount, pair, refund_address, withdraw_address):
		"""
		Generate deposit address to shift currencies (fixed amount)
		"""

		# need to convert to the amount of desired currency you want
		# somewhat strange in my opinion ¯\_(ツ)_/¯

		rate = self.get_rate(pair)
		if rate[0]:
			amount = round(float(rate[1]) * amount, 8)
			url = self.base_url + "/sendamount"
			response = self.session.post(url, data={
					"amount": amount,
					"withdrawal": withdraw_address,
					"pair": pair,
					"returnAddress": refund_address
				}).json()

			if response.get('success', None):
				response = response['success']
				have, want = response['pair'].upper().split('_')
				print("If the shift is successful, {} {} will be sent to this address:\n{}\nPlease send EXACTLY {} {} to this {} deposit address:\n{}".format(
						response['withdrawalAmount'], want, response['withdrawal'],
						response['depositAmount'], have, have, response['deposit']
					))
				return (True, response)

			if response.get('error', None):
				print(response['error'])
			return (False, None)
		else:
			print('Could not check rate')
			return (False, None)

	def auto_shift(self, pair, refund_address, withdraw_address, email):
		"""
		Automate shifting between currencies
		Will check every 30 seconds for deposit status
		"""

		status = self.shift_coins(pair, refund_address, withdraw_address)

		# check deposit address
		if status[0]:
			while True:
				tx_response = self.get_tx_status(status[1]['deposit'])
				if tx_response[0]:
					if email:
						self.get_receipt(email, tx_response['transaction'])
					print('Shift was successful. Thanks for using shapeshift-cli!')
					break
				elif tx_response[1].get('error', None):
					break
				elif tx_response[1]['status'] == 'failed':
					break
				sleep(30)
