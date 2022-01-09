from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ModelArguments:
    """
    Arguments pertaining to which model/config/tokenizer we are going to fine-tune from.
    """

    model_name_or_path: str = field(
        default="klue/bert-base",
        metadata={
            "help": "Path to pretrained model or model identifier from huggingface.co/models"
        },
    )
    config_name: Optional[str] = field(
        default=None,
        metadata={
            "help": "Pretrained config name or path if not the same as model_name"
        },
    )
    tokenizer_name: Optional[str] = field(
        default=None,
        metadata={
            "help": "Pretrained tokenizer name or path if not the same as model_name"
        },
    )
    run_extraction: bool = field(
        default=True,
        metadata={
            "help": "Run Extraction based model"
        },
    )
    run_generation: bool = field(
        default=False,
        metadata={
            "help": "Run Generation based model"
        },
    )


@dataclass
class DataTrainingArguments:
    """
    Arguments pertaining to what data we are going to input our model for training and eval.
    """

    dataset_name: Optional[str] = field(
        default='../data/train', #"../data/train/train_data",
        metadata={"help": "The name of the dataset to use."},
    )
    overwrite_cache: bool = field(
        default=False,
        metadata={"help": "Overwrite the cached training and evaluation sets"},
    )
    preprocessing_num_workers: Optional[int] = field(
        default=None,
        metadata={"help": "The number of processes to use for the preprocessing."},
    )
    max_seq_length: int = field(
        default=384,
        metadata={
            "help": "The maximum total input sequence length after tokenization. Sequences longer "
            "than this will be truncated, sequences shorter will be padded."
        },
    )
    pad_to_max_length: bool = field(
        default=False,
        metadata={
            "help": "Whether to pad all samples to `max_seq_length`. "
            "If False, will pad the samples dynamically when batching to the maximum length in the batch (which can "
            "be faster on GPU but will be slower on TPU)."
        },
    )
    doc_stride: int = field(
        default=128,
        metadata={
            "help": "When splitting up a long document into chunks, how much stride to take between chunks."
        },
    )
    max_answer_length: int = field(
        default=30,
        metadata={
            "help": "The maximum length of an answer that can be generated. This is needed because the start "
            "and end predictions are not conditioned on one another."
        },
    )
    eval_retrieval: bool = field(
        default=True,
        metadata={"help": "Whether to run passage retrieval using sparse embedding."},
    )
    num_clusters: int = field(
        default=64, metadata={"help": "Define how many clusters to use for faiss."}
    )
    top_k_retrieval: int = field(
        default=1,
        metadata={
            "help": "Define how many top-k passages to retrieve based on similarity."
        },
    )

    sparse_name: Optional[str] = field(
        default='elastic',
        metadata={
            "help": "Sparse module option. (None, elastic)"
        },
    )

    dense_name: Optional[str] = field(
        default='None',
        metadata={
            "help": "Dense module option. (None, in-batch)"
        },
    )
    run_seq2seq : bool = field(
        default=False, metadata={"help": "Whether to seq2seq or EncoderDecoder"}
    )

'''
학습 방법
python train_copy.py --output_dir ./models/train_dataset --do_train --overwrite_cache --overwrite_output_dir

평가 방법
python train_copy.py --output_dir ./outputs/train_dataset --model_name_or_path ./models/train_dataset/ --do_eval --overwrite_cache --overwrite_output_dir

추론 방법
python inference_copy.py --output_dir ./outputs/test_dataset/ --dataset_name ../data/test_dataset/ --model_name_or_path ./models/train_dataset/ --do_predict  --overwrite_cache --overwrite_output_dir

앱실행 방법
streamlit run prototype.py --server.address=127.0.0.1 -- --output_dir ./outputs/test_dataset/ --model_name_or_path ./models/train_dataset/ --dataset_name ../data/test_dataset/ --do_predict

(model option : wjc123/qa_finetuned)
'''