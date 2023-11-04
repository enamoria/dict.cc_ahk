Script to show German definitions, by crawling dict.cc

# Usage
## Install dependencies
`pip install -r requirements.txt`

## Get definitions
`python get_def.py`

## Integrate with AHK
Map CapsLock & C to run `get_def.py`
```
	CapsLock & c::
	run, python.exe \path\to\get_def.py 
```
