#
# Copyright 2018 Analytics Zoo Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from bigdl.util.common import JavaValue
from zoo.common.utils import callZooFunc
from bigdl.nn.layer import Layer
from zoo.pipeline.api.keras.engine import KerasNet
import warnings


class InferenceModel(JavaValue):
    """
    Model for thread-safe inference.
    To do inference, you need to first initiate an InferenceModel instance, then call
    load|load_caffe|load_tf|load_openvino to load a pre-trained model, and finally call predict.

    # Arguments
    supported_concurrent_num: Int. How many concurrent threads to invoke. Default is 1.
    """

    def __init__(self, supported_concurrent_num=1, bigdl_type="float"):
        super(InferenceModel, self).__init__(None, bigdl_type, supported_concurrent_num)

    def load_bigdl(self, model_path, weight_path=None):
        """
        Load a pre-trained Analytics Zoo or BigDL model.

        :param model_path: String. The file path to the model.
        :param weight_path: String. The file path to the weights if any. Default is None.
        """
        callZooFunc(self.bigdl_type, "inferenceModelLoadBigDL",
                    self.value, model_path, weight_path)

    # deprecated in "0.8.0"
    def load(self, model_path, weight_path=None):
        """
        Load a pre-trained Analytics Zoo or BigDL model.

        :param model_path: String. The file path to the model.
        :param weight_path: String. The file path to the weights if any. Default is None.
        """
        warnings.warn("deprecated in 0.8.0")
        callZooFunc(self.bigdl_type, "inferenceModelLoad",
                    self.value, model_path, weight_path)

    def load_caffe(self, model_path, weight_path):
        """
        Load a pre-trained Caffe model.

        :param model_path: String. The file path to the prototxt file.
        :param weight_path: String. The file path to the Caffe model.
        """
        callZooFunc(self.bigdl_type, "inferenceModelLoadCaffe",
                    self.value, model_path, weight_path)

    def load_openvino(self, model_path, weight_path, batch_size=0):
        """
        Load an OpenVINI IR.

        :param model_path: String. The file path to the OpenVINO IR xml file.
        :param weight_path: String. The file path to the OpenVINO IR bin file.
        :param batch_size: Int. Set batch Size, default is 0 (use default batch size).
        """
        callZooFunc(self.bigdl_type, "inferenceModelLoadOpenVINO",
                    self.value, model_path, weight_path, batch_size)

    def load_tensorflow(self, model_path, model_type="frozenModel", intra_op_parallelism_threads=1,
                        inter_op_parallelism_threads=1, use_per_session_threads=True):
        """
        Load an TensorFlow model using tensorflow.

        :param model_path: String. The file path to the TensorFlow model.
        :param model_type: String. The type of the tensorflow model file. Default is "frozenModel"
        :param intra_op_parallelism_threads: Int. The number of intraOpParallelismThreads.
                                             Default is 1.
        :param inter_op_parallelism_threads: Int. The number of interOpParallelismThreads.
                                             Default is 1.
        :param use_per_session_threads: Boolean. Whether to use perSessionThreads. Default is True.
        """
        callZooFunc(self.bigdl_type, "inferenceModelLoadTensorFlow",
                    self.value, model_path, model_type, intra_op_parallelism_threads,
                    inter_op_parallelism_threads, use_per_session_threads)

    def load_tensorflow(self, model_path, model_type,
                        inputs, outputs, intra_op_parallelism_threads=1,
                        inter_op_parallelism_threads=1, use_per_session_threads=True):
        """
        Load an TensorFlow model using tensorflow.

        :param model_path: String. The file path to the TensorFlow model.
        :param model_type: String. The type of the tensorflow model file: "frozenModel" or
         "savedModel".
        :param inputs: Array[String]. the inputs of the model.
        inputs outputs: Array[String]. the outputs of the model.
        :param intra_op_parallelism_threads: Int. The number of intraOpParallelismThreads.
                                                Default is 1.
        :param inter_op_parallelism_threads: Int. The number of interOpParallelismThreads.
                                                Default is 1.
        :param use_per_session_threads: Boolean. Whether to use perSessionThreads. Default is True.
           """
        callZooFunc(self.bigdl_type, "inferenceModelLoadTensorFlow",
                    self.value, model_path, model_type,
                    inputs, outputs, intra_op_parallelism_threads,
                    inter_op_parallelism_threads, use_per_session_threads)

    # deprecated in "0.8.0"
    def load_tf(self, model_path, backend="tensorflow",
                intra_op_parallelism_threads=1, inter_op_parallelism_threads=1,
                use_per_session_threads=True, model_type=None,
                ov_pipeline_config_path=None, ov_extensions_config_path=None):
        """
        Load an TensorFlow model using tensorflow or openvino backend.

        :param model_path: String. The file path to the TensorFlow model.
        :param backend: String. The backend to use for inference. Either 'tensorflow' or 'openvino'.
                        For 'tensorflow' backend, only need to specify arguments
                        intra_op_parallelism_threads, inter_op_parallelism_threads
                        and use_per_session_threads.
                        For 'openvino' backend, only need to specify either model_type or
                        pipeline_config_path together with extensions_config_path.
                        Default is 'tensorflow'.
        :param intra_op_parallelism_threads: For 'tensorflow' backend only. Int.
                                             The number of intraOpParallelismThreads. Default is 1.
        :param inter_op_parallelism_threads: For 'tensorflow' backend only. Int.
                                             The number of interOpParallelismThreads. Default is 1.
        :param use_per_session_threads: For 'tensorflow' backend only. Boolean.
                                        Whether to use perSessionThreads. Default is True.
        :param model_type: For 'openvino' backend only. The type of the TensorFlow model,
                           e.g. faster_rcnn_resnet101_coco, ssd_inception_v2_coco, etc.
        :param ov_pipeline_config_path: For 'openvino' backend only. String.
                                        The file path to the pipeline configure file.
        :param ov_extensions_config_path: For 'openvino' backend only. String.
                                          The file path to the extensions configure file.
                                          Need pipeline_config_path and extensions_config_path
                                          for 'openvino' backend if model_type is not specified.
        """
        warnings.warn("deprecated in 0.8.0")
        backend = backend.lower()
        if backend == "tensorflow" or backend == "tf":
            callZooFunc(self.bigdl_type, "inferenceModelLoadTensorFlow",
                        self.value, model_path, "frozenModel", intra_op_parallelism_threads,
                        inter_op_parallelism_threads, use_per_session_threads)
        elif backend == "openvino" or backend == "ov":
            if model_type:
                if ov_pipeline_config_path:
                    callZooFunc(self.bigdl_type, "inferenceModelOpenVINOLoadTF",
                                self.value, model_path, model_type, ov_pipeline_config_path, None)
                else:
                    callZooFunc(self.bigdl_type, "inferenceModelOpenVINOLoadTF",
                                self.value, model_path, model_type)
            else:
                if ov_pipeline_config_path is None and ov_extensions_config_path is None:
                    raise Exception("For openvino backend, you must provide either model_type or "
                                    "both pipeline_config_path and extensions_config_path")
                callZooFunc(self.bigdl_type, "inferenceModelOpenVINOLoadTF",
                            self.value, model_path, ov_pipeline_config_path,
                            ov_extensions_config_path)
        else:
            raise ValueError("Currently only tensorflow and openvino are supported as backend")

    # deprecated in "0.8.0"
    def load_tf_object_detection_as_openvino(self,
                                             model_path,
                                             object_detection_model_type,
                                             pipeline_config_path,
                                             extensions_config_path
                                             ):
        """
        load object detection TF model as OpenVINO IR
        :param model_path: String, the path of the tensorflow model
        :param object_detection_model_type: String, the type of the tensorflow model
        :param pipeline_config_path: String, the path of the pipeline configure file
        :param extensions_config_path: String, the path of the extensions configure file
        :return:
        """
        warnings.warn("deprecated in 0.8.0")
        callZooFunc(self.bigdl_type,
                    "inferenceModelOpenVINOLoadTF",
                    self.value,
                    model_path,
                    object_detection_model_type,
                    pipeline_config_path,
                    extensions_config_path)

    # deprecated in "0.8.0"
    def load_tf_image_classification_as_openvino(self,
                                                 model_path,
                                                 image_classification_model_type,
                                                 checkpoint_path,
                                                 input_shape,
                                                 if_reverse_input_channels,
                                                 mean_values,
                                                 scale):
        """
        load image classification TF model as OpenVINO IR
        :param model_path: String, the path of the tensorflow model
        :param image_classification_model_type: String, the type of the tensorflow model
        :param checkpoint_path: String, the path of the tensorflow checkpoint file
        :param input_shape: List of Int,
                input shape that should be fed to an input node(s) of the model
        :param if_reverse_input_channels: Boolean,
                the boolean value of if need reverse input channels.
        :param mean_values: List of Float, all input values coming from original network inputs
                            will be divided by this value.
        :param scale: Float, the scale value, to be used for the input image per channel.
        :return:
        """
        warnings.warn("deprecated in 0.8.0")
        callZooFunc(self.bigdl_type,
                    "inferenceModelOpenVINOLoadTF",
                    self.value,
                    model_path,
                    image_classification_model_type,
                    checkpoint_path,
                    input_shape,
                    if_reverse_input_channels,
                    [float(value) for value in mean_values],
                    float(scale))

    def predict(self, inputs):
        """
        Do prediction on inputs.

        :param inputs: A numpy array or a list of numpy arrays or JTensor or a list of JTensors.
        """
        jinputs, input_is_table = Layer.check_input(inputs)
        output = callZooFunc(self.bigdl_type,
                             "inferenceModelPredict",
                             self.value,
                             jinputs,
                             input_is_table)
        return KerasNet.convert_output(output)
