/*
 * Copyright 2018 Analytics Zoo Authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.intel.analytics.zoo.serving.engine

import com.intel.analytics.bigdl.nn.abstractnn.Activity
import com.intel.analytics.bigdl.tensor.Tensor
import com.intel.analytics.bigdl.utils.T
import com.intel.analytics.zoo.serving.PostProcessing
import com.intel.analytics.zoo.serving.utils.SerParams

object InferenceSupportive {
  def singleThreadInference(preProcessed: Iterator[(String, Activity)],
                           params: SerParams): Iterator[(String, String)] = {
    val postProcessed = preProcessed.grouped(params.coreNum).flatMap(pathByteBatch => {
      val thisBatchSize = pathByteBatch.size
      (0 until params.coreNum).toParArray.map(idx => {
        val t = pathByteBatch(idx)._2
        val result = params.model.doPredict(t)
        val value = PostProcessing(result.toTensor[Float])
        (pathByteBatch(idx)._1, value)
      })
    })
    postProcessed
  }
  def multiThreadInference(preProcessed: Iterator[(String, Activity)],
                           params: SerParams): Iterator[(String, String)] = {
    val postProcessed = preProcessed.grouped(params.coreNum).flatMap(pathByteBatch => {
      val thisBatchSize = pathByteBatch.size

      val t = batchInput(pathByteBatch, params)
      /**
       * addSingletonDimension method will modify the
       * original Tensor, thus if reuse of Tensor is needed,
       * have to squeeze it back.
       */
//      println(s"preparing to predict")
      val result = if (params.modelType == "openvino") {
        val res = params.model.doPredict(t).toTensor[Float].squeeze()
        if (t.isTensor) {
          t.toTensor[Float].squeeze(1)
        }
        else if (t.isTable) {
          val dataTable = t.toTable
          dataTable.keySet.foreach(key => {
            dataTable(key).asInstanceOf[Tensor[Float]].squeeze(1)
          })
        }
        res.squeeze(1)
      } else {
        params.model.doPredict(t).toTensor[Float]
      }
//      println(s"predict end")
      (0 until thisBatchSize).toParArray.map(i => {
        val value = PostProcessing(result.select(1, i + 1), params.filter)
        (pathByteBatch(i)._1, value)
      })
    })
    postProcessed
  }
  def batchInput(seq: Seq[(String, Activity)],
    params: SerParams): Activity = {
    val thisBatchSize = seq.size

    val inputSample = seq.head._2.toTable
    val kvTuples = inputSample.keySet.map(key => {
      (key, Tensor[Float](params.coreNum +:
        inputSample(key).asInstanceOf[Tensor[Float]].size()))
    }).toList
    val t = T(kvTuples.head, kvTuples.tail: _*)
    (0 until thisBatchSize).toParArray.foreach(i => {
      val dataTable = seq(i)._2.toTable
      t.keySet.foreach(key => {
        t(key).asInstanceOf[Tensor[Float]].select(1, i + 1)
          .copy(dataTable(key).asInstanceOf[Tensor[Float]])
        if (params.modelType == "openvino") {
          t(key).asInstanceOf[Tensor[Float]].addSingletonDimension()
        }
      })
    })
    t.keySet.foreach(key => {
      val singleTensorSize = inputSample(key).asInstanceOf[Tensor[Float]].size()
      var newSize = Array(thisBatchSize)
      for (elem <- singleTensorSize) {
        newSize = newSize :+ elem
      }
      t(key).asInstanceOf[Tensor[Float]].resize(newSize)
    })
    if (params.dataShape.length == 1) {
      t.keySet.foreach(key => {
        return t(key).asInstanceOf[Tensor[Float]]
      })
    }
    t
  }
}
