PROJ_DIR=`pwd`
VENV=${PROJ_DIR}/.env
PROJ_NAME=WeiboSpider

# if your python release is not anaconda or cpython, please change the code below
ANACONDA_EXISTS=`which conda`

if [ $? -eq 0 ];then
    conda install virtualenv -yq
else
    pip3 install -i https://pypi.douban.com/simple/ virtualenv
fi

if [ ! -d ${VENV} ];then
    virtualenv --prompt "(${PROJ_NAME})" ${VENV} -p  python3
fi

source ${VENV}/bin/activate

export PYTHONPATH=${PROJ_DIR}
export PROJ_DIR
export PATH=${PATH}:${VENV}/bin

# if your host is in China, use douban's pypi to speed up
pip3 install -i https://pypi.douban.com/simple/ -r requirements.txt
