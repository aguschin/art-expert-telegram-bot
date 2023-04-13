export FLYIO_APP_NAME="art-expert-chat-art-platform-duplicate"
export FLYIO_ORG_NAME="cap_ds_bootcamp_2023"

mlem build docker_dir \
    -m price \
    --target dockerdir \
    --server fastapi \
    --server.request_serializer pil_numpy \
    --args.base_image python:3.9.16-slim

# Fix packages versions
sed -i 's/numpy==1.21.6/numpy==1.22/g' ./dockerdir/requirements.txt
sed -i 's/tensorflow==2.11.0/tensorflow==2.12.0/g' ./dockerdir/requirements.txt
sed -i 's/keras==2.11.0/keras==2.12.0/g' ./dockerdir/requirements.txt

cp ./fly.toml ./dockerdir/fly.toml 
cd dockerdir
flyctl deploy