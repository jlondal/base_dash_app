# Data Explorer

Data Explorer a tool to help your explore a small dataset (excel file).

INSERT VIDEO DEMO

I am assuming you are using a Mac. If you are not using a Mac you will need to
install Python 3 and pip which are required. See requirements.txt for Python
modules that are required.  


## Pre-Install

Skip this section if you have already setup up [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)

**Note pyenv-virtualenv is an plugin to pyenv to provide additional features.
If you have pyenv installed you also have install pyenv-virtualenv too.**

to install pyenv-virtualenv open your terminal

```bash
pip install --upgrade virtualenv
brew install pyenv-virtualenv
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
export PYENV_VIRTUALENV_DISABLE_PROMPT=1
```

## Install

To create your environment run install.sh

```bash
sudo bash install.sh
```

## Run

to run in development

```bash
python app.py
```

or

```bash
bash run.sh
```

Then, navigate to [dashboard](http://127.0.0.1:8000/dashboard)

## Production

As Flask is single threaded meaning it can only serve one user at a time so for  
production were there will likely be many users we require UWSGI to run several
versions of our Flask app.

```bash
bash run_uwsgi.sh
```

Then, navigate to [dashboard](http://127.0.0.1:8000/dashboard)

**Note, we do not recommend you only use UWSGI for you should also run NGINX
or Apache in front of your application.**

## Contributing

We would love you to build on the application to get you started have a read
CONTRIBUTING.MD to learn how the application is structured.

Don't for get to check the pull requests to see if someone else has had the
same idea as you and is already working on it. Team up or pick something else.  
