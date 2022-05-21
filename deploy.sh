NCP_HOST=$SERVER_HOST:$SERVER_PORT
BASE_DIR=$PWD
CA_PATH="$BASE_DIR/ca.pem"
CERT_PATH="$BASE_DIR/cert.pem"
KEY_PATH="$BASE_DIR/key.pem"

docker run -H $NCP_HOST --tlscacert=$CA_PATH --tlscert=$CERT_PATH --tlskey=$KEY_PATH -p 8000:8000 -d cafe-search:$RELEASE_VERSION
