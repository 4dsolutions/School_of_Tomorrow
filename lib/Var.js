//Var*.js, opensource/Apache2 (versions before Bellsack256/2025-8-3 are MIT) by Ben F Rayfield

//copied (then maybe modified) from VarTree_002.html 2025-7-5.
//Var class was copied 2025-4-16 from blobMonstersGame_2025-3-27.html then modified TODO...
//
//this is a named var in gob.brain(...vars). It may modify .kv .dp .dv .mn .mx and .poten
//but NOT .p and NOT .v cuz that happens after a block of calculations in var.nextState(dt)
//so order of calling gob.brain(...vars) of many gobs and Vars, has no effect except float64 roundoff.
//Also dont modify prevP, epsilon, accelMul, or gp. Those are set externally.
//TODO over time, remove this.gob/optionalGob and use ONLY Var, and same for Game and other classes.
//They were made first, then redesigned as Var is their data format but its also a fast param like centerY.p.
//So far the tree is entirely organized by root.namespace.object.field, which is a Var tree 3 deep, as you see
//in the pic of json, but it can be any tree shape. Each var has a position, velocity, and 0 or more named childs.
//https://x.com/benrayfield/status/1877462454222958657 2025-1-9.
//
//To add new code, you move in a many dimensional space. Each possible code string is hashed to name
//it as a dimension. Position in that dimension means does the code exist or not. Child dimensions are its
//parameters, part of the high dimensional game state vector. It returns list or Int32Array of int voxels.
//You just write a javascript function of any parameters you want (Var instances which have
//position and velocity) and generate whatever pic you want based on that. The params will automatically
//change so the pics come to life.
//
const Var = function(optionalParentVar, optionalName, optionalBig, optionalGob){

	//fixme remove Var.brain cuz Var.getOb().brain would be that if ob is a Gob,
	//and remove Var.vars cuz thats now Var.pu aka the opposite spelling of Var.up.
	//this.brain = null; //where compiled (this.big || this.name) goes, normally a js func of Var's to list/array of int voxels.
	//this.vars = null;
	
	//If this.name is a hash id (or might be prefixed with something? todo), then its the hash of this.big which is probably a string of json (see Dagverse json norming, in dagball, TODO).
	//This must be verifiable. Dont just make up a name and make up a big that cant prove that its name is the hash of that.
	this.big = optionalBig || null;
	this.t = 0; //not used as of 2025-2-20 even though some code copies it, maybe later? TODO actual current time //TODO? this.t = utc time as float64 so has at least microsecond precision for 100+ more years.
	
	//TODO? this.ch = [] child vars list (gob.vars if this is gob.influence), if this is a .influence var
	//that is 1 for this thing exists and 0 for does not exist.
	//so there is 1 correct answer, or it should converge, to what .p and .v should a var be at time t
	//TODO? this.ns = string namespace, like game.ns.
	//TODO? this.pk = primaryKey of this Var. or should that be per scalar instead of per Var?
	//should pk depend on namespace? be concat to that? or what? pk certainly should not depend on t/time.
	this.name = optionalName || 'v'+(++generatedNameCounter);
	this.cache = {}; //holds constY and constX if this wraps a tile
	if(this.name.startsWith('tile')){
		if(isTileString(this.name)){
			let square = tileStringToSquare(this.name);
			this.cache.constY = SquareMidY(square);
			this.cache.constX = SquareMidX(square);
			//let yOfTopLeftCorner = SquareY(square);
			//let xOfTopLeftCorner = SquareX(square);
			//for Var.y() when Var.ob would be a QuadTile since it doesnt have Y and X Var childs cuz its in the square number instead
			//cant use this.constY cuz it will make a Var instance and put it in this.pu.constY
			//this.constY = yOfTopLeftCorner;
			//this.constX = xOfTopLeftCorner; //for Var.x()
			//this.cache.constY = yOfTopLeftCorner;
			//this.cache.constX = yOfTopLeftCorner;
		}
	}

	/*Should Var also have a namespace (game.ns) so can make up new vectors without affecting the current game? ... TODO something like this?... /namespaceABC/game/distToPoten0 /namespaceABC/game/distToPoten1023 /namespaceABC/monster567sHashId/centerY /namespaceABC/monster567sHashId/centerX /namespaceABC/monster567sHashId/heightToWidthRatio, and each of those refers to a Var. That could be its primaryKey. /namespaceABC/monster567sHashId would also be a Var and is the .influence of that gob, and thatGob.vars would be its childs including /namespaceABC/monster567sHashId/heightToWidthRatio which is a Var.
	*/
	this.up = optionalParentVar || null;
	if(!this.up && this.name != 'V'){ //FIXME remove this. The V global var is root of all Vars, but someone might rename it something else, who knows. This is a test to find those not in the tree at all 2024-11-21.
		throw new Error('Var not in the tree: '+this.path());
	}
	//path height. V is height 0. V.testnet aka namespace is height 1. and so on.
	//Gobs normally go at height 2. Gob fields height 3.
	this.h = this.up ? this.up.h+1 : 0;
	
	if(this.name=='Y' && this.h==2){
		throw new Error('Var named '+this.name+' as child in namespace. should be 1 deeper.');
	}
	
	//pu is opposite of up aka down.
	//TODO make a {} whose Object.getPrototypeOf is custom built so any field that doesnt exist automatically creates
	//a Var instance as that child with that name and this Var as its parent and its .p of 0 and .v of 0 and other defaults.
	this.pu = {}; //mape of childVar.name to childVar.//this.down = {}; //mape of childVar.name to childVar.
	
	//2025-2-6+ will probably keep Var.ob as it can be Gob or Game instance
	//(like V.testnet.game.getOb() is a Game and sets V.testnet.game.ob and returns from that on next call of getOb()),
	//maybe other types later too. If you just type V.someOtherNamespace567.game.getOb() that should also make a Game instance.
	//TODO this field Var.gob will be removed???, Var class replaces Gob class. parent is this.up. childs are in this.pu.
	//can put same fields in Var as long as they're deriveable by Var.p Var.v Var.name Var.big etc.
	//The root (V) Var, and a namespace Var (like V/blobMonstersGameDefaultNamespace), dont have a Gob.
	//Its 1 layer deeper (theGobVar itself instead of gob.instance), and inside that is gob.vars.
	this.ob = null; //Gob or Game instance, whose parent Var is the same such as V.testnet: this.gob = optionalGob || null;
	
	this.p = 0; //position
	this.v = 0; //velocity
	this.kv = 0; //velocity continuous decay per second, using this.v *= Math.exp(-dt*this.kv)
	this.dp = 0; //diffeq, extra change of p per second See pinballBumper in dagball.
	this.dv = 0; //diffeq, extra change of v per second. See pinballBumper in dagball.
	//dv is this i think, dont need da: this.da = 0; //da accel. dv velocity. dp position. so dv += da*dt; then dp += dv*dt; so we dont need dt param to accelerate by game.gravY.p.
	this.gr = 0; //same as (negative) .dv but duplicates it cuz this stores gradient separately, and .dv can be set by gob.brain(...vars).
	this.prevGr = this.gr; //for debug/logging. Has no effect on physics. Its just that .gr gets erased often.
	this.mn = -Infinity; //for truncating this.p to Math.max(this.mn, Math.min(this.p, this.mx)). mn is min. mx is max.
	this.mx = Infinity; //for truncating this.p
	//you only need to add to poten in 1 Var but could do it in all of them. will just get summed.
	//This is extra poten, not including game.poten. Normally you just add to the first var's poten, if you do it at all.
	//You can put things here like spring forces or up to NP-complete and fourier math etc, anything by least-squares etc.
	this.poten = 0;
	this.prevP = 0; //stores the prev value of this.p while an epsilon is added to this.p during a gradient calculation, then restore it
	this.epsilon = DefaultEpsilon; //FIXME, replacement for indexToEpsilon
	this.accelMul = 1; //FIXME, replacement for indexToAccelMul
	//use this.brain instead: this.evaled = null; //eval of this.big || this.name, a js lambda whose params are all Var objects, those in this.influence.vars or gob.vars
	
	/* A tighter security copy of this.p, that may differ from this.p like by game.sparseUpdate() or game.tryEval(string) etc.
	Decides if its evaled into local game state or removed. Should try to stay equal to this.p if this.y() this.x() is near enough to view.
	
	2025-2-18 mmMain:redesignDisorganizedBuggyTiles2025-2-18+ which led to the creation
	of Var.e and TODO Var.setE(number) or something like that TODO.
	
	Ive probably broken the loading of tiles again but ive got to mmMain:"fix why the tiles are appearing/disappearing approx like they should but at a few hundred pixels past where the gobs appear/disappear at the sparse distance (see sparseUpdate)"

	This whole tile thing is getting too complex. Its time for a small redesign, to get things straight in the design before writing more code. Its too many places things are being stored:
	Var.ob is a QuadTile, which has a square (uint53) and a Quad.
	game.wal is a BigTile containing Tile's.
	tile.dense is a 128x128 byte array.
	tile.sparse is a Quad.
	game.board is modified by a Quad in Tile.prototype.paintGame and it remembers that in tile.lastPaintedQuadOnGame (similar to gob.voxInGame int array but its a Quad instead).

	Theres also autoEval in Var.

	Theres Var.p NOT being used for create/delete at height 2 (V.testnet.objectName.p). State was supposed to be in the Var tree but some parts are not, and its causing an avalanche of cache errors that confusing me and getting way too much stuff tangled.
	Maybe I need a bit field in Var to say if its in the game or not, or a scalar field to say gradually how much, 0 to 1 in the simplest case.
	I recently changed Gob to not change its Var (gob.bo is a Var whose Var.ob is that Gob) when you edit the textarea. The var changes, but its a new Gob. Similarly, I dont want state stored in Tile thats not in Var, which might mean I have to redesign how you paint on BigTile to queue updates in some other structure and do them all at once (before next video frame).

	These redesigns wont be covered here[[[
	wikib upgrades.
	gob.m.IsSelected etc put in the Var tree.
	redesign gob.brain funcs to not modify their param Vars and instead be a pure-function (except maybe the mouse gob that reads Controls.mouseY etc) but I dont know how to do that efficiently.
	]]]

	This might turn into a bigger redesign than I thought, but think thru it carefully. In general I think I want to make game.wal (which is a BigTile) be a backing wrapper of the V/Var tree instead of storing out of sync caches of it, and I likely want another upgrade to the Var class which is Var.pExistsInGame but find something smaller to write it as maybe p.e. Yes, lets call it p.e for amount of eval, thats supposed to usually be the same as .p but .e goes thru more security checks, while .p can be changed by merging V tree across internet, its only evaled (TODO) into game.board etc	if !!p.e where p.e is normally 0 or 1. Also, we dont share Var.e across internet cuz its about local views of the Var tree, such as viewing it in a specific game.board game.gobs game.wal etc.
	...
	And im gonna need events to update things whenever .e changes, so .setE func instead of setting .e directly?
	*/
	this.e = 0;
	
	//gp works. it makes the gobs voxels overlap eachother less and bounce better. keep it. now is 2025-1-16.
	//gp: Like -dt*gr (gradient) usually goes into velocity, this part goes into position. p += -dt*gp.
	//This is an experimental field of Var added 2024-11-13 to try to solve that gobs overlap too much, take too long to accel away from eachother,
	//so this should slightly make them instantly jump away from eachother too.
	//I just doubled constraint solving efficiency of Blob Monster Game in 2 lines of code, in Var class:
	//"this.gp = 1.5; //TODO this.gp = 0;" and "let nextP = this.p + dt*(this.v+this.dp-this.gp*this.gr);".
	//Now they overlap less. https://pic.x.com/7OjEWfA9hC (2024_pic.x.comSLASH7OjEWfA9hC.png)
	//This might be useful as a neuralnet param, built on the loss function it solves toward lower. Ive already live trained a 22 node sigmoid RNN
	//whose output is to recurse 15 cycles then take one node's output as potentialEnergy. Bent it like neural playdough. Havent tried this on it 2024-11-13.
	//--https://x.com/benrayfield/status/1856780041985687963
	//this.gp = 2.3; //TODO this.gp = 0;
	this.gp = DefaultGp;
	if(this.up && this.up.pu[this.name]){
		throw new Error('Duplicate Var, same name, same parent Var');
	}
	//if(this.up) this.up.pu[this.name] = this;
	//tie the new Var into its parent in TWO places
	//** fast own-prop lookup	(thisParent.child)
	//** iteration / filtering (thisParent.pu.child)								 */
	if(this.up){
		this.up.pu[this.name] = this;	 // existing behavior 2025-7-4 and earlier.
		this.up[this.name]	= this;	 // new: direct, non-proxy hit, 2025-7-5+
	}
	
	/*doesnt work, need Proxy: this.get = function(fieldName){
		console.log('fieldName='+fieldName);
		return this[fieldName]!==undefined ? this[fieldName] : this.pU(fieldName); //creates fieldName
	};*/
	
	//has no effect if ps==0. position taRget, like in dagball.Ed having a target ave and strength as a parabola
	this.pr = 0;
	//strength of p toward pr, as pr and ps define a parabola of poten
	this.ps = 0;
	this.cv = 0; //base kv. its cv+kv, not just kv, but kv is set by code dynamicly, and cv is set in the Var.
};

