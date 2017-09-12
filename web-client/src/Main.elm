module Main exposing (..)

import Types exposing (..)
import View
import Html
import List.Extra as List
import Http
import Parsing


main =
    Html.program
        { init = init
        , view = View.view
        , update = update
        , subscriptions = subscriptions
        }


init : ( Model, Cmd Msg )
init =
    default_model
        ! [ Http.send handFileResultToMessage getHandFile
          ]


getHandFile : Http.Request Hand
getHandFile =
    Http.get "http://localhost:8000/web-client/resources/hand.json" Parsing.hand


handFileResultToMessage : Result a Hand -> Msg
handFileResultToMessage result =
    case result of
        Err e ->
            HandFileRecieved <| toString e

        Ok hand ->
            HandFileRecieved <| toString hand



-- UPDATE


increaseScore : Int -> List Player -> List Player
increaseScore index players =
    players
        |> List.updateAt index
            (\player -> { player | score = player.score + 1 })
        |> Maybe.withDefault players


update : Msg -> Model -> ( Model, Cmd Msg )
update action model =
    case action of
        AddScore index ->
            { model | players = increaseScore index model.players } ! []

        HandFileRecieved content ->
            Debug.log content (model ! [])


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none
