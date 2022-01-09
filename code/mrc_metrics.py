from datasets import (
    load_metric,
)


def postprocess_text(preds, labels):
    preds = [pred.strip() for pred in preds]
    labels = [label.strip() for label in labels]
    
    # preds = ["\n".join(tokenizer.tokenize(pred)) for pred in preds]
    # labels = ["\n".join(tokenizer.tokenize(label)) for label in labels]

    return preds, labels

def gen_metrics(tokenizer , valid_datasets) :

    metric = load_metric("squad") 
    def compute_metrics(eval_preds):
        import numpy as np
        preds, labels = eval_preds

        if isinstance(preds, tuple):
            preds = preds[0]

        max_val_samples = 16
        # breakpoint()

        # print(preds)
        # print(labels)

        decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)
        labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
        
        decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

        decoded_preds, decoded_labels = postprocess_text(decoded_preds, decoded_labels)
        
        formatted_predictions = [{"id": ex["id"], "prediction_text": decoded_preds[i]} for i, ex in         
                                 enumerate(valid_datasets.select(range(max_val_samples)))]
        references = [{"id": ex["id"], "answers": ex["answers"]} for ex in valid_datasets.select(range(max_val_samples))]
 
        result = metric.compute(predictions=formatted_predictions, references=references)

        return result
    return compute_metrics