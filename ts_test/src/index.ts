import {Game,Player,Board} from './board/board.js'

let g:Game = new Game(new Board(10,10), 1);
let p:Player = new Player(g, 0);
p.play()