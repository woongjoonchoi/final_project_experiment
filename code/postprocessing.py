from typing import Dict, Tuple
import numpy as np

from utils_qa import postprocess_qa_predictions
from arguments import DataTrainingArguments
from transformers import EvalPrediction, TrainingArguments

from datasets import load_metric


# Post-processing:
def post_processing_function(
        examples,
        features,
        predictions: Tuple[np.ndarray, np.ndarray],
        training_args: TrainingArguments,
    ) -> EvalPrediction:
    # Post-processing: start logits과 end logits을 original context의 정답과 match시킵니다.
    answer_column_name = "answers" if "answers" in examples.column_names else examples.column_names[2]

    predictions = postprocess_qa_predictions(
        examples=examples,
        features=features,
        predictions=predictions,
        max_answer_length=DataTrainingArguments.max_answer_length,
        output_dir=training_args.output_dir,
    )

    # Metric을 구할 수 있도록 Format을 맞춰줍니다.
    formatted_predictions = [
        {"id": k, "prediction_text": v} for k, v in predictions.items()
    ]
    
    if training_args.do_predict:
        return formatted_predictions

    # inference.py 실행 시 post_processing 합치면서 확실하지 않음
    elif training_args.do_eval:
        references = [
            {"id": ex["id"], "answers": ex[answer_column_name]}
            for ex in examples # for ex in datasets["validation"]
        ]
        return EvalPrediction(
            predictions=formatted_predictions, label_ids=references
        )

    
def compute_metrics(p: EvalPrediction) -> Dict:
    metric = load_metric("squad")

    return metric.compute(predictions=p.predictions, references=p.label_ids)