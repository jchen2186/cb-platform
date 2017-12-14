# Connect! Chorus Battle
A website that brings together the chorus battle (CB) community on YouTube, Twitter, and other social media sites.

## We are Live!
[http://cbplatform.herokuapp.com](cbplatform.herokuapp.com)

## How to Run Locally
*** Note that we are using Python3 rather than Python2.

1. Clone this repo
```
git clone https://github.com/jchen2186/cbplatform.git
```

2. Create and use a virtual env
```
virtualenv .venv
source .venv/bin/activate
```

3. Install the requirements
```
pip3 install -r requirements.txt
```

4. Run the development server
```
python3 application.py
```

Updating the Requirements
```
pip3 freeze > requirements.txt
```

## How to Run Pylint
In the cbplatform directory, run the following:
```
python3 pylintrunner.py
```

## How to Run Tests
In the cbplatform directory, run the following:
```
pytest
```
