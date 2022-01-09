import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from transformers import AutoModel, AutoTokenizer

from app.utils import load_data


def get_cls_token(model, tokenizer, sentence):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(device)
    model.to(device)

    model.eval()
    tokenized_sent = tokenizer(
            sentence,
            return_tensors="pt",
            truncation=True,
            add_special_tokens=True,
            max_length=128
    ).to(device)
    with torch.no_grad():
        outputs = model(
            input_ids=tokenized_sent['input_ids'],
            attention_mask=tokenized_sent['attention_mask'],
            token_type_ids=tokenized_sent['token_type_ids']
        )

    logits = outputs.last_hidden_state[:, 0, :].detach().cpu().numpy()

    return logits


def get_prediction(sentence):
    questions, answers = load_data()
    
    model = AutoModel.from_pretrained('klue/bert-base')
    tokenizer = AutoTokenizer.from_pretrained('klue/bert-base')
    
    query_cls_hidden = get_cls_token(model, tokenizer, sentence)
    dataset_cls_hidden = []

    for q in questions:
        q_cls = get_cls_token(model, tokenizer, q)
        dataset_cls_hidden.append(q_cls)
    dataset_cls_hidden = np.array(dataset_cls_hidden).squeeze(axis=1)

    cos_sim = cosine_similarity(query_cls_hidden, dataset_cls_hidden)
    top_question = np.argmax(cos_sim)

    return sentence, answers[top_question]