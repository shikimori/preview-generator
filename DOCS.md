# CLI

**Usage**:

```console
$ [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `fetch`: Fetch anime or manga and save to file
* `make-preview`: Make preview based on input and config

## `fetch`

Fetch anime or manga and save to file

**Usage**:

```console
$ fetch [OPTIONS] ITEM_ID
```

**Arguments**:

* `ITEM_ID`: Target anime/manga id(s)  [required]

**Options**:

* `-M, --multiple`: Need to process multiple ids  [default: False]
* `--app-name TEXT`: Application name for requests  [required]
* `--save-path TEXT`: File to save list of targets  [default: .pgen.json]
* `-m, --manga`: Download manga info  [default: False]
* `--help`: Show this message and exit.

## `make-preview`

Make preview based on input and config

**Usage**:

```console
$ make-preview [OPTIONS] INPUT_FILE
```

**Arguments**:

* `INPUT_FILE`: File with prefetched anime/manga  [required]

**Options**:

* `--output-folder TEXT`: Output folder  [required]
* `--config TEXT`: Config file in YAML format (see: config.example.yaml)  [required]
* `--app-name TEXT`: Application name for requests  [required]
* `-P`: Use multithreading  [default: False]
* `--n_jobs INTEGER`: Number of threads is multithreading is enabled  [default: -1]
* `--demo`: Make demo sequence  [default: False]
* `--help`: Show this message and exit.
