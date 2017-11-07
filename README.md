# Web Platform for Chorus Battles
A website that brings together the chorus battle (cb) community on YouTube, Twitter, and other social media sites.

## How to Run Locally
1. Clone this repo
```
git clone https://github.com/jchen2186/cbplatform.git
```

2. Create and use a virtual env
```python
virtualenv .venv
source .venv/bin/activate
```

3. Install the requirements
```python
pip install -r requirements.txt
pip install -e .
```

4. Run the development server
```python
python application.py
```

Updating the Requirements
```python
pip freeze > requirements.txt
```