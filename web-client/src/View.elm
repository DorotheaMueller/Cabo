module View exposing (view)

import Html exposing (Html, div, p, h1, button, input, text, ul, li)
import Html.Attributes exposing (..)
import Html.Events exposing (onClick)
import Types exposing (..)


view : Model -> Html Msg
view model =
    div [] (List.indexedMap viewPlayer model.players)


viewPlayer : Int -> Player -> Html Msg
viewPlayer index player =
    div []
        [ h1 [] [ text player.name ]
        , p [] [ text <| toString player.score ]
        , button [ onClick (AddScore index) ] [ text "+1" ]
        , viewHand player.hand
        ]


viewHand : Hand -> Html a
viewHand hand =
    ul []
        [ li [] [ viewCard hand.card1 ]
        , li [] [ viewCard hand.card2 ]
        , li [] [ viewCard hand.card3 ]
        , li [] [ viewCard hand.card4 ]
        ]


viewCard : Card -> Html a
viewCard card =
    case card of
        Empty ->
            text "Empty"

        Unknown ->
            text "???"

        Card number ->
            text <| toString number
