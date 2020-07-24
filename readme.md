# stonky



## Settings

### Config

stonky is mainly configured through a config file. By default it looks for and loads a file named **`.stonky.cfg`** in the users home directory. You can specify a custom path by passing the `--config=<PATH>` command line argument. Take a look at [example.cfg](https://raw.githubusercontent.com/jkwill87/stonky/master/example.cfg) for inspiration.

### Arguments

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

Most of these should be pretty straight forward. Sort fields can be one of `ticket`, `bid`, `ask`, `low`, `high`, `close`, `change`, `volume`.
