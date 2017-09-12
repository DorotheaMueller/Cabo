module Parsing exposing (hand)

import Json.Decode as Json
import Types exposing (..)


hand : Json.Decoder Hand
hand =
    Json.map4
        (\a b c d ->
            { card1 = a, card2 = b, card3 = c, card4 = d }
        )
        (Json.field "card1" card)
        (Json.field "card2" card)
        (Json.field "card3" card)
        (Json.field "card4" card)


card : Json.Decoder Card
card =
    Json.map (Card) Json.int
