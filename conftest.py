import sys
import os

# Add the project root to the sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from core.config import settings


# configure custom variable that holds the version you want to test


def pytest_addoption(parser):
    parser.addoption("--ver", action="store", help="A variable for testing API versions")


def pytest_generate_tests(metafunc):
    ver = metafunc.config.getoption("ver")
    if not ver:        
        versions = [f"/api/v{i}" for i in range(1, int(settings.API_LATEST_VERSION) + 1)]
        metafunc.parametrize("ver", versions)
    else:        
        metafunc.parametrize("ver", ["/api/v" + ver])

