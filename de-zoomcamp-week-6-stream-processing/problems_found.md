ImportError: DLL load failed while importing cimpl

SOLUTION: $env:CONDA_DLL_SEARCH_MODIFICATION_ENABLE=1 in Powershell. 
You need to set this DLL manually in Conda Env.

ModuleNotFoundError: No module named 'avro'

SOLUTION: pip install confluent-kafka[avro]. 
For some reason, Conda also doesn't include this when installing confluent-kafka via pip.

SOURCES:
https://github.com/confluentinc/confluent-kafka-python/issues/590
https://githubhot.com/repo/confluentinc/confluent-kafka-python/issues/1186?page=2
https://github.com/confluentinc/confluent-kafka-python/issues/1221
https://stackoverflow.com/questions/69085157/cannot-import-producer-from-confluent-kafka

