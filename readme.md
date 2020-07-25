![pypi](https://img.shields.io/pypi/v/stonky?style=for-the-badge)
![unittest](https://img.shields.io/github/workflow/status/jkwill87/stocky/unittest?style=for-the-badge)
[![licence](https://img.shields.io/github/license/jkwill87/mnamer.svg?style=for-the-badge)](https://github.com/jkwill87/stonky/blob/master/license.txt)
[![style black](https://img.shields.io/badge/Style-Black-black.svg?style=for-the-badge)](https://github.com/ambv/black)

# 📈 stonky

stonky is a simple command line dashboard for monitoring stocks. It pulls live data from [Yahoo! Finance](https://finance.yahoo.com) so anything it can support, e.g. international exchanges, crypocurrencies, etc., stonky can too.

![screenshot](https://github.com/jkwill87/stonky/raw/master/assets/screenshot.png)

## Install

`$ pip3 install --user stonky`

## Config

stonky is mainly configured through a config file. By default it looks for and loads a file named **`.stonky.cfg`** in your home directory. You can also specify a custom path by passing the `--config=<PATH>` command line argument which can be useful to monitor multiple watchlists. If you run stonky without a config file it will load [the example one](https://github.com/jkwill87/stonky/blob/master/stonky/__example.cfg) by default.

## Arguments

You can also set or override many of stonky's settings via command-line arguments.

```
usage: stonky [-h] [--config PATH] [--currency CODE] [--refresh SECONDS] [--sort FIELD]

optional arguments:
  -h, --help         show this help message and exit
  --config PATH      sets path to config file
  --currency CODE    converts all amounts using current forex rates
  --refresh SECONDS  refreshes output on set interval
  --sort FIELD       orders stocks by field

FIELDS can be one of ticket, bid, ask, low, high, close, change, volume
```
