DEST_FOLDER="orca-mini-3b/"
mkdir -p $DEST_FOLDER
cd $DEST_FOLDER
curl -L -O https://storage.googleapis.com/download.usefulsensors.com/ai_in_a_box/orca-mini-3b.tar.gz
tar -xf *.tar.gz
echo "Archive extraction succeeded in ${MODEL_FOLDER}/${DEST_FOLDER}."
mv orca-mini-3b.ggmlv3.q4_0.bin $DOWNLOADED_FOLDER
rm *.tar.gz