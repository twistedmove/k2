/**
 * @brief
 * compose
 *
 * @copyright
 * Copyright (c)  2020  Xiaomi Corporation (authors: Daniel Povey)
 *
 * @copyright
 * See LICENSE for clarification regarding multiple authors
 */

#ifndef K2_CSRC_FSA_ALGO_H_
#define K2_CSRC_FSA_ALGO_H_

#include "k2/csrc/array.h"
#include "k2/csrc/fsa.h"

namespace k2 {


// Note: b is FsaVec<Arc>.
void Intersect(const DenseFsa &a, const FsaVec &b, FsaVec *c,
               Array1<int32_t> *arc_map_a = nullptr,
               Array1<int32_t> *arc_map_b = nullptr);



/*
  compose/intersect array of FSAs (multiple streams decoding or training in
  parallel, in a batch)... basically composition with frame-synchronous beam pruning,
  like in speech recognition.

  This code is intended to run on GPU (but should also work on CPU).

         @param[in] a_fsas   Input FSAs, `decoding graphs`.  There should
                         either be one FSA (a_fsas.Dim0() == 1) or a vector of
                         FSAs with the same size as b_fsas (a_fsas.Dim0() ==
                         b_fsas.Dim0()).
         @param[in] b_fsas   Input FSAs that correspond to neural network
                         outputs (see documentation in fsa.h).
         @param[in] beam   Decoding beam, e.g. 10.  Smaller is faster,
                         larger is more exact (less pruning).  This is the
                         default value; it may be modified by {min,max}_active.
         @param[in] max_active  Maximum active states allowed per frame.
                         (i.e. at each time-step in the sequences).  Sequence-
                         specific beam will be reduced if more than this number of
                         states are active.
         @param[in] min_active  Minimum active states allowed per frame; beam
                         will be decreased if the number of active states falls
                         below this
         @param[out] out Output vector of composed, pruned FSAs, with same Dim0()
                         as b_fsas.  Elements of it may be empty if the composition
                         was empty, either intrinsically or due to failure of
                         pruned search.
         @param[out] arc_map_a  Vector of

*/
void IntersectDensePruned(FsaVec &a_fsas,
                          DenseFsaVec &b_fsas,
                          float beam,
                          int32_t max_active_states,
                          int32_t min_active_states,
                          FsaVec *out,
                          Array1<int32_t> *arc_map_a,
                          Array1<int32_t> *arc_map_b);


}  // namespace k2

#endif  // K2_CSRC_FSA_ALGO_H_