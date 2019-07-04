### Usage

```bash
$ rez env generic_project -- create MyProject
Continue? [Y/n] y
Successfully created %cd%\MyProject
```

```bash
$ rez env generic_project -- create --help
usage: create.py [-h] [-y] [--version VERSION] [--prefix PREFIX] name

Create a new project

positional arguments:
  name               Name of project

optional arguments:
  -h, --help         show this help message and exit
  -y, --yes          Do not ask for confirmation, just do it.
  --version VERSION  Initial version
  --prefix PREFIX    Where to write a new project
```
