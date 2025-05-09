video_processing_toolkit.utils.train_utils
==========================================

.. py:module:: video_processing_toolkit.utils.train_utils






Module Contents
---------------

.. py:function:: get_annotations(annot_dir, sequence_dir, frame_file)

   Gets the annotations contained in the xml file of the current frame.

   :param annot_dir: The root dir of annotation folders
   :type annot_dir: str
   :param sequence_dir: The directory in which frame is located, relative to
   :type sequence_dir: str
   :param root directory:
   :param frame_file: The frame filename
   :type frame_file: str
   :param i.e.:
   :param sequence_identifier/frame_number.JPEG:
   :param or the full path.:

   :returns:

             (dictionary) A dictionary containing the four values of the
                 the bounding box stored in the following keywords:
                 'xmax' (int): The rightmost x coordinate of the bounding box.
                 'xmin' (int): The leftmost x coordinate of the bounding box.
                 'ymax' (int): The uppermost y coordinate of the bounding box.
                 'ymin' (int): The lowest y coordinate of the bounding box.

             width (int): The width of the jpeg image in pixels.
             height (int): The height of the jpeg image in pixels.
             valid_frame (bool): False if the target is present in the frame,
                 and True otherwise.
             OBS: If the target is not in the frame the bounding box information
             are all None.
   :rtype: annotation


.. py:function:: check_folder_tree(root_dir)

   Checks if the folder structure is compatible with the expected one.
   :param root_dir: (str) The path to the root directory of the dataset

   :returns: True if the structure is compatible, False otherwise.
   :rtype: bool


.. py:class:: Params(json_path)

   Class that loads hyperparameters from a json file.
   Example:
   ```
   params = Params(json_path)
   print(params.learning_rate)
   params.learning_rate = 0.5  # change the value of learning_rate in params
   ```


   .. py:method:: save(json_path)


   .. py:method:: update(json_path)

      Loads parameters from json file



   .. py:method:: update_with_dict(dictio)

      Updates the parameters with the keys and values of a dictionary.



   .. py:property:: dict

      Gives dict-like access to Params instance by `params.dict['learning_rate']


.. py:class:: RunningAverage

   A simple class that maintains the running average of a quantity

   Example:
   ```
   loss_avg = RunningAverage()
   loss_avg.update(2)
   loss_avg.update(4)
   loss_avg() = 3
   ```


   .. py:attribute:: steps
      :value: 0



   .. py:attribute:: total
      :value: 0



   .. py:method:: update(val)


.. py:function:: set_logger(log_path)

   Set the logger to log info in terminal and file `log_path`.
   In general, it is useful to have a logger so that every output to the
   terminal is saved in a permanent file.
   Example:
   ```
   logging.info("Starting training...")
   ```
   :param log_path: (string) where to log


.. py:function:: save_dict_to_json(d, json_path)

   Saves dict of floats in json file
   :param d: (dict) of float-castable values (np.float, int, float, etc.)
   :param json_path: (string) path to json file


.. py:function:: save_checkpoint(state, is_best, checkpoint)

   Saves model and training parameters at checkpoint + 'last.pth.tar'.
   If is_best==True, also saves checkpoint + 'best.pth.tar'
   :param state: (dict) contains model's state_dict, may contain other keys such
                 as epoch, optimizer state_dict
   :param is_best: (bool) True if it is the best
                   model seen till now
   :param checkpoint: (string) folder where parameters are
                      to be saved


.. py:function:: load_checkpoint(checkpoint, model, optimizer=None)

   Loads model parameters (state_dict) from file_path. If optimizer is
   provided, loads state_dict of optimizer assuming it is present in
   checkpoint.
   :param checkpoint: (string) filename which needs to be loaded
   :param model: (torch.nn.Module) model for which the parameters are loaded
   :param optimizer: (torch.optim) optional: resume optimizer from checkpoint


