# down
. ./deploy/down.sh

# up
mkdir -p logs
docker build -f Dockerfile.production --tag $APP_NAME:$APP_VERSION .
docker run --name $APP_NAME-main -v $(pwd)/logs:/app/logs -d $APP_NAME:$APP_VERSION main_app.py production
docker run --name $APP_NAME-ws -v $(pwd)/logs:/app/logs -d $APP_NAME:$APP_VERSION ws_app.py production
