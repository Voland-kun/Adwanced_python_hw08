import csv
import os
import json
import pickle
from pathlib import Path


__all__ = ['filewriter']


def _size_count(path, list_=[]):
    result = list_
    size = 0
    for i in Path(path).iterdir():
        if i.is_file():
            size += os.path.getsize(i)
            result.append({
                "name": os.path.basename(i),
                "parent": os.path.basename(os.path.dirname(i)),
                "type": "file",
                "size": os.path.getsize(i),
            })
        else:
            size_dir = _size_count(i, result)[0]
            size += size_dir
            result.append({
                "name": os.path.basename(i),
                "parent": os.path.basename(os.path.dirname(i)),
                "type": "directory",
                "size": size_dir,
            })
    return size, result


def filewriter(path):
    s = _size_count(path)
    path_dict = s[1]
    path_dict.append({
        "name": os.path.basename(path),
        "parent": ".",
        "type": "directory",
        "size": s[0],
    })

    with open('res.json', 'w', encoding='utf-8') as f:
        json.dump(path_dict, f, ensure_ascii=False, indent=2)

    with open('res.csv', 'w', encoding='utf-8', newline='') as f:
        fieldnames = list(path_dict[0])
        csv_write = csv.DictWriter(f, fieldnames=fieldnames, dialect="excel-tab")
        csv_write.writeheader()
        csv_write.writerows(path_dict)

    with open('res.pickle', 'wb') as f:
        pickle.dump(path_dict, f)
