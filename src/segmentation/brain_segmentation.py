import os
from src.common.io.command_operations import run_commands
from src.common.io.path_operations import (
    extract_save_dir_from_path,
    extract_subject_id_from_file_path,
    get_file_list_from_pattern,
)
import logging


class BrainExtractor:
    """
    Extracts the brain from a T1 image using the CaPTk Deep Learning model.
    """

    def __init__(self):
        pass

    def run(self, pattern: str):
        """
        Run the brain extraction on a list of T1 images.

        Args:
            pattern (str): pattern to get the list of T1 images
        """

        t1_path_list = get_file_list_from_pattern(pattern)

        commands = []

        for t1_path in t1_path_list:

            subject_id, _ = extract_subject_id_from_file_path(t1_path)

            save_directory = extract_save_dir_from_path(t1_path)

            logging.info(f"Save directory:{save_directory}")

            output_folder = os.path.join(save_directory, "brain_extraction_outputs")
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            output_patient_folder = os.path.join(output_folder, subject_id)
            if not os.path.exists(output_patient_folder):
                os.makedirs(output_patient_folder)

            logging.info("Creating command for:" + t1_path)

            command = self.create_CaPTk_command(t1_path, output_patient_folder)

            logging.info("Command:" + command)

            commands.append(command)

        run_commands(commands)

        logging.info("Brain extraction was successful.")

    def create_CaPTk_command(self, t1_path: str, output_patient_folder: str):
        """
        Create a CaPTk Skull strip command for a T1 image.

        Args:
            t1_path (str): path to the T1 image

        Returns:
            str: command
        """

        logging.info("Output folder:" + output_patient_folder)

        output_file = f"{output_patient_folder}/brain_mask.nii.gz"

        command = (
            "/work/CaPTk/bin/install/appdir/usr/bin/DeepMedic"
            + " -i "
            + t1_path
            + " -o "
            + output_file
            + " -md "
            + "/work/CaPTk/bin/install/appdir/usr/data/deepMedic/saved_models/skullStripping_modalityAgnostic"
        )

        return command
