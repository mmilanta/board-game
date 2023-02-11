
export enum CellTerrain{
    See, Grass, Forest, Mountain, INVALID
}
export class Board{
    private board_data: CellTerrain[][];

    readonly width : number;
    readonly height : number;

    constructor(width:number, height:number){

        this.width = width
        this.height = height

        this.board_data = [];

        for(var i: number = 0; i < height; i++) {
            this.board_data[i] = [];
            for(var j: number = 0; j < width; j++) {
                this.board_data[i][j] = CellTerrain.Grass;
            }
        }
    }

    public get_cell(x:Coord):CellTerrain{
        if(this.check_coord(x))
            return this.board_data[x.row][x.col];
        else
            return CellTerrain.INVALID;
    }
    public check_coord(x:Coord):boolean{
        return (x.row >= 0 && x.row < this.height) && (x.col >= 0 && x.col < this.width)
    }
}
export const INVALID_MOVE = -1;
export const VALID_MOVE = 0;
export class Player{
    private game: Game;
    private id: number;
    constructor(game:Game, id:number){
        this.game = game;
        this.id = id;
    }
    public play(){
        this.game.move_unit(this.id, {row:0,col:0}, {row:1,col:1})
        this.game.end_turn(this.id)
        this.game.move_unit(this.id, {row:2,col:1}, {row:2,col:0})
        this.game.move_unit(this.id, {row:1,col:1}, {row:9,col:9})
        this.game.move_unit(this.id, {row:9,col:9}, {row:12,col:12})
        this.game.end_turn(this.id)
    }
}
export class Unit{
    constructor(){

    }
}
export type Coord = {
    row: number;
    col: number;
};
function isEqual(x: Coord, y:Coord):boolean{
    return x.row === y.row &&  x.col === y.col;
}

export class Game{
    private board: Board;
    private units: [Unit,Coord,number][]; // unit type, location of the unit, id of the player owning that unit
    private number_players: number;
    private playing_playerID: number;
    constructor(board: Board, number_players: number){
        this.board = board;
        this.number_players = number_players;
        this.units = [[new Unit(),{row: 0, col: 0} , 0]];
        this.playing_playerID = 0;
    }
    public end_turn(playerID: number): -1 | 0 {
        if (playerID !== this.playing_playerID)
            return INVALID_MOVE;
        else{
            this.playing_playerID += 1;
            if (this.playing_playerID >= this.number_players)
                this.playing_playerID = 0;
            console.log("player " + playerID + " turn ended")
            return VALID_MOVE
        }
    }
    public move_unit(playerID: number, from: Coord, to: Coord): -1 | 0 {
        if (playerID !== this.playing_playerID || !this.board.check_coord(from) || !this.board.check_coord(to) ){
            console.log("invalid move")
            return INVALID_MOVE;
        }
        // check if there is a unit of the correct player in from, and there is no unit in to.
        let valid_from :boolean = false;
        let valid_to :boolean = true;
        let unit_index :number = -1;
        for (let i = 0; i < this.units.length; i++){
            if (isEqual(this.units[i][1], from) && (this.units[i][2] === playerID)){
                valid_from = true;
                unit_index = i;
            }
            if (isEqual(this.units[i][1], to))
                valid_from = false;
        }
        if (!(valid_from && valid_to)){
            console.log("invalid move")
            return INVALID_MOVE;
        }
        this.units[unit_index][1] = to;
        console.log("unit moved from " + from.row +"-" + from.col + " to "+to.row +"-" + to.col )
        return VALID_MOVE;
    }
}