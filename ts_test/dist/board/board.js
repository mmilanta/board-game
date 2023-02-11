export var CellTerrain;
(function (CellTerrain) {
    CellTerrain[CellTerrain["See"] = 0] = "See";
    CellTerrain[CellTerrain["Grass"] = 1] = "Grass";
    CellTerrain[CellTerrain["Forest"] = 2] = "Forest";
    CellTerrain[CellTerrain["Mountain"] = 3] = "Mountain";
    CellTerrain[CellTerrain["INVALID"] = 4] = "INVALID";
})(CellTerrain || (CellTerrain = {}));
export class Board {
    constructor(width, height) {
        this.width = width;
        this.height = height;
        this.board_data = [];
        for (var i = 0; i < height; i++) {
            this.board_data[i] = [];
            for (var j = 0; j < width; j++) {
                this.board_data[i][j] = CellTerrain.Grass;
            }
        }
    }
    get_cell(x) {
        if (this.check_coord(x))
            return this.board_data[x.row][x.col];
        else
            return CellTerrain.INVALID;
    }
    check_coord(x) {
        return (x.row >= 0 && x.row < this.height) && (x.col >= 0 && x.col < this.width);
    }
}
export const INVALID_MOVE = -1;
export const VALID_MOVE = 0;
export class Player {
    constructor(game, id) {
        this.game = game;
        this.id = id;
    }
    play() {
        this.game.move_unit(this.id, { row: 0, col: 0 }, { row: 1, col: 1 });
        this.game.end_turn(this.id);
        this.game.move_unit(this.id, { row: 2, col: 1 }, { row: 2, col: 0 });
        this.game.move_unit(this.id, { row: 1, col: 1 }, { row: 9, col: 9 });
        this.game.move_unit(this.id, { row: 9, col: 9 }, { row: 12, col: 12 });
        this.game.end_turn(this.id);
    }
}
export class Unit {
    constructor() {
    }
}
function isEqual(x, y) {
    return x.row === y.row && x.col === y.col;
}
export class Game {
    constructor(board, number_players) {
        this.board = board;
        this.number_players = number_players;
        this.units = [[new Unit(), { row: 0, col: 0 }, 0]];
        this.playing_playerID = 0;
    }
    end_turn(playerID) {
        if (playerID !== this.playing_playerID)
            return INVALID_MOVE;
        else {
            this.playing_playerID += 1;
            if (this.playing_playerID >= this.number_players)
                this.playing_playerID = 0;
            console.log("player " + playerID + " turn ended");
            return VALID_MOVE;
        }
    }
    move_unit(playerID, from, to) {
        if (playerID !== this.playing_playerID || !this.board.check_coord(from) || !this.board.check_coord(to)) {
            console.log("invalid move");
            return INVALID_MOVE;
        }
        let valid_from = false;
        let valid_to = true;
        let unit_index = -1;
        for (let i = 0; i < this.units.length; i++) {
            if (isEqual(this.units[i][1], from) && (this.units[i][2] === playerID)) {
                valid_from = true;
                unit_index = i;
            }
            if (isEqual(this.units[i][1], to))
                valid_from = false;
        }
        if (!(valid_from && valid_to)) {
            console.log("invalid move");
            return INVALID_MOVE;
        }
        this.units[unit_index][1] = to;
        console.log("unit moved from " + from.row + "-" + from.col + " to " + to.row + "-" + to.col);
        return VALID_MOVE;
    }
}
//# sourceMappingURL=board.js.map