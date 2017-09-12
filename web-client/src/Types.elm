module Types exposing (..)


type Card
    = Card Int
    | Unknown
    | Empty


type alias Hand =
    { card1 : Card
    , card2 : Card
    , card3 : Card
    , card4 : Card
    }


empty_hand : Hand
empty_hand =
    { card1 = Empty, card2 = Empty, card3 = Empty, card4 = Empty }


type alias Player =
    { name : String
    , score : Int
    , hand : Hand
    }


default_player : Player
default_player =
    { name = "", score = 0, hand = empty_hand }


type Msg
    = AddScore Int
    | HandFileRecieved String


type alias Model =
    { players : List Player }


default_model : Model
default_model =
    { players =
        [ { default_player | name = "Doro" }
        , { default_player | name = "Sara" }
        ]
    }
