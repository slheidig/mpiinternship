# !/bin/sh

# For Mac:
#gzcat $1 | awk -v prop=$3 'BEGIN {srand()}
#  /^#/ { print $0 }
#  !/^$/ { if (rand() <= prop) print $0 }' > $2

# For Linux
zcat $1 | awk -v prop=$3 'BEGIN {srand()}
  /^#/ { print $0 }
  !/^$/ { if (rand() <= prop) print $0 }'  > $2

