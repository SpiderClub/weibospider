PROJ_DIR=`pwd`
VENV=${PROJ_DIR}/.env
PROJ_NAME=WeiboSpider

# if your python release is not anaconda or cpython, please change the code below
ANACONDA_EXISTS=`which conda`

if [ -e ${ANACONDA_EXISTS} ];then
    conda install virtualenv -yq
else
    pip3 install virtualenv -yq
fi

if [ ! -e ${VENV} ];then
    virtualenv --prompt "(${PROJ_NAME})" ${VENV} -p  python3
fi

source ${VENV}/bin/activate

export PYTHONPATH=${PROJ_DIR}
export PROJ_DIR
export PATH=${PATH}:${VENV}/bin

pip3 install -r requirements.txt
