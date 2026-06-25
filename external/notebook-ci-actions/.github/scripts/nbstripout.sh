#!/bin/bash
find notebooks/ -name '*.ipynb' -exec nbstripout {} \;
