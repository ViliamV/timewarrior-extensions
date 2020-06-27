# timewarrior-extensions
Extensions for [Timewarrior](https://timewarrior.net/)

## Installation
Install the extensions

```sh
  pip install --user timewarrior-extensions
```
And install extensions you want

## Extensions
### Percentage
Time report with %

#### Installation
```
timewarrior_percentage_install
```

#### Usage
```sh
  timew percentage
  timew percentage :day
  timew percentage :week
  timew percentage :lastweek
  timew percentage :month
```

#### Output
```
Tag             Duration  Portion
--------------  --------  -------
Multi word tag  3:00       44.9%
development     1:31       22.8%
meeting         1:00       15.0%
review          1:00       15.0%
S2              0:08        2.1%
S               0:01        0.2%
--------------  --------  -------
Total           6:40      100.0%
```

## Development

```sh
  git clone https://github.com/ViliamV/timewarrior-extensions.git
  cd timewarrior-extensions
  poetry install
  ln -rs pre-commit .git/hooks/
```
