 # pytest test_database.py::Test_core::test_core
 # pytest test_database.py::Test_core::test_xpath
 # pytest test_database.py::Test_core::test_response_pickle
 # pytest test_database.py::Test_spider_base::test_process_task
 # pytest test_database.py::Test_spider_base::test_get_response
 #  pytest test_database.py::Test_scheduler::test_sched
 #  pytest test_database.py::Test_spider_base::test_process_task
# pytest test_engine.py::Test_engine::test_crawl
# pytest test_misc.py
# pytest test_misc.py::test_import_file
# pytest test_misc.py::test_walk_modules
# pytest test_misc.py::test_dump_tmp
# pytest test_spider_loader.py::Test_Settings::test_settings
# pytest test_spider_loader.py::Test_spider_loader::test_load
#pytest test_bloomfilter.py::test_bloomfilter
#pytest test_proxy.py::test_db_get_all
#pytest test_proxy.py::test_db_get_random
# pytest test_proxy.py::test_db_update_flag
# pytest test_proxy.py::test_db_get_ip
# pytest test_proxy.py::test_db_insert_many
# pytest test_spider_base.py::test_spider_add_task
# pytest test_spider_base.py::test_spider_base_find_task_hander
# pytest test_spider_base.py::test_spider_perform_callback

# pytest test_proxy.py::test_db_add_flag


# pytest test_database.py::Test_database::test_get
# pytest test_database.py::Test_database::test_put
# pytest  test_spider_updateproxy.py::Test_spider_updateproxy::test_updateproxy
# pytest test_torrent.py::test_magnet_info
python restart.py  pytest ./tests/test_misc.py::test_dump_tmp
find -name __pycache__ -delete
find -name '*.pyc' -delete