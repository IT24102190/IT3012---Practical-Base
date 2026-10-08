from logic_engine import KnowledgeBase


def test_forward_chaining():
    kb = KnowledgeBase()

    # Domain Rules
    kb.tell_rule(
        ['TargetVisible', 'HasDust'],
        'SafeToEngage'
    )

    kb.tell_rule(
        ['SafeToEngage', 'BloodseekerMissing'],
        'Retreat'
    )

    # Test Case 1
    kb.clear_facts()

    kb.tell_fact('TargetVisible')
    kb.tell_fact('HasDust')

    kb.forward_chain()

    assert 'SafeToEngage' in kb.facts
    assert 'Retreat' not in kb.facts

    # Test Case 2
    kb.clear_facts()

    kb.tell_fact('TargetVisible')
    kb.tell_fact('HasDust')
    kb.tell_fact('BloodseekerMissing')

    kb.forward_chain()

    assert 'Retreat' in kb.facts

    print("All Logic Engine Test Cases Passed!")


if __name__ == "__main__":
    test_forward_chaining()