$(document).ready(() => {

    //create element of type e and get a jquery selector to it
    function c(e){
        return $(document.createElement(e));
    }

    var state = null; //
    var player = null; //selected player - 1 or 2


    function loadState(){
        $.get("/state", (data) => {
            let grid = $('#game-grid').empty();
            state = data;
            for(r=0; r<state.grid.length; r++){
                let row = c('div').appendTo(grid);
                row.addClass('game-row');
                for(let t=0; t<state.grid[r].length; t++){
                    let tile = c('div').appendTo(row);
                    tile.addClass('game-tile').addClass(`player${state.grid[r][t]}`);
                    if(state.current_player == player){
                        tile.click(()=>{
                            $.get(`/place?player=${player}&col=${t}`, loadState);
                        });
                    }
                }
            }
            message = $('#message').empty();
            message_text = c('span').appendTo(message);
            if(state.winner){
                message_text.text((state.winner == player) ? "you win" : "you lose")
            }
            else{
                if(state.current_player == player){
                    message_text.addClass(`player${player}`).text('your turn');
                }
                else{
                    message_text.text("other player's turn")
                }
            }
        });

    }

    // create player-selector buttons
    for(let i = 1; i<=2; i++){
        c('div').addClass('game-tile').addClass(`player${i}`).appendTo($('#player-selector')).click(() => {
            // on click, set the current player and remove the buttons
            player = i;
            $('#player-selector').remove();
            window.setInterval(loadState, 1500);
            loadState();
        });
    }

    $('#new-game').click(() => {
        $.get('/new_game', loadState)
    });

});
