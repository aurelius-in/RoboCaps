import torch

from src.core.routing_attention import RoutingAttention


def test_routing_attention_shapes():
    batch, num_children, input_dim = 2, 64, 128
    num_parents, num_heads = 10, 4
    votes = torch.randn(batch, num_children, input_dim)
    ra = RoutingAttention(input_dim=input_dim, num_parents=num_parents, num_heads=num_heads)
    parents, attn = ra(votes)
    assert parents.shape == (batch, num_parents, input_dim)
    assert attn.shape == (batch, num_heads, num_parents, num_children)
