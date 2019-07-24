set -x
# create folders for experiments
mkdir -p data
mkdir -p exp

# clone graph embedding tool
git clone https://github.com/cnclabs/smore
cd smore; make; cd ..

# TODO require some installation steps
# clone knn tool
#git clone https://github.com/facebookresearch/faiss
#cd faiss

# prepare python environment
virtualenv -p python3 bandit_env
. ./bandit_env/bin/activate

# download data
wget http://files.grouplens.org/datasets/movielens/ml-10m.zip -P ./data
unzip ./data/ml-10m.zip -d ./data

