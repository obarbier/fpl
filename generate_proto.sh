#!/usr/bin/env bash
# PROTOC_VERSION="$(protoc --version)"
# if test "$PROTOC_VERSION" != 'libprotoc 3.12.3'; then
#     PROTOC_ZIP=protoc-3.12.3-linux-x86_64.zip
#     curl -o tmp/ https://github.com/protocolbuffers/protobuf/releases/download/v3.12.3/$PROTOC_ZIP
#     sudo unzip -o $PROTOC_ZIP -d /usr/local bin/protoc
#     sudo unzip -o $PROTOC_ZIP -d /usr/local 'include/*'
#     rm -f $PROTOC_ZIP
# fi
export PATH=$PATH:/home/obarbier/Downloads/protoc-gen-grpc-web
PROTOS="fplsupercharge/protos"
PROTOS_JS="fplsupercharge/server/js/src"
protoc -I="$PROTOS" \
    --python_out="$PROTOS" \
    --js_out=import_style=commonjs:"$PROTOS_JS" \
    --grpc-web_out=import_style=commonjs,mode=grpcwebtext:"$PROTOS_JS" \
    "$PROTOS"/apiServices.proto