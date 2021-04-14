### Running tests locally

In order to run the tests locally, e.g. for development, make sure you have installed the requirements by running `pip install -r requirements.txt` in the root of the project. 

You can now run all tests py running `pytest` in the root of the project. in order to run specific tests you can specifying the test file to run, e.g. `pytest tests/path/to/your/testfile.py`. You can also run individual tests only using the `-k` flag of pytest `pytest tests/path/to/your/testfile.py -k 'test_your_whatever'` where `test_your_whatever` is the name of the test definition. For more information, please, refer to the [pytest docs](https://docs.pytest.org/en/).

It is recommended to run the tests locally (and to add tests to your chnages and code additions). Tests will automatically run when trying to merge into or push to master. The merge or push will be rejected if any test fails.