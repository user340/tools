PYTHON_UNITTEST=	python -m unittest
PYTHON_PATH=		${PWD}/src:${PYTHONPATH}
UNITTEST_QEMU=		tests.qemu.TestQemuImg

test_parse_size:
	cd src && PYTHONPATH=${PYTHON_PATH} ${PYTHON_UNITTEST} ${UNITTEST_QEMU}.test_parse_size -v
