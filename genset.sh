# generate a set of random files

while read seed; do
  while read config; do
    OUTPUT_NAME="pregens/twr_rand_s${seed}_p${config}"
    echo "python3 twr_rand.py --o ${OUTPUT_NAME} --s ${seed} ${config}"
    python3 twr_rand.py --o "${OUTPUT_NAME}" --s "${seed}" ${config}
  done <configs.txt
done <seeds.txt
