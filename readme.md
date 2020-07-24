# stonky

stonky is a simple command line dashboard for stocks. It pulls live data from [Yahoo Finance](https://finance.yahoo.com).

## Config

stonky is mainly configured through a config file. By default it looks for and loads a file named **`.stonky.cfg`** in your home directory. You can specify a custom path by passing the `--config=<PATH>` command line argument. Checkout [example.cfg](https://github.com/jkwill87/stonky/blob/master/example.cfg) for inspiration.

## Arguments

You can set or override some of stonky's settings via command-line arguments.

```
usage: stonky [-h] [--config PATH] [--currency CODE] [--refresh SECONDS] [--sort FIELD]

optional arguments:
  -h, --help         show this help message and exit
  --config PATH      sets path to config file
  --currency CODE    converts all amounts using current forex rates
  --refresh SECONDS  refreshes output on set interval
  --sort FIELD       orders stocks by field
```

Sort fields can be one of **`ticket`**, **`bid`**, **`ask`**, **`low`**, **`high`**, **`close`**, **`change`**, or **`volume`**.
