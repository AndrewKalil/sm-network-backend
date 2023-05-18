This is a flask api for CRUD operations on posts and their corresponding comments in a social network.

## Getting started
Download project and install dependencies
```bash
git clone git@github.com:AndrewKalil/sm-network-backend.git
cd ./sm-network-backend
pip install -r requirements.txt
python -m venv env
./env/Scripts/activate
```

## Run the project
```bash
flask run
```

## Run tests
```bash
python -m pytest
```

## View coverage report
```bash
python -m coverage run -m pytest
python -m coverage report
```