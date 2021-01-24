When
    [Case
        (Deposit
            (Role "seller")
            (Role "seller")
            (Token "" "")
            (Constant 100)
        )
        (When
            [Case
                (Choice
                    (ChoiceId
                        "refund"
                        (Role "buyer")
                    )
                    [Bound 0 2]
                )
                (If
                    (ValueEQ
                        (ChoiceValue
                            (ChoiceId
                                "refund"
                                (Role "buyer")
                            ))
                        (Constant 1)
                    )
                    Close 
                    (If
                        (ValueEQ
                            (ChoiceValue
                                (ChoiceId
                                    "refund"
                                    (Role "buyer")
                                ))
                            (Constant 2)
                        )
                        (Pay
                            (Role "seller")
                            (Party (Role "buyer"))
                            (Token "" "")
                            (Constant 90)
                            Close 
                        )
                        (Pay
                            (Role "seller")
                            (Party (Role "buyer"))
                            (Token "" "")
                            (Constant 75)
                            Close 
                        )
                    )
                )]
            30 Close 
        )]
    1 Close 