Var.opt = {
	//oneBitPerDimGradient: true, //test. should make balls ignore magnitude of gradient per dimension and use opt.oneBitPerDimGradientVal vs -opt.oneBitPerDimGradientVal instead
	//oneBitPerDimGradient: false, //normal
	//oneBitPerDimGradientVal: 20,
	//oneBitPerDimGradientVal: 1,
};

//Returns a new child, that doesnt  exist (or isnt loaded, someone else in same namespace might have made it).
//is random but you might want autoinc or something like that. TODO?
Var.prototype.new = function(optionalPrefix, optionalSuffix){
	let prefix = optionalPrefix||'V';
	let suffix = optionalSuffix||'';
	let name;
	do{
		name = prefix+(''+(1e9+randInt(1e9))).substring(1)+suffix; //like 'V123456789'
	}while(this.pu[name]);
	return this[name];
};

var randInt = max=>((Math.random()*max)|0);

//var DefaultEpsilon = window.DefaultEpsilon = 2**-7; //FIXME which scripts (of the 3 in this html) use this?
var DefaultEpsilon = 2**-12; //FIXME is this small enuf? is it for float32 or float64?

//This should be a little more than the common epsilon of 1 for pixel coordinates (1 pixel over)
//so it can jump a little past that. If its 1, it moves a little too slow. If 2 its noticably jumpy.
//var DefaultGp = 1.5; //normal
//var DefaultGp = -1.5; //fixme
//var DefaultGp = 11.5;
//var DefaultGp = -11.5;
//var DefaultGp = -.1;
//var DefaultGp = .1;
//var DefaultGp = .2;
var DefaultGp = 0;
//var DefaultGp = 5.5;
//var DefaultGp = 15.5;

Var.prototype.touch = function(){
	this.t = TimeId(); //a unique time, increments by at least 1 ULP.
	return this; //for chaining calls
};

//delete me from the local V/Var tree
Var.prototype.del = function(){
	if(!this.up){
		Err('Already is root V/Var, cant del: '+this.path());
	}
	console.log('Deleting Var path='+this.path());
	delete this.up.pu[this.name];
	//FIXME this.up still exists, so if this.abc.def.ghi still exists then ghi.up.up... will still find this and parents.
};

//copy copyMe.p to this.p, copyMe.v to this.v, etc, but nothing in this.pu (childs) cuz thats not local.
//Its only the fields that count as longterm game state, not temp vars used DURING a physics cycle like this.gr.
//Does not copy .epsilon or .accelMul cuz those are set once in code in the varName/*p v e a*/ syntax,
//which I might change to include pr ps cv and maybe more, but i might leave that to the fieldEditor UI etc.
Var.prototype.copyLocalFrom = function(copyMe){
	this.p = copyMe.p;
	this.v = copyMe.v;
	this.pr = copyMe.pr;
	this.ps = copyMe.ps;
	this.cv = copyMe.cv;
};

Var.prototype.Mn = function(val){
	this.mn = Math.max(this.min,val);
};

Var.prototype.Mx = function(val){
	this.mx = Math.min(val, this.mx);
};

//does both Mn and Mx. Same as setting this.p (after this.nextState(dt)) but if others have set this.mn or this.mx
//and the value this sets it to is not in that allowed range, it does not get set at all. Thats to keep it independent
//of the order Var's are updated, which is less important in Blob Monsters Game than it was in dagball cuz Var is so
//far 2024-11-23 only used in 1 Gob/monster at a time, but in dagball they have EdJoint's. Might add EdJoints here later.
//Var.prototype.MnMx = function(val){
Var.prototype.set = function(val){
	this.mn = Math.max(this.mn,val);
	this.mx = Math.min(val, this.mx);
};

//get namespace
Var.prototype.ns = function(){
	if(this.h <= 1){
		if(this.h == 0) throw Error('This is root Var, which namespaces are childs of.');
		return this;
	}
	return this.up.ns();
};

//gets the Game (like V.testnet.game) of the namespace, even if this is like V.testnet.someGob555
Var.prototype.getGameVar = function(){
	return this.ns().game; //TODO multiple views, each a Game instance.
};

Var.prototype.getGame = function(){
	return this.getGameVar().getOb(); //Game instance
};

//added 2025-7-5, not tested
Var.prototype.z = function(){
	return this.cache.constZ!==undefined ? this.cache.constZ : (this.pu.Z || this.Z).p;
};

Var.prototype.y = function(){
	//Var.constY and .constX are created if isTileString(Var.name)
	//return (this.constY!==undefined) ? (this.constY) : ((this.pu.Y || this.Y).p);
	return this.cache.constY!==undefined ? this.cache.constY : (this.pu.Y || this.Y).p;
};

Var.prototype.x = function(){
	return this.cache.constX!==undefined ? this.cache.constX : (this.pu.X || this.X).p;
};

//used on Var.name or Var.big of a tile, like tile1971585409951104$tsLwEmG1RXpu2SgiNDErGbSemnRdoj2eTL1FNBOjstF
//or the longer form that goes in .big or the shorter form thats a literal instead of a hash after the first $.
var isTileString = s=>/^tile\d{1,16}\$/.test(s);

