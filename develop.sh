# development script for fein-skeleton
# watches for changes in the skeleton folder
# and recreates project from the skeleton
if [ $# -ne 1 ]
then
  echo "Usage: `basename $0` {project_name}"
  exit 1 
fi
PROJECT_NAME=$1
watchmedo shell-command \
    --patterns="*.py;*.sass;*.js;*.png;*.jpg;*.html;*.md" \
    --recursive \
    --command='echo "Regenerating..." && mkdir ../feinskeletontemp && cd ../feinskeletontemp && django-admin.py startproject --template=../fein-skeleton '"${PROJECT_NAME}"' && mkdir -p ../'"${PROJECT_NAME}"'project && cp -r '"${PROJECT_NAME}"'/* ../'"${PROJECT_NAME}"'project/ && cd .. && rm -rf feinskeletontemp' .
