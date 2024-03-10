from unittest import TestCase

from quality.QualityMeasurer import QualityMeasurer


class TestQualityMeasurer(TestCase):

    def test_compare_results_tp(self):
        qm = QualityMeasurer()
        result = qm.compare_results("a", "a")
        self.assertEquals("tp", result)

    def test_compare_results_tn(self):
        qm = QualityMeasurer()
        result = qm.compare_results("other", "other")
        self.assertEquals("tn", result)

    def test_compare_results_TN(self):
        qm = QualityMeasurer()
        result = qm.compare_results("Other", "Other")
        self.assertEquals("tn", result)

    def test_compare_results_fp(self):
        qm = QualityMeasurer()
        result = qm.compare_results("a", "other")
        self.assertEquals("fp", result)

    def test_compare_results_fn(self):
        qm = QualityMeasurer()
        result = qm.compare_results("other", "a")
        self.assertEquals("fn", result)