var tileStringToQuadTile = s=>{ //returns a QuadTile containing all the info in the string. TODO merge some of the code from Tile.toVar() into this.
	/*let i = s.indexOf('$');
	let base64 = s.substring(i+1);
	let tileNum = parseFloat(s.substring('tile'.length, i)); //0 to (2**53)-1, an integer.
	let height = SquareH(tileNum);
	let quadBytes = base64ToBytes(base64);
	return new Quad(height, quadBytes);
	*/
	let square = tileStringToSquare(s);
	return new QuadTile(square, new Quad(SquareH(square), tileStringToBytes(s)));
};

//0 to (2**53)-1, an integer. Use with SquareY SquareX SquareH and Square(h,y,x)
var tileStringToSquare = s=>parseFloat(s.substring('tile'.length, s.indexOf('$')));

var tileStringToH = s=>SquareH(tileStringToSquare(s));

//top Y. 1<<height is y height and x width.
var tileStringToY = s=>SquareY(tileStringToSquare(s));

//left X. 1<<height is y height and x width.
var tileStringToX = s=>SquareX(tileStringToSquare(s));

//is either the sha256 of the .big form or is the bytes for a Quad, so check if its the Var.name vs Var.big.
var tileStringToBytes = s=>base64ToBytes(s.substring(s.indexOf('$')+1));


//lazy create ob (Gob or Game, depending on var path ends with .game or not, todo multiple views/games).
Var.prototype.getOb = function(){
	if(this.ob){
		return this.ob;
	}else{
		if(this.h == 2){
			//raise this.t which is a unique (in this browser tab, not across network) UTC time (TimeId())
			//When multiple QuadTiles are at the same square,
			//TODO uses touch time (QuadTile.bo.t) to keep newest and turn older ones off,
			//but across network (TODO its still just 1 computer as of 2025-2-23) it wont trust .t and syncs by .p mainly.
			//Locally we use .t in some cases to choose .p values, and .e tries (within security rules) to stay equal to .p
			//when near the Y X of the view area, so it should all fit together.
			this.touch();
			let text = this.text();
			if(text.startsWith('(') || text.startsWith('gob$')){
				let game = this.getGame(); //likely a sibling, and game.influence===this.getGameVar()
				//text is a js lambda (brain) whose params if evaled should be Var objects, returns list of int voxels
				//fails cuz text is not evaled, is still a string: return this.ob = new Gob(game, text);
				let jsLambdaAsGobBrain = game.tryEval(text);
				return this.ob = new Gob(game, jsLambdaAsGobBrain);
			}else if(text == 'game'){
				//like V.testnet.game is the default path of the game,
				//but todo multiple games/views at once of each namespace.
				return this.ob = new Game(this);
			}else if(isTileString(this.name)){
				let qt = tileStringToQuadTile(this.big || this.name);
				this.ob = qt;
				qt.bo = this; //QuadTile.bo is its Var. Only if created/loaded by Var will it have a .bo field.
				return qt;
			}else{
				throw new Error('Uknown object type: '+text);
			}
		}else{
			throw new Error('this.h/height is '+this.h+' but Gob and Game go at height 2 (right after namespace at height 1)');
		}
	}
};

//copies from map to Var recursively. Overwrites where existed.
//You can fork world state by loading the part just past the namespace into another namespace you make up,
//which you can do many times per second such as for harmony-search of game states to look for lower poten/potentialEnergy.
//a json map of the kind V.toMap() creates, or subset of it, like you might do V.testnet.load({..parts inside V.testnet..})
//or you might V.load({testnet:{...},otherNamespace5:{...}}). This only copies it into the Var system,
//doesnt eval it (TODO should it? Maybe it will later and this comment not be updated FIXME?).
//
//If optional_isAutoEval is false (or param not given) then it doesnt call Var.eval() after loading,
//so for example if you load a tile it will appear in the Var tree but not in game.board or on screen.
//If you instead use optional_isAutoEval of true, it will do that eval and appear on screen,
//but be careful in that it can lead to remote-code-injection cross-site-scripting etc as the code may have
//come from an untrusted source, a peer to peer network of whatever js code ppl and AIs write as game content.
//To limit the risk of that, it should use game.tryEval(string) but as of 2025-2-17 it just evals nearly everything.
//Another way to limit that risk is to use wikibinator203 instead of javascript as the model of gob.brain code
//which is likely to be a far future upgrade.
Var.prototype.loadMap = function(map, optional_isAutoEval){
	this.p = map.p || 0; //position
	this.v = map.v || 0; //velocity
	if(map.pu){ //childs of any names
		for(let id in map.pu){
			let childMap = map.pu[id];
			//let childVar = this[id]; //reuses if exist, else creates using varProxyHandler as Var is a js Proxy object.
			let childVar = this.pu[id];
			if(!childVar){
				let big = childMap.big || id;
				childVar = this[big];
				if(childVar.name != id){
					Err('Wrong hash. big did not generate expected id of '+id+', from big='+big);
					//you could just do this[id] but that wouldnt create this[id].big which id is derived from.
				}
			}
			childVar.loadMap(childMap, optional_isAutoEval);
		}
	}
	if(optional_isAutoEval){
		console.log('Var.eval() cuz optional_isAutoEval='+optional_isAutoEval+', '+this.path());
		this.eval();
	}
};

Var.prototype.loadJson = function(json, optional_isAutoEval){
	this.loadMap(JSON.parse(json), optional_isAutoEval);
};

Var.prototype.clear = function(map){
	this.nextState(0);
	for(let key in this.pu){
		delete this[key]; //cuz is duplicated in this[childName] and this.pu[childName]
	}
	this.pu = {}; //empty this.pu
};

Var.prototype.toJson = function(excludeBig){
	return JSON.stringify(this.toMap(excludeBig));
};

Var.prototype.toJSON = function(){ //for if this is used in JSON.stringify(someVar) it auto calls someVar.toJSON()
	return this.toJson(false);
};

var Load = json=>{
	let isAutoEval = true;
	V.loadJson(json, isAutoEval);
};

var State = excludeBig=>V.toJson(excludeBig);

/*todo var Save = name=>{
	if(name === undefined){
		name = 'blobMonstersGame_'+time();
	}
	if(!name.includes('.')) name += '.vartree';
	let json = State();
	
};*/

var quicksave = function(name){
	console.log('quicksave '+name);
	localStorage.setItem('monst.'+name, State());
};

var quickload = function(name){
	console.log('quickload '+name);
	let json = localStorage.getItem('monst.'+name);
	if(json){
		Load(json);
	}
};

var saveFile = (fileName, contentType, text)=>{
	var blob = new Blob([text], {type: contentType});
	if(window.navigator.msSaveOrOpenBlob){
		window.navigator.msSaveBlob(blob, fileName);
	}else{
		var elem = window.document.createElement('a');
		elem.href = window.URL.createObjectURL(blob);
		elem.download = fileName;
		document.body.appendChild(elem);
		elem.click();
		document.body.removeChild(elem);
	}
};



//If this is a Tile, like tile1971585409951104$tsLwEmG1RXpu2SgiNDErGbSemnRdoj2eTL1FNBOjstF,
//then loads it into game.wal (BigTile) and game.board (64 megapixel array of nearest 8k x 8k square
//to game.Y.p game.X.p 2d coordinate where viewing, so careful not to load tile where it would wrap around that as its farther away.
//TODO also load gob if its that, aka its name starts with gob$ . Careful about remote code injection,
//check it for infinite loops, spam redirects of window.location, etc.
Var.prototype.eval = function(){
	if(this.name.startsWith('gob$')){
		//Todo();
		console.log('Ignoring Var.eval() for gob cuz gob puts itself in game.gobs list and has been working as of 2025-2-17, path='+this.path());
	}else if(isTileString(this.name)){
		let quadTile = this.getOb();
		game.wal.tile(quadTile.square).writeSparse(quadTile.quad); //idempotent and fast if that same quad is already there
	}else{
		console.warn('TODO how to load Var='+this.path());
	}
};

/*//path height. V is height 0. V.testnet aka namespace is height 1. and so on.
//Gobs normally go at height 2. Gob fields height 3.
Var.prototype.h = function(){
	return this.up ? (this.up.pathHeight()+1) : 0;
};*/

Var.prototype.toMap = function(excludeBig){
	let ret = {
		p: this.p,
		v: this.v,
		//name: this.name,
		//pu: {},
	};
	if(this.t){
		ret.t = this.t; //UTC time updated. not all code will use this. but each Var is a time-series of 2 numbers: position and velocity.
	}
	if(this.pr){
		ret.pr = this.pr; //target position to spring toward
	}
	if(this.ps){
		ret.ps = this.ps; //spring strength of p toward pr
	}
	if(this.cv){
		ret.cv = this.cv; //base velocity decay, which kv is reset to in Var.nextState(dt)
	}
	if(this.big && !excludeBig){
		ret.big = this.big;
	}
	for(let childName in this.pu){
		let pu = ret.pu || (ret.pu = {});
		pu[childName] = this.pu[childName].toMap(excludeBig);
	}
	return ret;
};

Var.prototype.text = function(){
	return this.big || this.name;
};

const DefaultMaxResults = 2**16;
const DefaultRadiusResults = 2**12;

Var.prototype.allVars = function(optionalListToFill){
	let list = optionalListToFill || [];
	list.push(this);
	for(let childName in this.pu){
		this.pu[childName].allVars(list);
	}
	return list;
};

