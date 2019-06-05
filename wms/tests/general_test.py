# Created by sonlp on 05/04/2019
import logging
from parameterized import parameterized



_logger = logging.getLogger(__name__)


class GeneralTestCase:
    @staticmethod
    def custom_test_name_func(testcase_func, param_num, param):
        return "{}_[{}]___test_num[{}]".format(

            testcase_func.__name__,
            parameterized.to_safe_name("__".join(str(x) for x in param.args)),
            param_num,
        )