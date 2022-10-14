"""
Created by Matthew Choy 27/09/2022 for COMP3710 - Pattern Recognition
This file should contain the data loader for loading and preprocessing your data.
"""
import requests
import zipfile
import functools
import pathlib
import shutil
from tqdm.auto import tqdm
import os
from os.path import exists

import torchvision

class ISIC():
    ISIC_TRAIN_IMG = "https://isic-challenge-data.s3.amazonaws.com/2017/ISIC-2017_Training_Data.zip"
    @staticmethod
    def download_dataset(url, filename):
        """
        Download a file from a URL, into a local file.
        :param url: The URL to download from
        :param filename: Filepath specifying the file to download into.
        """

        if exists(filename):
            print(f"[SKIP] Skipping download - file {filename} already exists")
            return
        # The following implementation was taken from StackOverflow:
        # https://stackoverflow.com/a/63831344/8214951
        r = requests.get(url, stream=True, allow_redirects=True)

        if r.status_code != 200:
            r.raise_for_status()
            raise RuntimeError(f"[FAIL] Request to {url} returned status code {r.status_code}")

        file_size = int(r.headers.get('Content-Length', 0))

        path = pathlib.Path(filename).expanduser().resolve()
        path.parent.mkdir(parents=True, exist_ok=True)

        desc = "(Unknown total file size)" if file_size == 0 else ""
        r.raw.read = functools.partial(r.raw.read, decode_content=True)  # Decompress if needed
        print("\tDownloading from", url, " to ", filename)
        with tqdm.wrapattr(r.raw, "read", total=file_size, desc=desc) as r_raw:
            with path.open("wb") as f:
                shutil.copyfileobj(r_raw, f)
        print("[ OK ] Download succeeded")

        return path

    @staticmethod
    def unzip(source_fp, dest_folder):
        """
        Unzip the contents of source_fp into a destination folder dest_folder
        :source_fp: The zip file to unzip
        :dest_folder: The directory to dump the contents of the zip file.
        """
        print("Unzipping ", source_fp, " to ", dest_folder)
        with zipfile.ZipFile(source_fp, "r") as z:
            for file in tqdm(iterable=z.namelist(), total=len(z.namelist())):
                z.extract(member=file, path=dest_folder)
        print("[ OK ] Unzip successful")

    def download(self):
        download_dataset(
            "https://isic-challenge-data.s3.amazonaws.com/2017/ISIC-2017_Training_Data.zip",
            self.location + "/train.zip")
        # unzip(self.location + "/train.zip", self.location)

        download_dataset(
            "https://isic-challenge-data.s3.amazonaws.com/2017/ISIC-2017_Training_Part1_GroundTruth.zip",
            self.location + "/train_res.zip"
    )
        # unzip(self.location + "/train_res.zip", self.location)

        download_dataset(
            "https://isic-challenge-data.s3.amazonaws.com/2017/ISIC-2017_Test_v2_Data.zip",
            self.location + "/test.zip"
        )
        # unzip(self.location + "/test.zip", self.location)

        download_dataset(
            "https://isic-challenge-data.s3.amazonaws.com/2017/ISIC-2017_Test_v2_Part1_GroundTruth.zip",
            self.location + "/test_res.zip"
        )
        # unzip(self.location + "/test_res.zip", self.location)

        # TODO -> Move unzipped contents of ./data/train_res into ./data/train
        #      -> Move unzipped contents of ./data/test_res  into ./data/test

    def __init__(self, download=True, location="./data/ISIC-2017"):
        self.location = location
        self.filenames = []
        self.train_loader = torchvision.datasets.ImageFolder(root="./data/ISIC-2017/train")
        self.test_loader = torchvision.datasets.ImageFolder(root="./data/ISIC-2017/test")
        # self.download()
        # For now, assume that the images are downloaded into the correct directory.
        pass

    def get_train_img(self, idx):
        return

    def __len__(self):
        return -1




if __name__ == "__main__":
    # Download and unzip the training dataset
    i = ISIC()