//returns a list of Var in descending (or is it ascending? is positive good or bad? choose one.) order of goal(theVar)
//which returns a number for how good a match it is. Also limit by exclude negatives (or positives?) from if score is too low?
//Theres an optimization that if optionalMaxResults==1 it doesnt sort an array but just keeps the best in a loop,
//but either way it calls goal on every Var reachable from here.
//TODO optimize more in that case to not even create the array of all Var.
Var.prototype.searchTree = function(goal, optionalMaxResults){
	let maxResults = optionalMaxResults || DefaultMaxResults;
	let vars = this.allVars();
	if(maxResults == 1){ //n cost
		let bestScore = -Infinity; //FIXME is this reversed from how i vars.sort it?
		let bestVar = null;
		for(let v of vars){
			let score = goal(v);
			if(bestScore < score){
				score = bestScore;
				bestVar = v;
			}
		}
		return bestVar ? [bestVar] : [];
	}else{ //n*log(n) cost
		vars.sort((varA,varB)=>Math.sign(goal(varA)-goal(varB))); //FIXME is this reversed?
		while(vars.length > maxResults) vars.pop();
		return vars;
	}
};

//TODO rename search to searchChilds and have another func searchTree.
//goal(anyVar)->score (FIXME or should it be loss which is -score or someConstant-score?
//As goal, any positive number passes, and any 0 or negative number does not match.
//Sort by that descending, of those which pass.
Var.prototype.search = function(goal, optionalMaxResults){
	let maxResults = optionalMaxResults || DefaultMaxResults;
	//if(maxResults === undefined) maxResults = DefaultMaxResults;
	let scores = new Map();
	let ret = [];
	for(let n in this.pu){
		let childVar = this.pu[n];
		let score = goal(childVar);
		if(score > 0){
			scores.set(childVar, score);
			ret.push(childVar);
		}
	}
	ret.sort((a,b)=>{
		let scoreA = scores.get(a), scoreB = scores.get(b);
		if(scoreA < scoreB) return -1;
		if(scoreA > scoreB) return 1;
		return 0;
	});
	while(ret.length > maxResults) ret.pop();
	//console.log('Var.search got '+ret.length+' results, goal='+goal);
	/*if(game.gobs.length > 0 && ret.length == 0){ //FIXME remove this
		lastGoalWhenEmpty = goal;
		lastGobsListWhenEmptying = [...(game.gobs)];
	}*/
	return ret;
};

//FIXME rename centerY and centerX in existing game content to Y and X, like game.Y and game.X TODO game.Y and game.X.
//if its on the line, is not included. Has to be less than r distance. This is cuz sorts by a relative distance, and 0 must not be included.
Var.prototype.searchZYXR = function(z, y, x, r, maxResults){
	if(r === undefined) r = DefaultRadiusResults;
	//const rr = r*r;
	return this.search(
		vr=>{
			//return rr - ((vr.Y.p-y)**2 + (vr.X.p-x)**2);
			let distSq = (vr.z()-z)**2 + (vr.y()-y)**2 + (vr.x()-x)**2;
			let dist = Math.sqrt(distSq);
			return dist;
			
			
			
			
			
			
			
			
			
			
			
			
			
			//FIXME this isnt cutting it off (by being 0 or less) at r aka radius.
			
			
			
			
			
			
			
			
			
			
			
			//let d = rr - ((vr.z()-z)**2 + (vr.y()-y)**2 + (vr.x()-x)**2);
			//return d;
			//return -d;
		},
		maxResults);
};

//makes a new goal that also	requires it be within r distance of (y,x) (not on the line).
Var.prototype.searchYXRGoal = function(y, x, r, goal, maxResults){
	const rr = r*r;
	return this.search(vr=>{
		//let isNear = rr > ((vr.Y.p-y)**2 + (vr.X.p-x)**2);
		//in case [the Var whose Var.ob is a QuadTile] doesnt have Y and X child Vars,
		//since its implied by the first number in Var.big in that case (see SquareY and SquareX funcs and tileSize).
		//See Var.constY and Var.constX which Var.y() and Var.x() use if they exist.
		let isNear = rr > ((vr.y()-y)**2 + (vr.x()-x)**2);
		if(!isNear) return 0;
		return goal(vr);
	}, maxResults);
};

Var.prototype.if0 = function(newP){
	if(!this.p) this.p = newP;
	return this;
};

Var.prototype.setNow = function(newP, optionalNewV){
	this.p = newP;
	if(optionalNewV !== undefined) this.v = optionalNewV;
	return this;
};

Var.prototype.setPr = function(optionalPr){ //spring target this.p. If you dont give optionalPr its this.p the current position.
	this.pr = optionalPr!==undefined ? optionalPr : this.p;
	return this;
};

Var.prototype.setPs = function(ps){ //spring strength of this.p toward this.pr
	this.ps = ps;
	return this;
};



Var.prototype.setSpring = function(ps, optionalPr){
	this.ps = ps;
	this.pr
	this.pr = pr;
};

//const hashIdLen = ('sha256$'.length+64); //64 hex chars. todo base58 or base64 or something. have code in Dagverse.js.
const hashIdLen = ('gob$'.length+64); //64 hex chars. todo base58 or base64 or something. have code in Dagverse.js.
//
//FIXME theres gob$hash and tile9007199254595405$hash and tile9007199254595405$literalIfSmall,
//so should hashIdLen be renamed to minHashIdLen?


//TODO what should this limit be?
//If its longer	than this, auto hashes it and uses the hash (prefixed by what, in case it starts with a digit etc?)
//as the Var.name and the content hashed as the Var.big.
//so u can know if its a hash or not by its length. or could check for any chars then $ like sha256$thehash.
const MaxLiteralNameLen = hashIdLen-1;

const isLowercase = c=>(c >= 'a' && c <= 'z');

//get or create child Var
Var.prototype.pU = function(nameOrBig){
	if(isLowercase(nameOrBig[0])){
		Err('Child Vars cant start with lowercase letter, such as toString p v or you gave: '+nameOrBig);
	}
	let ret;
	if(nameOrBig.length <= MaxLiteralNameLen && /^[a-zA-Z_$][a-zA-Z0-9_$]*$/.test(nameOrBig)){ //TODO make this condition be a func
		ret = this.pu[nameOrBig] || new Var(this, nameOrBig, null, this.ob||null); //auto puts it in this.pu[string]
	}else{
		//let hash = hashStringToHex(nameOrBig);
		let name = hashStringToBase64(nameOrBig); //todo dont hash if its small enuf to be a literal id (dont use .big)
		/*if(nameOrBig.startsWith('mutid$')){ //FIXME 2025-1-9 removed the mutid$ prefix of tiles, so am not using it for anything.
			let i = nameOrBig.indexOf('$','mutid$'.length);
			if(i!=-1){ //found next $ like in mutid$tile3534523423$...
				name = nameOrBig.substring(i+1)+name; //mutid$tile3534523423$234324hash345345
			}else Err('no second $ found in mutid$...');
		*/
		//TODO this is likely blobMonstersGame Gob code not relevant to bellsack:
		if(nameOrBig.startsWith('tile')){ //like tile1971583262467328$ then base64 of its Quad bytes, if small, else then base64 of hash of that.
			if(isValidVarName(nameOrBig) && nameOrBig.length < 64){
				//considering size of tile1971583262467328$ (size 21) and 43 digits of sha256 base64 (21+43==64),
				//if its smaller then use it directly, else hash it.
				//isValidVarName might let vars be bigger like 100, but i havent used it much and am experimenting. Might need those bigger vars.
				name = nameOrBig;
			}else{ //FIXME this isnt running for nontiles, like anyPrefixblahblah4325$stufftohash
				let i = nameOrBig.indexOf('$');
				if(i == -1) Err('No $ after tile in var name');
				let prefix = nameOrBig.substring(0,i+1); //like tile1971583262467328$
				name = prefix+name; //like tile1971583262467328$thenbase64ofsha256ofdotbig
				
				//example:
				//tile1971585409951104$tsLwEmG1RXpu2SgiNDErGbSemnRdoj2eTL1FNBOjstF is the name of big:	//tile1971585409951104$qjB$pzN$oUR$$$2GwV$$$Bo$$$28$$$$lF$$$3k$pUg$oz$$oUc$nRJ$$$0BIBJ$I3lBIBZ$lF$$$3k$I3k$oUAClF$$$3lBlF0B$3lBI3lB$CArnF28$$$$lF$$$3k$$3k$oUQ8I3n4I3k$I3lBmRJ$I$0BI$0BI$2HyF2Hx$2Gzk2GygZ$lJlB$3k$$3k$nRJ$I$0BI$24I3k$I$$$$$$$$$
			}
			//TODO generate this.Y.p and this.X.p to be derived from SquareY and SquareX of 1971585409951104 like in tile1971585409951104$,
			//but dont let them change and dont spend time computing what if they change during physics. Tiles are constants.
			
			//My 128x128 game tiles have hash ids like this. The first number tells a power
			//of 2x2 size, y, and x: tile1971585409951104$tsLwEmG1RXpu2SgiNDErGbSemnRdoj2eTL1FNBOjstF
			//Then 43 base64 digits of sha256 of the quadtree compressed content, which is normally a few hundred bytes.
		}else{
			//name = 'sha256$'+name; //no special prefixing
			name = 'gob$'+name; //no special prefixing
		}
		//ret = this.pu[name] || new Var(this, name, nameOrBig, this.gob||null); //auto puts it in this.pu[string]
		ret = this.pu[name] || new Var(this, name, nameOrBig, this.ob||null); //auto puts it in this.pu[string]
	}
	//TODO this is likely blobMonstersGame Gob code not relevant to bellsack:
	if(ret.big && ret.big.startsWith('(')){ //likely a js function string
		let listOfLists = getParamNames(ret.big);
		if(listOfLists.length){
			ret.vars = []; //same order as in gob.vars, a list instead of the .pu {} of paramName to Var. Vars either way.
			for(let list of listOfLists){
				let paramName = list[0]; //TODO if theres more stuff in it, do whats normally done after getParamNames, fill in .p .v .epsilon andOr .accelMul etc.
				ret.vars.push(ret.pU(paramName));
			}
		}
	}
	return ret;
};

