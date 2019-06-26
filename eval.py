#!/usr/bin/env python3
""" A training program for MNASNet family of models.

All parameters are hardcoded for better reproducibility. This training harness
targets MNASNet with various depth multipliers. To change the depth multiplier,
simply set `MODEL_NAME` variable to the model you want. 4x1080ti are assumed.
Fewer GPUs will require smaller batches and smaller learning rates."""

import os
import typing
import math

import torch
import torchvision.models as models

import imagenet
import metrics
import log

IMAGENET_DIR = os.path.expanduser("~/datasets/imagenet")


def eval(model_name: str) -> None:
    if model_name == "mnasnet0_5":
        model = models.mnasnet0_5(num_classes=1000).cuda()
    elif model_name == "mnasnet0_75":
        model = models.mnasnet0_75(num_classes=1000).cuda()
    elif model_name == "mnasnet1_0":
        model = models.mnasnet1_0(num_classes=1000).cuda()
    elif model_name == "mnasnet1_3":
        model = models.mnasnet1_3(num_classes=1000).cuda()
    else:
        raise ValueError("Don't know how to evaluate {}".format(model_name))

    loss = torch.nn.CrossEntropyLoss().cuda()
    val_dataset = imagenet.validation(IMAGENET_DIR)
    all_metrics = metrics.default()

    model.eval()
    with torch.no_grad():
        val_losses = []
        metrics = collections.defaultdict(list)
        for batch_index, (inputs, truth) in enumerate(val_loader, 0):
            outputs = model(inputs.cuda()).cpu()
            val_losses.append(loss(outputs, truth).item())
            for name, metric_fn in metrics:
                metrics[name].append(metric_fn(outputs, truth))

        print(numpy.mean(val_losses), list([(name, numpy.mean(vals)) for name, vals in metrics.items()]))

if __name__ == "__main__":
    for m in ["mnasnet1_0", "mnasnet0_5"]:
        print("Evaluating pretrained", m)
        eval(m)
