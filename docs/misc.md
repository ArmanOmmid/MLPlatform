
**Processes By User**
pstree -pT -u $USER

**Disk Usage**
du -shc ./*

**Git Pull Accept All Incoming**
git pull origin -s recursive -X theirs <branch>

**Bash Capture Args**
ARGS=${@: 1}

**Docker with GPUs flags**
--gpus all