Var.prototype.think = function(){
	let brain = this.brain || (this.brain = eval(this.big || this.name));
	//no this is done in Gob.think: this.extraThink(); //do game.gravY.p etc.
	return brain(...(this.vars)); //list or Int32Array of int voxels. See YXC IY IX YXRGB etc funcs for int voxels.
};

const varProxyHandler = {
	/*get(target, prop, receiver){ //works 2025-7-4
		if(typeof(prop) === 'symbol'){
			return Reflect.get(target, prop, receiver);
		}
		return target[prop] || receiver.pU(prop);
	},*/
	//2025-7-5 moving varProxyHandler to be prototype of prototype of each Var instance, so .toString etc stay in its prototype.
	//If a childName is not found, creates it in thisVar.childName and in thisVar.pu.childName which point at the same Var,
	//so thisVar.pu.childName doesnt create it and theres some syntax thisVar.pu.?childName maybe, that can chain it get undefined at end.
	get(target, prop, receiver){
		if(typeof(prop) === 'symbol'){
			return Reflect.get(target, prop, receiver);
		}
		//return target[prop] || receiver.pU(prop);
		/*GPT-o3 says why change receiver.pU(prop) to target.pU.call(receiver, prop)
		-	 const child = target.Pu.call(receiver, prop);
		+	 const child = target.pU.call(receiver, prop);
			return child;
		}
		❓ Why not receiver.pU(prop)?
		When the instance (receiver) looks for pU, it doesn’t have an
		own-property, so the engine would walk up the prototype chain:
		VarPrototype → VarProxy → …
		That walk would re-enter the same proxy trap we’re executing right
		now, leading to an extra hop (and, in some cases, an infinite loop
		if guards were missing).

		By calling target.pU.call(receiver, …) we:

		grab the already-known method reference directly from the
		plain object that is the proxy’s target (VarPrototype),

		bind this to the real instance (receiver),

		avoid any second trip through the proxy machinery.

		This keeps the “first-touch” cost to one proxy invocation and guarantees
		that all subsequent property reads hit the freshly cached
		this[childName] own-property at plain-object speed.
		*/
		//return target[prop] || target.pU.call(receiver,prop);
		
		//Prototype-owned props (pU, path, toString, …)
		//if(prop in target){
		//	return target[prop];
		//}
		//Prototype-owned methods (pU, path, toString, …)
		//if(prop in Var.prototype){
		//	return Var.prototype[prop];
		//}
		
		
		/*//Already-materialised child (own-prop on the instance)
		const cached = Reflect.get(receiver, prop, receiver);
		if(cached !== undefined){
			return cached;
		}
		that caused infinite loop
		V.hello
		bellsack161.html:2384 Uncaught RangeError: Maximum call stack size exceeded
		at Reflect.get (<anonymous>)
		at Object.get (bellsack161.html:2384:26)
		at Reflect.get (<anonymous>)
		at Object.get (bellsack161.html:2384:26)
			Here’s the one-line fix that stops the infinite recursion.
		(Only the get trap is touched.)

		diff
		Copy
		Edit
		@@
		-		//Already-materialised child (own-prop on the instance)
		-		const cached = Reflect.get(receiver, prop, receiver);
		-		if(cached !== undefined){
		-			return cached;
		-		}
		+		//Already-materialised child (own-prop on the *instance*) – check without climbing the
		+		//prototype chain so we don’t re-enter this proxy trap.
		+		if (Object.prototype.hasOwnProperty.call(receiver, prop)) {
		+			return receiver[prop];
		+		}
		*/
		//Already-materialised child (own-prop on the *instance*) – check without climbing the
		//prototype chain so we don’t re-enter this proxy trap.
		if(Object.prototype.hasOwnProperty.call(receiver, prop)){
			return receiver[prop];
		}
		
		//First-touch child: create & cache via pU
		//return target.pU.call(receiver, prop);
		//First-touch child — use receiver.pU; the lookup
		//resolves on Var.prototype and never re-enters the proxy.
		return receiver.pU(prop);
	},
};

//Var.prototype = new Proxy(Var.prototype, varProxyHandler);
const VarProxy	 = new Proxy(Object.create(null), varProxyHandler);
Object.setPrototypeOf(Var.prototype, VarProxy); //2025-7-5 changing from Var being a Proxy to "instance → proto → proxy".


//Var.prototype.pushEpsilon = function(epsilon){
Var.prototype.pushEpsilon = function(){
	this.prevP = this.p;
	this.p += this.epsilon;
};

Var.prototype.popEpsilon = function(){
	this.p = this.prevP;
	this.prevP = 0;
};

//TODO test this.
Var.prototype.valueOf = function(){ //the position, this.p, though calling this.p is probably more efficient.
	return this.p;
};

Var.prototype.path = function(){
	return this.up ? this.up.path()+'.'+this.name : this.name;
};

Var.prototype.toString = function(){
	return this.path();//return this.up ? this.up.toString()+'.'+this.name : this.name;
	//return '{type:"vox_var",p:'+this.p+',v:'+this.v+',kv:'+this.kv+',dp:'+this.dp+',dv:'+this.dv+',mn:'+this.mn+',mx:'+this.mx+'}';
};

Var.prototype.nextState = function(dt){
	
	if(this.p != this.p){ //FIXME remove this, was added 2025-8-5 during isBallCacheOptimization cuz balls keep turning NaN after few seconds
		this.p = (Math.random()-0.5)*30;
		this.v = 0;
		console.log('Var.nextState ugly hack just changed NaN p to '+this.p+' and v to '+this.v);
	}
	
	
	if(dt){
		//use someVar.nextState(0) to clear someVar.kv someVar.dp etc, without modifying someVar.p or .v etc.
		//For use during gradient of things that might happen but have not decided to make them happen.
		
		//this.v = 0; //FIXME
		//let nextP = this.p + dt*(this.v+this.dp);
		if(this.ps){ //spring strength is nonzero. TODSO fix blobMonstersGame it has if(this.pr) should be ps.
			//this.gr += TODO something about this.pr and this.ps as parabola.
			//let positionDiff = this.pr-this.p; //FIXME is this backward? accel negative gradient
			let positionDiff = this.p-this.pr; //FIXME is this backward? accel negative gradient
			let partOfGradientFromParabola = positionDiff*this.ps; //TODO divide by 2 like potentialenergy of stack of z tall mass is z*z/2. ???
			//let partOfGradientFromParabola = positionDiff/2*this.ps; //TODO verify this /2 is correct (vs /4 or *2 or sqrt2, etc, or just leave it as is): divide by 2 like potentialenergy of stack of z tall mass is z*z/2. ???
			this.gr += partOfGradientFromParabola;
			//this.poten += this.ps*positionDiff*positionDiff;
		}
		/*if(Var.opt.oneBitPerDimGradient){ //FIXME this is outside the Var script, is part of Bellsack script, so shouldnt be here.
			if(this.gr < 0) this.gr = -Var.opt.oneBitPerDimGradientVal;
			if(this.gr > 0) this.gr = Var.opt.oneBitPerDimGradientVal;
			//3 possible values
		}*/
		let nextP = this.p + dt*(this.v+this.dp-this.gp*this.gr);
		if(this.mn <= this.mx){
			nextP = Math.max(this.mn, Math.min(nextP, this.mx)); //truncate into range
		}
		let nextV = (this.v+dt*this.accelMul*(this.dv-this.gr))*Math.exp(-dt*this.kv);
		//let nextV = 0; //FIXME
		
		
		//let changePAmount = Math.abs(this.p-nextP);
		//if(changePAmount > 100 && this.ob==cShapedGob){ //FIXME remove this
		//	console.log('Var '+this.path()+' changePAmount='+changePAmount);
		//}
		
		this.p = nextP;
		this.v = nextV;
	}
	//this.kv = this.dp = this.dv = this.gr = this.poten = 0;
	this.kv = this.cv; //cv is base kv. velocity decay per second continuously.
	this.dp = this.dv = this.poten = 0; //OLD: leave this.gr as is, since its not a sum, is just set all at once in one of the doPhysics funcs.
	this.prevGr = this.gr; //for debugging. has no effect on physics. previous gradient.
	this.gr = 0; //cuz in blobMonstersGame gr was set in doPhysicsA, but here we dont have that func.
	this.mn = -Infinity;
	this.mx = Infinity;
	//leave this.pr and this.ps (spring) as they are, which are inputs only, not moved by gradient.
};

