# -*- coding: utf-8 -*-
import re

from .base import BaseConfig


class ReportsConfig(BaseConfig):

    def __init__(
        self,
        data_dir,
        image_w=2048,
        image_h=128,
        dataset_name="reports",
        chars="оеанисртвълкд1пмуг.яы2б-хйь3зч40,586 i79жѣюшщКВОСПцЕМНИ)Г/А:РТБДэУфЗЧ%№>;ЛЖЯI(ХЪФШЙ\"+Э'ЬЩЦVЫЮё^e|»c!=*X]<«tnbѵay?ojCsprhSzdkl{vJf[O§RBNUѳ}xPD~E",
        corpus_name="old_russian.txt",
        blank="ß",
        **kwargs,
    ):
        super().__init__(
            data_dir=data_dir,
            dataset_name=dataset_name,
            image_w=image_w,
            image_h=image_h,
            chars=chars,
            blank=blank,
            corpus_name=corpus_name,
            **kwargs,
        )

    def preprocess(self, text):
        """preprocess only train text"""
        text = text.strip()
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def postprocess(self, text):
        """postprocess output text"""
        text = text.strip()
        text = re.sub(r"\s+", " ", text)
        return text.strip()
