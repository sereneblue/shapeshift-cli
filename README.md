# shapeshift-cli
A command line interface for https://shapeshift.io

# Install

### Using pip

```
pip install shapeshift-cli
```

### Build from source

```
git clone https://github.com/sereneblue/shapeshift-cli
cd shapeshift_cli
python setup.py install
```

## Usage

	shapeshift-cli email <email_address> <transaction_id>
	shapeshift-cli info <have_currency> <want_currency>
	shapeshift-cli ls
	shapeshift-cli rate <have_currency> <want_currency>
	shapeshift-cli shift [-f=<amount> | -a] [-e=<email>] <have_currency> <want_currency> <refund_address> <withdraw_address>
	shapeshift-cli status <address>
	shapeshift-cli time <address>
	shapeshift-cli valid <currency> <address>

## Options

    -h --help                Show this screen.
	-e                       Email address to send receipt to
	-f=<amount>              Specify a fixed transaction (shifting)
	-a                       Automated shifting
	--version                Show version


## Examples

##### Shift currency with automated status checking

`shapeshift-cli -a shift ltc btc REFUND_ADDRESS WITHDRAW_ADDRESS -e your.email@domain.com`


##### List available currencies
`shapeshift-cli ls`

##### Check if address is valid for currency
`shapeshift-cli valid btc 1dice8EMZmqKvrGE4Qc9bUFf9PX3xaYDp`


##### Get time remaining for a fixed deposit address

`shapeshift-cli time 1dice8EMZmqKvrGE4Qc9bUFf9PX3xaYDp`

##### Get market info for a currency pair

`shapeshift-cli info HAVE_CURRENCY WANT_CURRENCY`

## Disclaimer

This project is not affiliated or endorsed by Shapeshift.