//getParamNames((a/*2 3 4*/, b/*5 6*/, c)=>(a+b)) returns [['a',2,3,4],['b',5,6],['c']].
var getParamNames = funcOrStr=>{
	const fnStr = funcOrStr.toString().replace(/[\r\n]/g, '').trim();
	if(fnStr.startsWith('()=>')){
		return [];
	}
	const params = fnStr.slice(fnStr.indexOf('(') + 1, fnStr.indexOf(')')).split(',')
		.map(param => param.trim().match(/(\w+)(?:\/\*([^*]+)\*\/)?/));
	return params.map(match => {
		const [_, name, comment] = match;
		const numbers = comment ? comment.match(/\d+/g) : [];
		return [name, ...(numbers || []).map(Number)];
	});
};

Var.prototype.setOb = function(gobOrGame){
	this.ob = gobOrGame;
	return this;
};




//Example fields 'p' 'v' 'kv'. someVar.fieldGetter('p')() returns someVar.p
Var.prototype.fieldGetter = function(field){
	const thisVar = this;
	return ()=>(thisVar[field]);
};

//Example fields 'p' 'v' 'kv'. someVar.fieldSetter('p')(someVar.fieldGetter('p')+1) increments someVar.p
Var.prototype.fieldSetter = function(field){
	const thisVar = this;
	return val=>(thisVar[field] = val);
};

/*This makes (the next version of todo) the editor at the top left appear with input type=range sliders
of the selected Gob, in the selectedGobVarsDiv_table code, similar to this:
V.testnet.gob$Zxbv95B$dT3MVDu7Akt8PZNHAMeB4ZwNeats2TeDchR
Var.name	                       .p                              	.pr	.ps	.cv
Y	min=0 max=16777215
74972.52934667701
min=0 max=16777215
0	min=0 max=100
0	min=0 max=3
0
X	min=0 max=16777215
75182.65197622102
min=0 max=16777215
0	min=0 max=100
0	min=0 max=3
0
heightToWidthRatio	min=-5 max=5
0.9336636940953708	min=-5 max=5
0	min=0 max=100
0	min=0 max=3
0
make a new SigmoidNumEditor of that field in this Var such as to edit thisVar.cv or thisVar.p.
Theres some arbitrary interpretation involved in which var names (Y and X especially) get scaled how much
in the display of the editor, how much of the range of the slidebar (input type=range) means which number ranges,
but if you call fieldEditor again later it will use updated Var values to give you a more relevant editor.
*/
Var.prototype.fieldEditor = function(field, isForMenu){
	//the first 2 params of every gob.brain func should be Y and X which range 0 to 0xffffff.
	let isYX = this.name=='Y' || this.name=='X';
	let add = 0;
	let mul = 1;
	let hardMin = -(2**30);
	let hardMax = 2**30;
	if(field == 'name'){ //string name so uses a StringViewer instead of a SigmoidNumEditor. Its just for displaying the string in the table.
		return new StringViewer(this.name);
	}else if(field == 'path'){ //string name so uses a StringViewer instead of a SigmoidNumEditor. Its just for displaying the string in the table.
		return new StringViewer(this.path());
	}else if(field == 'p'){ //position
		if(isYX){
			add = this.p|0;
			mul = 300; //FIXME?
			hardMin = 0;
			hardMax = 0xffffff;
		}else if(this.name=='gravY'){ //FIXME put these default ranges (how big does slider movement mean?) somewhere else
			add = 0; //FIXME?
			mul = 100; //FIXME?
			hardMin = -1000;
			hardMax = 1000;
		}else{
			if((field.startsWith('is') || field.startsWith('do')) && (this.p===0 || this.p===1)){
				return new CheckboxVarEditor(this); //like for V.testnet.game.doRps
			}
			//add = this.p;
			add = 0; //FIXME?
			mul = 10; //FIXME?
			hardMin = -100;
			hardMax = 100;
		}
	}else if(field == 'v'){ //velocity
		add = 0;
		if(isYX){
			mul = 100; //FIXME?
		}else{
			mul = 10; //FIXME?
		}
		hardMin = -1000; //FIXME?
		hardMax = 1000; //FIXME?
	}else if(field == 'pr'){ //target position, that a simulated spring pushes toward
		if(isYX){
			add = this.p|0;
			mul = 500; //FIXME?
			hardMin = 0;
			hardMax = 0xffffff;
		}else{
			add = this.p;
			mul = 10; //FIXME?
			hardMin = -100; //FIXME
			hardMax = 100; //FIXME
		}
	}else if(field == 'ps'){ //strength of the pr spring
		//This should be a log scale from 0 up
		add = -5; //FIXME
		mul = 10; //FIXME
		hardMin = 0;
		hardMax = 30;
	}else if(field == 'cv'){ //bases velocity decay
		//This should be a log scale from 0 up
		add = -5; //FIXME
		mul = 10; //FIXME
		hardMin = 0;
		hardMax = 30;
	}else if(field == 'kv'){ //dynamic velocity decay, that in Var.nextState is reset to Var.cv
		//This should be a log scale from 0 up
		add = -5; //FIXME
		mul = 10; //FIXME
		hardMin = 0;
		hardMax = 30;
	}else{
		ave = 0; //FIXME?
		mul = 10; //FIXME?
		hardMin = -100;
		hardMax = 100;
	}
	//FIXME its not using hardMin or hardMax
	let getter = this.fieldGetter(field);
	let setter = this.fieldSetter(field,isForMenu);
	const numEditor = new NumEditor(getter, setter);
	const sigmoidNumEditor = new SigmoidNumEditor(numEditor, add, mul);
	sigmoidNumEditor.labelPrefix = this.name; //not this.path() that would be too long, but TODO make the dom display that on hover in a title
	/*let extraSetterEvent = ()=>{
		//sigmoidNumEditor.
	};
	if(isForMenu){
		const innerSetter = this.fieldSetter(field);
		setter = val=>{
			innerSetter(val);
			console.error('TODO innerSetter');
			//throw new Error('TODO');
		};
	}else{
		setter = this.fieldSetter(field);
	}
	return new SigmoidNumEditor(new NumEditor(getter, setter), add, mul);
	*/
	return sigmoidNumEditor;
};

//returns a list of them which normally goes in VarEditors which is a list of lists of editors
Var.prototype.fieldEditors = function(){
	return [
		this.fieldEditor(game.isDisplayFullVarNamesInTable.p ? 'path' : 'name'),
		this.fieldEditor('v',false), //false not isForMenu, cuz is for the 2d grid on the bottom right controlled by "vars" checkbox.
		this.fieldEditor('p',false),
		this.fieldEditor('pr',false),
		this.fieldEditor('ps',false),
		this.fieldEditor('cv',false),
	];
};

//var LogScale = function(mul){
//	this.mul = mul;
//};
//LogScale.prototype.forward = function(val){
//	//FIXME how do i get it into range 0 to 1? Just use sigmoid? Use tanh for range -1 to 1?
//	return this.mul*Math.log(val);
//};

//set(get()+1) increments the val, for example.
var NumEditor = function(get, set){
	this.get = get;
	this.set = set;
};

//wrapMe is a NumEditor such as wrapping a raw Var.ps or Var.p or Var.kv
var SigmoidNumEditor = function(wrapMe, optionalAdd, optionalMul, optionalMin, optionalMax){
	this.add = optionalAdd || 0;
	this.mul = optionalMul || 1;
	this.min = optionalMin || (-(2**30));
	this.max = optionalMax || (2**30);
	this.wrapMe = wrapMe;
};

SigmoidNumEditor.prototype.get = function(){
	//return sigmoid(this.add+this.mul*this.wrapMe.get());
	return sigmoid((this.wrapMe.get()-this.add)/this.mul);
};

SigmoidNumEditor.prototype.set = function(val){
	//this.wrapMe.set((inverseSigmoid(val)-this.add)/this.mul);
	//this.wrapMe.set(inverseSigmoid(val+this.add)*this.mul);
	this.wrapMe.set(Math.max(this.min, Math.min(this.add+this.mul*inverseSigmoid(val), this.max)));
	//console.log('SigmoidNumEditor set '+val);
	this.updateDom(); //needed to update the label under the slider when its in the menu
};

SigmoidNumEditor.prototype.updateDom = function(){
	if(!this.dom){
		Err('Have no dom');
	}
	let slider = document.getElementById(this.idPrefix+'_slider');
	let label = document.getElementById(this.idPrefix+'_label');
	let newVal = this.get();
	if(newVal != slider.valueAsNumber){ //less dom events, only if changed, cuz might interfere with mouse drag events of the slider
		//FIXME 2025-3-7 this is not updating the label in NS.game.gravY.fieldEditor('p'), which is the first time
		//I used a SigmoidNumEditor outside the grid menu on the bottom right of screen (that "vars" checkbox displays or not),
		//and that grid has its own update loop that runs once per video frame. Menu checkboxes and menu sliders
		//are a separate event system, so we probably need to make new event in SigmoidNumEditor.prototype.set
		//but without creating duplicate events in the grid sliders.
		slider.valueAsNumber = newVal;
		//label.textContent = this.wrapMe.get();
	}
	let correctLabelText = ''+this.wrapMe.get();
	if(this.labelPrefix) correctLabelText = this.labelPrefix+' '+correctLabelText;
	if(label.textContent != correctLabelText){ //avoid slow dom event if didnt change
		label.textContent = correctLabelText;
	}
};

var NextIdNum = 1000;

