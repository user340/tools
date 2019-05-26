PYTHON_UNITTEST=	python -m unittest
PYTHON_PATH=		${PWD}/src:${PYTHONPATH}
TEST_CODE=			tests.speed_wifi_home

test:
	cd src && PYTHONPATH=${PYTHON_PATH} ${PYTHON_UNITTEST} ${TEST_CODE} -v
