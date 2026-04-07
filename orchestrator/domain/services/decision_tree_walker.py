"""
Domain Service: Decision Tree Walker

Generic, reusable traversal engine for JSON decision trees.
Eliminates the ~1,500 lines of duplicated traverse_* functions in the
legacy CoreEngine by providing a single, parameterized walker.

Decision Tree Format (expected JSON structure)
----------------------------------------------
{
    "nodes": {
        "root":   {"question": "...", "options": {"yes": "next_node", "no": "leaf_X"}},
        "nodeB":  {"question": "...", "options": {"yes": "leaf_Y", "no": "leaf_Z"}}
    },
    "leaves": {
        "leaf_X": {"strategy": "...", "reasoning": "...", ...},
        "leaf_Y": {"strategy": "...", "reasoning": "...", ...}
    }
}
"""

from typing import Any, Callable, Dict, Optional
import logging

logger = logging.getLogger(__name__)

# Type alias for the question resolver callback.
# Given a node_id and the full metrics dict, returns the answer string.
QuestionResolver = Callable[[str, Dict[str, Any]], str]


def walk_decision_tree(
    tree: Dict[str, Any],
    question_resolver: QuestionResolver,
    metrics: Dict[str, Any],
    *,
    start_node: str = "root",
    default_leaf_key: Optional[str] = None,
    nodes_key: str = "nodes",
    leaves_key: str = "leaves",
    max_depth: int = 50,
) -> Dict[str, Any]:
    """Walk a JSON decision tree and return the matched leaf.

    Parameters
    ----------
    tree:
        Parsed JSON decision tree with ``nodes`` and ``leaves`` sections.
    question_resolver:
        Callback ``(node_id, metrics) -> answer_string`` that maps each
        decision node to the answer used for routing.
    metrics:
        Runtime metrics dictionary passed to the ``question_resolver``.
    start_node:
        Entry node for the traversal (default ``"root"``).
    default_leaf_key:
        Fallback leaf key if the traversal fails to reach a leaf.
    nodes_key:
        Key in ``tree`` that holds the nodes dictionary.
    leaves_key:
        Key in ``tree`` that holds the leaves dictionary.
    max_depth:
        Safety limit to prevent infinite loops in malformed trees.

    Returns
    -------
    dict
        The matched leaf dictionary (content from ``tree[leaves_key][leaf_id]``).
        An additional ``"_leaf_id"`` key is injected for downstream identification.

    Raises
    ------
    ValueError
        If the tree is malformed or traversal fails without a default.
    """
    nodes = tree.get(nodes_key, tree)  # Some trees have flat structure
    leaves = tree.get(leaves_key, {})

    current = start_node
    depth = 0

    while depth < max_depth:
        depth += 1

        # Check if we've reached a leaf
        if current in leaves:
            leaf = dict(leaves[current])  # shallow copy
            leaf["_leaf_id"] = current
            return leaf

        # Check if it's a valid node
        if current not in nodes:
            break

        node = nodes[current]

        # Resolve the answer for this node
        try:
            answer = question_resolver(current, metrics)
        except Exception as e:
            logger.warning(
                "Question resolver failed for node '%s': %s. "
                "Defaulting to 'no'.",
                current,
                e,
            )
            answer = "no"

        # Navigate to the next node/leaf
        options = node.get("options", {})
        next_step = options.get(answer)

        if next_step is None:
            # Try fallback to 'no' if the answer key doesn't exist
            next_step = options.get("no")
            if next_step is None:
                logger.warning(
                    "No valid transition from node '%s' with answer '%s'. "
                    "Available options: %s",
                    current,
                    answer,
                    list(options.keys()),
                )
                break

        # Check if next_step is a leaf directly
        if next_step in leaves:
            leaf = dict(leaves[next_step])
            leaf["_leaf_id"] = next_step
            return leaf

        current = next_step

    # Fallback
    if default_leaf_key and default_leaf_key in leaves:
        logger.info(
            "Traversal did not reach a leaf; using default '%s'.",
            default_leaf_key,
        )
        leaf = dict(leaves[default_leaf_key])
        leaf["_leaf_id"] = default_leaf_key
        return leaf

    raise ValueError(
        f"Decision tree traversal failed: ended at '{current}' "
        f"after {depth} steps with no matching leaf. "
        f"Available leaves: {list(leaves.keys())}"
    )


def build_simple_resolver(
    question_map: Dict[str, Callable[[Dict[str, Any]], str]],
    default_answer: str = "no",
) -> QuestionResolver:
    """Build a QuestionResolver from a simple mapping of node_id → lambda.

    Parameters
    ----------
    question_map:
        Dictionary mapping node IDs to callables that accept ``metrics``
        and return the answer string.
    default_answer:
        Answer returned when a node_id is not in the map.

    Returns
    -------
    QuestionResolver
        A callable suitable for ``walk_decision_tree``.

    Example
    -------
    >>> resolver = build_simple_resolver({
    ...     "root": lambda m: "yes" if m.get("is_critical") else "no",
    ...     "scale_check": lambda m: "yes" if m.get("large_scale") else "no",
    ... })
    """

    def resolver(node_id: str, metrics: Dict[str, Any]) -> str:
        fn = question_map.get(node_id)
        if fn is not None:
            return fn(metrics)
        return default_answer

    return resolver
