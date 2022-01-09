import logging
import os
import sys

from typing import List, NoReturn, NewType, Any

from dataclasses import field
from datasets import load_metric, load_from_disk, Dataset, DatasetDict, load_dataset

from transformers import (
    DataCollatorForSeq2Seq,
    DataCollatorWithPadding,
    Seq2SeqTrainer,
    EvalPrediction,
    HfArgumentParser,
    TrainingArguments,
    set_seed, 
)

from configure import *
from preprocess import *
from postprocessing import post_processing_function, compute_metrics

from utils_qa import postprocess_qa_predictions, check_no_error
from trainer_qa import QuestionAnsweringTrainer

from arguments import (
    ModelArguments,
    DataTrainingArguments,
)

from run_mrc import run_combine_mrc, run_generation_mrc

logger = logging.getLogger(__name__)


def main():

    # print(datasets.__version__)
    parser = HfArgumentParser(
        (ModelArguments, DataTrainingArguments, TrainingArguments)
    )
    model_args, data_args, training_args = parser.parse_args_into_dataclasses()
    
    training_args.logging_steps = 20000
    training_args.save_steps = 20000
    training_args.save_total_limit = 10
    print(model_args.model_name_or_path)

    print(f"model is from {model_args.model_name_or_path}")
    print(f"data is from {data_args.dataset_name}")

    # logging 설정
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s -    %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # verbosity 설정 : Transformers logger의 정보로 사용합니다 (on main process only)
    logger.info("Training/evaluation parameters %s", training_args)

    # 모델을 초기화하기 전에 난수를 고정합니다.
    set_seed(training_args.seed)

    # datasets = load_from_disk(data_args.dataset_name)
    PATH = data_args.dataset_name
    datasets = load_dataset('json', data_files={'train':os.path.join(PATH, 'train.json'), 'validation': os.path.join(PATH, 'valid.json')}, field='data')
    print(datasets)
    
    datasets['train'] = datasets['train'].shuffle(seed=42).select(range(10000))
    datasets['validation'] = datasets['validation'].shuffle(seed=42).select(range(1000))

    model, tokenizer = configure_model(model_args, training_args, data_args)
    print(
        type(training_args),
        type(model_args),
        type(datasets),
        type(tokenizer),
        type(model),
    )

    # do_train mrc model 혹은 do_eval mrc model
    if training_args.do_train or training_args.do_eval:
        if model_args.run_extraction:
            run_combine_mrc(data_args, training_args, model_args, datasets, tokenizer, model)
        elif model_args.run_generation:
            run_generation_mrc(data_args, training_args, model_args, datasets, tokenizer, model)


if __name__ == "__main__":
    main()