SigmoidNumEditor.prototype.putInDom = function(dom){
	const thisEditor = this;
	this.idPrefix = 'sigmoidNumEditor_'+(NextIdNum++);
	let s = '';
	
	s += '<font color=gray>add='+this.add+' mul='+this.mul+'</font><br>';
	s += '<input type=range id='+this.idPrefix+'_slider min=0, max=1 step=.001></input><br>';
	s += '<label id='+this.idPrefix+'_label value='+this.wrapMe.get()+'></input><br>';
	
	/*
	for(let i=0; i<selectedGob.vars.length; i++){
		let v = selectedGob.vars[i];
		for(let field of fields){
			let slider = document.getElementById('slider_'+v.name+'_'+field);
			//dont mod dom nodes, which causes event problems if mouse is acting on it, unless it actually changed
			let changed = slider.valueAsNumber != v[field];
			if(changed){
				slider.valueAsNumber = v[field];
			}
			let isBigDim = (v.name == 'Y' || v.name == 'X') && field=='p';
			if(!isBigDim){
				//if(changed){
					let label = document.getElementById('label_'+v.name+'_'+field);
					//label.innerHTML = ''+v[field];
					label.textContent = ''+v[field];
				//}
			}
		}
	}
	*/
	
	
	//dom.innerHTML = 'SigmoidNumEditor, add='+this.add+' mul='+this.mul; //FIXME
	dom.innerHTML = s;
	
	let slider = document.getElementById(this.idPrefix+'_slider');
	slider.addEventListener('input', function(){
		let val = this.valueAsNumber;
		//let prevVal = v[field];
		//v[field] = val;
		let prevVal = thisEditor.get();
		thisEditor.set(val);
		//console.log('Set '+v.path()+'.'+field+' from '+prevVal+' to '+val);
		console.log('SigmoidNumEditor changed from '+prevVal+' to '+val);
	});
	
	this.dom = dom;
};

//like SigmoidNumEditor but made for viewing its string Var.name. Goes in VarEditors (list of lists of editor).
var StringViewer = function(str){
	this.str = str;
};

StringViewer.prototype.putInDom = function(dom){
	dom.innerHTML = this.str;
	this.dom = dom;
};

StringViewer.prototype.updateDom = function(){
	//do nothing. updateDom is just here for compatibility with SigmoidNumEditor
};

//for Var's whose value is 0 or 1, like V.testnet.game.doRps turns Rock Paper Scissors mode on/off.
//Puts a checkbox on screen that mods that var.p when clicked and updates itself on screen if Var changes
//after polling using this.updateDom();
var CheckboxVarEditor = function(theVar, optionalText){
	this.bo = theVar; //bo is opposite spelling of ob (object). object.bo gets Var. Var.ob gets object.
	//this.text = optionalText || theVar.path();
	this.text = optionalText || theVar.name;
};

CheckboxVarEditor.prototype.putInDom = function(dom){
	const thisEditor = this;
	this.idPrefix = 'checkboxVarEditor_'+(NextIdNum++);
	let firstVal = !!this.bo.p;
	let s = '<input type=checkbox id='+this.idPrefix+'_chk '+(firstVal?'checked':'')+'></input><label for='+this.idPrefix+'_chk title="'+thisEditor.bo.path()+'">'+this.text+'</label>';
	dom.innerHTML = s;
	this.dom = dom;
	const chk = document.getElementById(this.idPrefix+'_chk');
	chk.addEventListener('input', function(){
		thisEditor.bo.p = chk.checked ? 1 : 0;
		console.log('CheckboxVarEditor '+thisEditor.bo.path()+'.p = '+thisEditor.bo.p);
	});
};

CheckboxVarEditor.prototype.updateDom = function(){
	if(!this.dom){
		Err('Have no dom');
	}
	let chk = document.getElementById(this.idPrefix+'_chk');
	let newVal = !!this.bo.p;
	if(chk.checked !== newVal){ //avoid slow dom event if value didnt change
		chk.checked = newVal;
	}
};

CheckboxVarEditor.prototype.deleteDom = StringViewer.prototype.deleteDom = SigmoidNumEditor.prototype.deleteDom = function(){
	if(this.dom){
		this.dom.innerHTML = '';
		delete this.dom;
	}
};







//https://raw.githubusercontent.com/benrayfield/jsutils/master/src/sha256.js
var sha256 = function(bytesIn){
	//var t = typeof bytesIn;
	//if(t != 'Uint8Array') throw 'Expected Uint8Array but got a '+t; //this check wont work because its like a map of index to byte
	
	var chunks = Math.floor((bytesIn.byteLength+9+63)/64); //512 bit each
	
	//Copy bytesIn[] into b[], then pad bit1, then pad bit0s,
	//then append int64 bit length, finishing the last block of 512 bits.
	//byte b[] = new byte[chunks*64];
	var b = new Uint8Array(chunks*64);
	
	//System.arraycopy(bytesIn, 0, b, 0, bytesIn.byteLength);
	b.set(bytesIn, 0);
	
	b[bytesIn.byteLength] = 0x80;
	
	//long bitLenTemp = bytesIn.byteLength*8;
	var bitLenTemp = bytesIn.byteLength*8; //in js, this has float64 precision, which is more than enough for Uint8Array size
	for(var i=7; i>=0; i--){
		b[b.byteLength-8+i] = bitLenTemp&0xff;
		bitLenTemp >>>= 8;
	}
	
	//log('b as hex = '+bitfuncs.uint8ArrayToHex(b));
	
	
	var a = new Uint32Array(136);
	//"first 32 bits of the fractional parts of the cube roots of the first 64 primes 2..311"
	a[0]=0x428a2f98;
	a[1]=0x71374491;
	a[2]=0xb5c0fbcf;
	a[3]=0xe9b5dba5;
	a[4]=0x3956c25b;
	a[5]=0x59f111f1;
	a[6]=0x923f82a4;
	a[7]=0xab1c5ed5;
	a[8]=0xd807aa98;
	a[9]=0x12835b01;
	a[10]=0x243185be;
	a[11]=0x550c7dc3;
	a[12]=0x72be5d74;
	a[13]=0x80deb1fe;
	a[14]=0x9bdc06a7;
	a[15]=0xc19bf174;
	a[16]=0xe49b69c1;
	a[17]=0xefbe4786;
	a[18]=0x0fc19dc6;
	a[19]=0x240ca1cc;
	a[20]=0x2de92c6f;
	a[21]=0x4a7484aa;
	a[22]=0x5cb0a9dc;
	a[23]=0x76f988da;
	a[24]=0x983e5152;
	a[25]=0xa831c66d;
	a[26]=0xb00327c8;
	a[27]=0xbf597fc7;
	a[28]=0xc6e00bf3;
	a[29]=0xd5a79147;
	a[30]=0x06ca6351;
	a[31]=0x14292967;
	a[32]=0x27b70a85;
	a[33]=0x2e1b2138;
	a[34]=0x4d2c6dfc;
	a[35]=0x53380d13;
	a[36]=0x650a7354;
	a[37]=0x766a0abb;
	a[38]=0x81c2c92e;
	a[39]=0x92722c85;
	a[40]=0xa2bfe8a1;
	a[41]=0xa81a664b;
	a[42]=0xc24b8b70;
	a[43]=0xc76c51a3;
	a[44]=0xd192e819;
	a[45]=0xd6990624;
	a[46]=0xf40e3585;
	a[47]=0x106aa070;
	a[48]=0x19a4c116;
	a[49]=0x1e376c08;
	a[50]=0x2748774c;
	a[51]=0x34b0bcb5;
	a[52]=0x391c0cb3;
	a[53]=0x4ed8aa4a;
	a[54]=0x5b9cca4f;
	a[55]=0x682e6ff3;
	a[56]=0x748f82ee;
	a[57]=0x78a5636f;
	a[58]=0x84c87814;
	a[59]=0x8cc70208;
	a[60]=0x90befffa;
	a[61]=0xa4506ceb;
	a[62]=0xbef9a3f7;
	a[63]=0xc67178f2;
	//h0-h7 "first 32 bits of the fractional parts of the square roots of the first 8 primes 2..19"
	a[64]=0x6a09e667;
	a[65]=0xbb67ae85;
	a[66]=0x3c6ef372;
	a[67]=0xa54ff53a;
	a[68]=0x510e527f;
	a[69]=0x9b05688c;
	a[70]=0x1f83d9ab;
	a[71]=0x5be0cd19;
	//a[72..135] are the size 64 w array of ints
	for(var chunk=0; chunk<chunks; chunk++){
		var bOffset = chunk<<6;
		//copy chunk into first 16 words w[0..15] of the message schedule array
		for(var i=0; i<16; i++){
			//Get 4 bytes from b[]
			var o = bOffset+(i<<2);
			a[72+i] = ((b[o]&0xff)<<24) | ((b[o+1]&0xff)<<16) | ((b[o+2]&0xff)<<8) | (b[o+3]&0xff);
		}
		//Extend the first 16 words into the remaining 48 words w[16..63] of the message schedule array:
		for(var i=16; i<64; i++){
			//s0 := (w[i-15] rightrotate 7) xor (w[i-15] rightrotate 18) xor (w[i-15] rightshift 3)
			//s1 := (w[i-2] rightrotate 17) xor (w[i-2] rightrotate 19) xor (w[i-2] rightshift 10)
			//w[i] := w[i-16] + s0 + w[i-7] + s1
			var wim15 = a[72+i-15];
			var s0 = ((wim15>>>7)|(wim15<<25)) ^ ((wim15>>>18)|(wim15<<14)) ^ (wim15>>>3);
			var wim2 = a[72+i-2];
			var s1 = ((wim2>>>17)|(wim2<<15)) ^ ((wim2>>>19)|(wim2<<13)) ^ (wim2>>>10);
			a[72+i] = a[72+i-16] + s0 + a[72+i-7] + s1;
		}
		var A = a[64];
		var B = a[65];
		var C = a[66];
		var D = a[67];
		var E = a[68];
		var F = a[69];
		var G = a[70];
		var H = a[71];
		for(var i=0; i<64; i++){
			/* S1 := (e rightrotate 6) xor (e rightrotate 11) xor (e rightrotate 25)
			ch := (e and f) xor ((not e) and g)
			temp1 := h + S1 + ch + k[i] + w[i]
			S0 := (a rightrotate 2) xor (a rightrotate 13) xor (a rightrotate 22)
			maj := (a and b) xor (a and c) xor (b and c)
			temp2 := S0 + maj
			h := g
			g := f
			f := e
			e := d + temp1
			d := c
			c := b
			b := a
			a := temp1 + temp2
			*/
			var s1 = ((E>>>6)|(E<<26)) ^ ((E>>>11)|(E<<21)) ^ ((E>>>25)|(E<<7));
			var ch = (E&F) ^ ((~E)&G);
			var temp1 = H + s1 + ch + a[i] + a[72+i];
			var s0 = ((A>>>2)|(A<<30)) ^ ((A>>>13)|(A<<19)) ^ ((A>>>22)|(A<<10));
			var maj = (A&B) ^ (A&C) ^ (B&C);
			var temp2 = s0 + maj;
			H = G;
			G = F;
			F = E;
			E = D + temp1;
			D = C;
			C = B;
			B = A;
			A = temp1 + temp2;
		}
		a[64] += A;
		a[65] += B;
		a[66] += C;
		a[67] += D;
		a[68] += E;
		a[69] += F;
		a[70] += G;
		a[71] += H;
	}
	//RETURN h0..h7 = a[64..71]
	//byte ret[] = new byte[32];
	var ret = new Uint8Array(32);
	for(var i=0; i<8; i++){
		var ah = a[64+i];
		ret[i*4] = (ah>>>24)&0xff;
		ret[i*4+1] = (ah>>>16)&0xff;
		ret[i*4+2] = (ah>>>8)&0xff;
		ret[i*4+3] = ah&0xff;
	}
	return ret;
};

