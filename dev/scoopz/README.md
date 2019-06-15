<img width=500 src=https://user-images.githubusercontent.com/2152766/59205156-2eecb500-8b9a-11e9-8ad9-2ef1e167b7b8.png>

Install anything from [Scoop](https://scoop.sh/) as a Rez package.

<br>

### Features

- **Large selection** Install any of the [500+ available packages](https://github.com/ScoopInstaller/Main/tree/master/bucket) from Scoop
- **Try before you buy** Like `apt-get` and `yum`, no packages are actually installed until you've witnessed and confirmed what Scoop comes up with, including complex dependencies.

<br>

### Installation

This repository is a Rez package, here's how you can install it.

```bash
$ git clone https://github.com/mottosso/rez-scoopz.git
$ cd rez-scoopz
$ rez build --install
```

<br>

### Usage

![scoopz](https://user-images.githubusercontent.com/2152766/59216542-bbf03800-8bb3-11e9-85a0-421df2b85f37.gif)

`scoopz` is used like any other Rez package, and comes with a handy `install` executable for convenient access.

```bash
$ rez env scoopz -- install python
...
$ python --version
Python 3.7.3
```

Which is the equivalent of calling..

```bash
$ rez env scoopz
> $ install curl
```

And, for the advanced user, it may also be used as a Python package. Note that it requires Rez itself to be present as a package, along with a copy of Python that isn't coming from Rez.

> How does this work?

```bash
$ rez env python rez scoopz
> $ python -m scoopz --help
usage: __main__.py [-h] [--verbose] [--release] [--prefix PATH] [-y] [-q]
                   request

positional arguments:
  request        Packages to install, e.g. python curl

optional arguments:
  -h, --help     show this help message and exit
  --verbose      Include Scoop output amongst scoopz messages.
  --release      Write to REZ_RELEASE_PACKAGES_PATH
  --prefix PATH  Write to this exact path
  -y, --yes      Do not ask to install, just do it
  -q, --quiet    Do not print anything to the console
```

<br>

### Update

The current version of this package, and in effect Scoop, is `2019-05-15` (see `package.py`).

Because each Rez package is idempotent, an effort is made to disable Scoops native auto-update functionality, along with maintaining a fixed relationship between the version of Scoop and version of "bucket", which is what Scoop calls its package repository. Scoop is only ever compatible with a single version of a repository, as both packages and API changes frequently over time.

To update to a newer version, specify either a tag, such as `2019-05-15` or commit SHA for *both Scoop and bucket*. This is important, else Scoop may not work.

<br>

### Why?

Packaging external software with Rez is a pain and unfun for anyone. Some software is available through Scoop, such as `python` so that you won't have to worry about packaging it yourself.

- [Full list](https://github.com/ScoopInstaller/Main/tree/master/bucket)

<br>

### Architecture

Rez wraps Scoop, forwarding any call made and parsing its response. Whenever an "app" is installed from one of its "buckets", the app is later converted into a Rez package and installed like any other.

```
$ rez env scoopz -- install python
     |
     |                        .-------------------> ~/packages/python/3.7.3
     |                        |
.----o-------- scoopz --------o----.
|    |                        |    |
| .--v-------- Scoop ---------o--. |
| |                              | |
| |                              | |
| |                              | |
| |                              | |
| |______________________________| |
|                                  |
`----------------------------------`

```

<br>

### FAQ

> Why rez-scoopz? Why not X?

This project came about as a requirement for a separate project, here are the developer "journal" from there.

- https://gist.github.com/mottosso/0945b2d19a1920e999fbfb61f4f301a3
- https://gist.github.com/mottosso/5492d55f20b1f38979c8577fc5f5cfbc
