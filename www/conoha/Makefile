PYTHON_UNITTEST=	python -m unittest
PYTHON_PATH=		${PWD}/src:${PYTHONPATH}
UNITTEST_API=		tests.unittest_api.TestConoHaAPI
UNITTEST_CMD=		tests.unittest_cmd.TestConoHaCmd

test: api_test cmd_test

test_api:
	cd src && PYTHONPATH=${PYTHON_PATH} python tests/unittest_api.py -v

test_api_init:
	cd src && PYTHONPATH=${PYTHON_PATH} ${PYTHON_UNITTEST} ${UNITTEST_API}.test_init -v

test_api_get_billing_incoices:
	cd src && PYTHONPATH=${PYTHON_PATH} ${PYTHON_UNITTEST} ${UNITTEST_API}.test_get_billing_invoices -v

test_api_get_vms_list:
	cd src && PYTHONPATH=${PYTHON_PATH} ${PYTHON_UNITTEST} ${UNITTEST_API}.test_get_vms_list -v

test_api_get_identity:
	cd src && PYTHONPATH=${PYTHON_PATH} ${PYTHON_UNITTEST} ${UNITTEST_API}.test_get_identity -v

test_api_get_vms_detail:
	cd src && PYTHONPATH=${PYTHON_PATH} ${PYTHON_UNITTEST} ${UNITTEST_API}.test_get_vms_detail -v

test_api_get_all_vm_details:
	cd src && PYTHONPATH=${PYTHON_PATH} ${PYTHON_UNITTEST} ${UNITTEST_API}.test_get_all_vm_details -v

test_api_get_flavors_list:
	cd src && PYTHONPATH=${PYTHON_PATH} ${PYTHON_UNITTEST} ${UNITTEST_API}.test_get_flavors_list -v

test_api_change_flavor:
	cd src && PYTHONPATH=${PYTHON_PATH} ${PYTHON_UNITTEST} ${UNITTEST_API}.test_change_flavor -v

test_api_confirm_flavor:
	cd src && PYTHONPATH=${PYTHON_PATH} ${PYTHON_UNITTEST} ${UNITTEST_API}.test_confirm_flavor -v

test_api_get_flavor_id:
	cd src && PYTHONPATH=${PYTHON_PATH} ${PYTHON_UNITTEST} ${UNITTEST_API}.test_get_flavor_id -v

test_api_power_on_vm:
	cd src && PYTHONPATH=${PYTHON_PATH} ${PYTHON_UNITTEST} ${UNITTEST_API}.test_power_on_vm -v

test_api_stop_cleanly_vm:
	cd src && PYTHONPATH=${PYTHON_PATH} ${PYTHON_UNITTEST} ${UNITTEST_API}.test_stop_cleanly_vm -v

test_api_reboot_vm:
	cd src && PYTHONPATH=${PYTHON_PATH} ${PYTHON_UNITTEST} ${UNITTEST_API}.test_reboot_vm -v

test_api_get_flavor_name:
	cd src && PYTHONPATH=${PYTHON_PATH} ${PYTHON_UNITTEST} ${UNITTEST_API}.test_get_flavor_name -v

test_cmd:
	cd src && PYTHONPATH=${PYTHON_PATH} python tests/unittest_cmd.py -v

test_cmd_show_vm_detail:
	cd src && PYTHONPATH=${PYTHON_PATH} ${PYTHON_UNITTEST} ${UNITTEST_CMD}.test_show_vm_detail -v

test_cmd_return_table:
	cd src && PYTHONPATH=${PYTHON_PATH} ${PYTHON_UNITTEST} ${UNITTEST_CMD}.test_return_table -v

test_cmd_show_billing:
	cd src && PYTHONPATH=${PYTHON_PATH} ${PYTHON_UNITTEST} ${UNITTEST_CMD}.test_show_billing -v

test_cmd_change_flavor:
	cd src && PYTHONPATH=${PYTHON_PATH} ${PYTHON_UNITTEST} ${UNITTEST_CMD}.test_change_flavor -v

test_cmd_get_server_id_from_tag:
	cd src && PYTHONPATH=${PYTHON_PATH} ${PYTHON_UNITTEST} ${UNITTEST_CMD}.test_get_server_id_from_tag -v
