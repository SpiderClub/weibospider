PROJ_DIR=`pwd`
VENV=${PROJ_DIR}/.env
PROJ_NAME=WeiboSpider

if [ ! -e ${VENV} ];then
    virtualenv --prompt "(${PROJ_NAME})" ${VENV} -p  python3
fi

source ${VENV}/bin/activate 

export PYTHONPATH=${PROJ_DIR}

export PROJ_DIR

export PATH=${PATH}:${PROJ_DIR}/bin
