# AWS Tag All
Tag all resources in AWS

## Prerequisites
```pip install boto3```

## Usage
```
from tagger import Tagger
Tagger(tags={'key': 'value'}).tag_all()
```