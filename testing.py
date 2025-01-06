from tests.test_service_grid import TestServiceGrid
from tests.test_service_helper import TestServiceHelper
from tests.test_service_metrics import TestServiceMetrics
from tests.test_service_preparation import TestServicePreparation

TestServiceGrid().run_all()
TestServiceHelper().run_all()
TestServiceMetrics().run_all()
TestServicePreparation().run_all()
