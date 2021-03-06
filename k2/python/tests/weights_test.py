#!/usr/bin/env python3
#
# Copyright (c)  2020  Xiaomi Corporation (author: Haowen Qiu)
#
# See ../../../LICENSE for clarification regarding multiple authors

# To run this single test, use
#
#  ctest --verbose -R weights_test_py
#

import unittest

import torch

import k2


class TestWfsa(unittest.TestCase):

    def setUp(self):
        s = r'''
        0 4 1
        0 1 1
        1 2 1
        1 3 1
        2 7 1
        3 7 1
        4 6 1
        4 8 1
        5 9 -1
        6 9 -1
        7 9 -1
        8 9 -1
        9
        '''
        self.fsa = k2.str_to_fsa(s)
        self.num_states = self.fsa.num_states()
        weights = torch.FloatTensor([1, 1, 2, 3, 4, 5, 2, 3, 4, 3, 5, 6])
        self.weights = k2.FloatArray1(weights)

    def test_max_weight(self):
        forward_max_weights = k2.DoubleArray1.create_array_with_size(
            self.num_states)
        backward_max_weights = k2.DoubleArray1.create_array_with_size(
            self.num_states)
        wfsa = k2.WfsaWithFbWeights(self.fsa, self.weights,
                                    k2.FbWeightType.kMaxWeight,
                                    forward_max_weights, backward_max_weights)
        expected_forward_max_weights = torch.DoubleTensor(
            [0, 1, 3, 4, 1, float('-inf'), 3, 9, 4, 14])
        expected_backward_max_weights = torch.DoubleTensor(
            [14, 13, 9, 10, 9, 4, 3, 5, 6, 0])
        self.assertTrue(
            torch.equal(forward_max_weights.data,
                        expected_forward_max_weights))
        self.assertTrue(
            torch.allclose(forward_max_weights.data,
                           expected_forward_max_weights))
        self.assertTrue(
            torch.allclose(backward_max_weights.data,
                           expected_backward_max_weights))

    def test_logsum_weight(self):
        forward_logsum_weights = k2.DoubleArray1.create_array_with_size(
            self.num_states)
        backward_logsum_weights = k2.DoubleArray1.create_array_with_size(
            self.num_states)
        wfsa = k2.WfsaWithFbWeights(self.fsa, self.weights,
                                    k2.FbWeightType.kLogSumWeight,
                                    forward_logsum_weights,
                                    backward_logsum_weights)
        expected_forward_logsum_weights = torch.DoubleTensor(
            [0, 1, 3, 4, 1,
             float('-inf'), 3, 9.126928, 4, 14.143222])
        expected_backward_logsum_weights = torch.DoubleTensor(
            [14.143222, 13.126928, 9, 10, 9.018150, 4, 3, 5, 6, 0])
        self.assertTrue(
            torch.allclose(forward_logsum_weights.data,
                           expected_forward_logsum_weights))
        self.assertTrue(
            torch.allclose(backward_logsum_weights.data,
                           expected_backward_logsum_weights))


if __name__ == '__main__':
    unittest.main()
