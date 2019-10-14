#! /usr/bin/env bash

FILES=("pngdiscover.py")

export PYTHONPATH=$PYTHONPATH:"${PWD}"

for FILE in "${FILES[@]}"
do
  echo "PYLINT EXAMINATION ${FILE}"
  python3 -m pylint $FILE --rcfile=pylintrc
  echo "FLAKE8 EXAMINATION ${FILE}"
  python3 -m flake8 $FILE
  echo "RUN CODE ${FILE}"
  python3 $FILE -r images -f png -d 3
done

echo 'DONE'
