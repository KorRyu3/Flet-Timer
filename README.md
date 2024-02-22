# Flet Timer
Python GUI Application using Flet.  
It is a timer that counts down.

## Installation
### Step0: Clone this repository
```bash
$ git clone https://github.com/KorRyu3/Flet_Timer.git
$ cd Flet_Timer
```

### Step1: Install mise
```bash
$ brew install mise
$ echo 'eval "$(mise activate zsh)"' >> "${ZDOTDIR-$HOME}/.zshrc"
```

### Step2: Install Poetry
```bash
$ brew install poetry
$ poetry completions zsh > ~/.zfunc/_poetry
```
#### Add this to your ~/.zshrc
```bash
fpath+=~/.zfunc
autoload -Uz compinit && compinit
```


### Step3: Install Environment
```bash
$ mise i
```

### Step4: Install Packages
```bash
$ poetry install --no-root
```

## Usage
### Step0: Run App
```bash
$ poetry run python3 src/app.py
```
