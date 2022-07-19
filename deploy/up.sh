# env
if [[ -f ./.env ]]; then
    echo "getting environment variables from .env..."
    . ./.env
fi

# Stop Running Containers
RUNNING_CONTAINERS=$(docker ps -q --filter ancestor=$APP_NAME:$APP_VERSION)

if [ ${#RUNNING_CONTAINERS} -ne 0 ]; then
    echo "Stopping currently running containers..."
    docker stop $RUNNING_CONTAINERS
fi

# Delete Containers
ALL_CONTAINERS=$(docker ps -a -q --filter ancestor=$APP_NAME:$APP_VERSION)

if [ ${#ALL_CONTAINERS} -ne 0 ]; then
    echo "Deleting containers..."
    docker rm $ALL_CONTAINERS
fi

# Delete Image
docker rmi -f $APP_NAME:$APP_VERSION

# Up
mkdir -p logs

docker build \
    -f Dockerfile.production \
    --tag $APP_NAME:$APP_VERSION .

docker run \
    --name $APP_NAME-main \
    -e TELE_KEY=$TELE_KEY \
    -e SQL_URL=$SQL_URL \
    --network $NETWORK_NAME \
    -v $(pwd)/logs:/app/logs \
    -d $APP_NAME:$APP_VERSION main_app.py production

docker run \
    --name $APP_NAME-ws \
    -e TELE_KEY=$TELE_KEY \
    -e SQL_URL=$SQL_URL \
    --network $NETWORK_NAME \
    -v $(pwd)/logs:/app/logs \
    -d $APP_NAME:$APP_VERSION ws_app.py production
