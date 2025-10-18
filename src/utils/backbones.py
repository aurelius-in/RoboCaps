from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Literal, Tuple

import torch
import torch.nn as nn
import torchvision.models as tvm


@dataclass
class BackboneOutput:
    features: torch.Tensor  # (batch, num_tokens, dim)
    feature_dim: int


class IdentityPool(nn.Module):
    def forward(self, x: torch.Tensor) -> torch.Tensor:  # noqa: D401
        return x


def vit_adapter(name: Literal["vit_b_16", "vit_l_16"] = "vit_b_16", pretrained: bool = True) -> Tuple[nn.Module, int, Callable[[torch.Tensor], BackboneOutput]]:
    model = getattr(tvm, name)(weights=getattr(tvm, f"{name.upper()}_Weights").DEFAULT if pretrained else None)
    dim = model.hidden_dim  # type: ignore[attr-defined]

    def forward(x: torch.Tensor) -> BackboneOutput:
        # Use vit.features to get token embeddings (including CLS)
        tokens = model._process_input(x)  # type: ignore[attr-defined]
        n = tokens.shape[0]
        cls_token = model.class_token.expand(n, -1, -1)
        x_tokens = torch.cat([cls_token, tokens], dim=1)
        x_tokens = model.encoder(x_tokens)  # type: ignore[attr-defined]
        return BackboneOutput(features=x_tokens, feature_dim=dim)

    return model, dim, forward


def convnext_adapter(name: Literal["convnext_tiny", "convnext_base"] = "convnext_tiny", pretrained: bool = True) -> Tuple[nn.Module, int, Callable[[torch.Tensor], BackboneOutput]]:
    model = getattr(tvm, name)(weights=getattr(tvm, f"{name.upper()}_Weights").DEFAULT if pretrained else None)
    # Convert final spatial map to tokens by flattening HxW
    dim = model.classifier[2].in_features  # type: ignore[index]

    def forward(x: torch.Tensor) -> BackboneOutput:
        feats = model.features(x)  # (b, c, h, w)
        b, c, h, w = feats.shape
        tokens = feats.flatten(2).transpose(1, 2)  # (b, h*w, c)
        return BackboneOutput(features=tokens, feature_dim=c)

    return model, dim, forward


def get_backbone(kind: Literal["vit", "convnext"], name: str, pretrained: bool = True):
    if kind == "vit":
        return vit_adapter(name=name, pretrained=pretrained)
    if kind == "convnext":
        return convnext_adapter(name=name, pretrained=pretrained)
    raise ValueError(f"Unsupported backbone kind: {kind}")
