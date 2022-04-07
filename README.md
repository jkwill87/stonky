[![pypi](https://img.shields.io/pypi/v/stonky?style=for-the-badge)](https://pypi.org/project/stonky)
[![unittest](https://img.shields.io/github/workflow/status/jkwill87/stocky/unittest?style=for-the-badge)](https://github.com/jkwill87/stonky/actions)
[![licence](https://img.shields.io/github/license/jkwill87/mnamer.svg?style=for-the-badge)](https://github.com/jkwill87/stonky/blob/master/license.txt)
[![style black](https://img.shields.io/badge/Style-Black-black.svg?style=for-the-badge)](https://github.com/ambv/black)

# 📈 stonky

stonky is a simple command line dashboard for monitoring stocks. It pulls live data from [Yahoo! Finance](https://finance.yahoo.com) so anything it can support, e.g. international exchanges, cryptocurrencies, etc., stonky can too.

![screenshot](https://github.com/jkwill87/stonky/raw/master/assets/screenshot.png)

## Installing and Upgrading

`$ pip3 install --user --upgrade stonky`

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

FIELDS can be one of amount, amount_desc, ticket, ticket_desc, change, change_desc, volume, volume_desc.
```

## Contributions

Community contributions are a welcome addition to the project. In order to be merged upsteam any additions will need to be formatted with [black](https://black.readthedocs.io) for consistency with the rest of the project and pass the continuous integration tests run against the PR. Before introducing any major features or changes to the configuration api please consider opening [an issue](https://github.com/jkwill87/stonky/issues) to outline your proposal.

Bug reports are also welcome on the [issue page](https://github.com/jkwill87/stonky/issues). Please include any generated crash reports if applicable. Feature requests are welcome but consider checking out [if it is in the works](https://github.com/jkwill87/stonky/issues?q=label%3Arequest) first to avoid duplication.
