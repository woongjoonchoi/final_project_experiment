import torch
from typing import Tuple
import sys
import os
from typing import Callable, List, Dict, NoReturn, Tuple
import pandas as pd
import json
from datasets import load_dataset
import numpy as np
import re

from .configure import configure_model
from transformers import (
    DataCollatorWithPadding,
    HfArgumentParser,
    TrainingArguments,
    set_seed,
)

# from .utils_qa import postprocess_qa_predictions, check_no_error
# from .trainer_qa import QuestionAnsweringTrainer
# from .sparse_retrieval import SparseRetrieval
# from .postprocessing import post_processing_function
from .run_mrc import run_combine_mrc
from .arguments import ModelArguments, DataTrainingArguments
from .run_retrieval import run_retrieval

parser = HfArgumentParser(
    (ModelArguments, DataTrainingArguments, TrainingArguments)
)
model_args, data_args, training_args = parser.parse_args_into_dataclasses()

set_seed(training_args.seed)


def load_model():
    model, tokenizer = configure_model(model_args, training_args, data_args)

    data_collator = DataCollatorWithPadding(
        tokenizer, pad_to_multiple_of=8 if training_args.fp16 else None
    )

    return model, tokenizer


def get_prediction(model, tokenizer, sentence):
    # 입력받은 sentence 정보를 datasets로 변환하기
    # dictionary -> json save -> load json to dataset
    sample_test = {"data": [
		{
			"id": "1",
			"question": sentence
		}]}

    print(sample_test)
    with open(os.path.join(data_args.dataset_name, 'sample_test.json'), "w", encoding='utf-8') as json_file:
        json.dump(sample_test, json_file, indent=4, sort_keys=True)

    datasets = load_dataset('json', data_files={'validation':os.path.join(data_args.dataset_name, 'sample_test.json')}, field='data')

    # Retrieval를 실행하여 관련 wiki news 가져오기
    datasets, context_list = run_retrieval(
            tokenizer,
            datasets,
            training_args,
            data_args,
    )

    predictions = run_combine_mrc(data_args, training_args, model_args, datasets, tokenizer, model)

    print(predictions)
    print(predictions[0]['prediction_text'])

    for c in context_list[0]:
        if re.search(predictions[0]['prediction_text'], c):
            context = c

    print(f"--------End Predict-----------")

    return context # predictions