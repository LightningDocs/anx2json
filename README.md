# anx2json
Python script that converts HotDocs .anx files to Knackly .json files

## Commands

To trim down a knackly file and remove all `id$` keys, run

```bash
python strip_id.py <filename>
```

By default, this creates a new file "`_<filename>`". To replace the file instead, include the `-r` tag

```bash
python strip_id.py <filename> [-r]
```