//this uses js digits. i prefer dvBase64Digits cuz they are all valid in js var names and are in ascending order.
//dagball.bytesToBase64 = bytes=>btoa(String.fromCharCode.apply(null, bytes)); //returns string

//bytesToBase64 = bytes=>jsBase64ToDvBase64(btoa(String.fromCharCode.apply(null, bytes))); //returns string


//use this one cuz its sorted by utf8 and ascii except = padding
const dvBase64Digits = '$0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz=';
//This is whats made by javascript atob and btoa funcs. This one is only used internally for atob and btoa
const jsBase64Digits = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';

var bytesToJsBase64 = bytes=>btoa(String.fromCharCode.apply(null, bytes)); //returns string

var jsBase64ToBytes = base64=>{ //returns Uint8Array
	const binaryString = atob(base64);
	const len = binaryString.length;
	const bytes = new Uint8Array(len);
	for (let i = 0; i < len; i++) {
		bytes[i] = binaryString.charCodeAt(i);
	}
	return bytes;
};

//dvbase64 has no = padding. expand to multiple of 4 size to convert back to js.
var jsBase64ToDvBase64 = function(jsBase64){
	let s = ''; //TODO char array or something is faster?
	let end = jsBase64.indexOf('=');
	if(end == -1) end = jsBase64.length;
	for(let i=0; i<end; i++){
		s += digitJsToDv[jsBase64[i]];
	}
	return s;
};

//dvBase64Digits and Uint8Array
var base64ToBytes = function(base64){
	return jsBase64ToBytes(dvBase64ToJsBase64(base64));
};
	
//dvBase64Digits and Uint8Array
var bytesToBase64 = function(bytes){
	return jsBase64ToDvBase64(bytesToJsBase64(bytes));
};

var digitJsToDv = {}; //transforms between 2 sets of base64 digits
var digitDvToJs = {};
for(let i=0; i<65; i++){ //last digit is = for padding, but dv base64 doesnt use it. js base64 does.
	let jsDigit = jsBase64Digits[i];
	let dvDigit = dvBase64Digits[i];
	digitJsToDv[jsDigit] = dvDigit;
	digitDvToJs[dvDigit] = jsDigit;
}

//dvbase64 has no = padding. expand to multiple of 4 size to convert back to js.
var jsBase64ToDvBase64 = function(jsBase64){
	let s = ''; //TODO char array or something is faster?
	let end = jsBase64.indexOf('=');
	if(end == -1) end = jsBase64.length;
	for(let i=0; i<end; i++){
		s += digitJsToDv[jsBase64[i]];
	}
	return s;
};

var dvBase64ToJsBase64 = function(dvBase64){
	let s = ''; //TODO char array or something is faster?
	for(let i=0; i<dvBase64.length; i++){
		s += digitDvToJs[dvBase64[i]];
	}
	while(s.length&3){ //while not a multiple of 4
		s += '='; //pad
	}
	return s;
};

var testBase64ToFromBytes = ()=>{
	let listOfByteArrays = [Uint8Array.of(2,3,17,255,254,3,3,2,171,170,199),Uint8Array.of(10),Uint8Array.of(),Uint8Array.of(1,2,3,4),Uint8Array.of(1,2,3,4,5),Uint8Array.of(1,2,3,4,5,6),Uint8Array.of(1,2,3,4,5,6,7)];
	for(let testNum=0; testNum<listOfByteArrays.length; testNum++){
		let bytes = listOfByteArrays[testNum];
		let b64 = bytesToBase64(bytes);
		let bytesRebuilt = base64ToBytes(b64);
		if(bytes.length != bytesRebuilt.length) Err('bytesRebuilt different len');
		for(let i=0; i<bytes.length; i++) if(bytes[i] != bytesRebuilt[i]) Err('bytes[i] != bytesRebuilt[i] i='+i);
		console.log('testBase64ToFromBytes_'+testNum+' test pass, bytes='+[...bytes].join(',')+' base64='+b64);
	}
};
testBase64ToFromBytes();

//TODO rewrite these comments:
//return 192 <= bytes[offset];
//return QFORK <= bytes[offset]; //QFORK is just below the line, of things above fork and things below dont. its an opcode to fork without knowing the length yet.
var byteHasChilds = byt=>(QFORK <= byt);
//var hasChilds = (bytes, offset)=>byteHasChilds(bytes[offset]);

var hashStringToHex = function(str){
	return bytesToHex(sha256(stringToBytes(str)));
};
var hashStringToBase64 = function(str){
	//return dagball.bytesToBase64(sha256(stringToBytes(str))); //fixme remove === padding at end.
	return bytesToBase64(sha256(stringToBytes(str))); //fixme remove === padding at end.
};
var utf8TextEncoder = new TextEncoder('utf-8');
var utf8TextDecoder = new TextDecoder('utf-8');
var stringToBytes = function(s){ return utf8TextEncoder.encode(s); };
var bytesToString = function(bytes){ return utf8TextDecoder.decode(bytes); };
var hexDigits = '0123456789abcdef'.split('');
var mapOfHexDigitToInt = {}; //vals are 0 to 15. filled in boot.
var mapOfDoubleHexDigitsToInt = {}; //vals are 0 to 255. filled in boot.
var bytesToHex = function(bytes){ return bytesAndRangeToHex(bytes,0,bytes.length); };
var doubleHexDigits = [];
for(let i=0; i<16; i++){
	mapOfHexDigitToInt[hexDigits[i]] = i;
	for(let j=0; j<16; j++){
		let hh = hexDigits[i]+hexDigits[j];
		doubleHexDigits.push(hh);
		mapOfDoubleHexDigitsToInt[hh] = ((i<<4)|j);
	}
};
var bytesAndRangeToHex = function(bytes,from,toExcl){
	let s = '';
	for(let i=from; i<toExcl; i++) s += doubleHexDigits[bytes[i]];
	return s;
};

//Var class was copied 2025-4-16 from blobMonstersGame_2025-3-27.html then modified TODO...
//blobMonstersGame used V.testnet. BellSack/LamGL will use V.bellsack.room1 or V.bellsack.makeUpARoomName etc,
//and V.htmls to put the html in,
//like v.htmls.sha256$9dda0dee909c8e96c82caf183cd938a1e07c23c9c79c06d5b53e626b36b54efc.big = '<html>...</html>' will load in iframe here,
//but only whichever of them has nonzero (or highest?) v.htmls.someHtml24353245.p.
//
//V is the root Var of the tree of Vars. Each Var is a time-series of .p/position and .v/velocity and .t/time. gob.influence like dagball.Circ.influence
//and dagball.Ball.influence is a Var that if its .p/value is 1 it exists and if 0 does not exist, in that namespace.
const V = window.V = new Var(null, 'V'); //var Var = function(optionalParentVar, optionalName, optionalBig, optionalGob)