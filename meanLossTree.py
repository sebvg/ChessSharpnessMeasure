# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 16:31:14 2021

@author: sebas
"""

import chess
import chess.engine

class MoveTree:
    def __init__(self,move,e):
        self.children = []
        self.move = move
        self.eval = e
        self.RSS = None
        
    def addChild(self, child):
        self.children.append(child)


def viableMoves(board, threshold, engine, maxContinuations, engineDepth,
                checkmateLoss = 1800):
    #returns list of viable moves in the given position and their evaluations, 
    #as well as the average loss for the first maxContinuations moves in the 
    #position
    #Checkmate loss is a problem in this method of evaluation, as checkmate
    #has no numeric evaluation and we thus have to assign one. Here I have
    #set it to 1800, which is the equivalent of losing two queens. Although
    #infinite would be more accurate, it makes the mean loss explode.
    anal = engine.analyse(board, chess.engine.Limit(depth=engineDepth),
                          multipv = maxContinuations)
    consideredMoves = []
    for x in anal:
        consideredMoves.append([x["pv"][0], x["score"].relative])
        
    for i in range(len(consideredMoves)):
        #This loop adjusts scores for checkmates, which have no numeric eval.
        #It has to sort for checkmates as black or as white; since evaluations
        #are relative, this is done through evaluating an inequality in the
        #chess Mate object.
        #Otherwise, you can just use the .score() function; the checkmate
        # problem is minor and doesn't come up often, but some positions do 
        # evaluate to checkmates in some number of moves.
        if consideredMoves[i][1].is_mate():
            if consideredMoves[i][1].mate() >= 0:
                consideredMoves[i][1] = checkmateLoss
            else:
                consideredMoves[i][1] = - checkmateLoss
        else:
            consideredMoves[i][1] = consideredMoves[i][1].score()
            
            
    meanEval = sum([x[1] for x in consideredMoves]) / len(consideredMoves)
    meanLoss = consideredMoves[0][1] - meanEval
    
    stoppingPoint = 0
    for j in range(len(consideredMoves)):
        if consideredMoves[0][1] - consideredMoves[j][1] > threshold:
            stoppingPoint = j
            break     
    if stoppingPoint != 0:
        consideredMoves = consideredMoves[:stoppingPoint]           
        
    return consideredMoves, meanLoss


def populateTree(tree, board, depth, threshold, engine, engineDepth, 
                 maxContinuations):
    #Populates an empty tree from a given root, giving all engine moves
    #below a certain thresholds as variations, and returning the loss of each
    #position.
    if depth != 0:
        v, tree.RSS = viableMoves(board, threshold, engine, maxContinuations, 
                                  engineDepth)
        for move in v:
            tree.addChild(MoveTree(move[0],move[1]))
        
        for child in tree.children:
            board.push(child.move)
            populateTree(child, board, depth-1, threshold, engine,
                         engineDepth, maxContinuations)
            board.pop()
    else:
        return
    
def setMeanRSS(tree, total=0, count=0):
    #Iterates through a populated move tree, collecting the mean loss of
    #each variation.
    if len(tree.children)==0:
        listOfRSS.append(total/count)
    else:
        for child in tree.children:
            setMeanRSS(child, total + tree.RSS, count+1)
            #Not my favourite way of doing this. I would like to avoid
            #the global variable listOfRSS.
    
enginePath = "stockfish_13_win_x64_bmi2/stockfish_13_win_x64_bmi2.exe"
engine = chess.engine.SimpleEngine.popen_uci(enginePath)
board = chess.Board("rnbqkb1r/p4ppp/2p1pn2/1p2P1B1/2pP4/2N2N2/PP3PPP/R2QKB1R b KQkq - 0 7")

threshold = 30
depth = 6
maxContinuations = 8
engineDepth = 10

positions = {"Queen's Indian":"rn1qkb1r/p1pp1ppp/bp2pn2/8/2PP4/1P3NP1/P3PP1P/RNBQKB1R b KQkq - 0 5",
"Caro-Kann Short Variation":"rn1qkbnr/pp3ppp/2p1p3/3pPb2/3P4/5N2/PPP1BPPP/RNBQK2R b KQkq - 1 5",
"Queen's Gambit Declined Exchange Variation":"rnbqkb1r/ppp2ppp/5n2/3p2B1/3P4/2N5/PP2PPPP/R2QKBNR b KQkq - 1 5",
"Exchange Caro-Kann":"rnbqkbnr/pp2pppp/8/3p4/3P4/3B4/PPP2PPP/RNBQK1NR b KQkq - 1 4",
"Four Knights English Opening":"r1bqkb1r/pppp1ppp/2n2n2/4p3/2P5/2N2N2/PP1PPPPP/R1BQKB1R w KQkq - 4 4",
"Giuoco Piano":"r1bqk1nr/pppp1ppp/2n5/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4",
"Accelerated Dragon Maroczy Bind":"r1bqk1nr/pp1pppbp/2n3p1/8/2PNP3/8/PP3PPP/RNBQKB1R w KQkq - 1 6",
"Benko Gambit Fully Accepted":"rnbqkb1r/3ppp1p/P4np1/2pP4/8/8/PP2PPPP/RNBQKBNR w KQkq - 0 6",
"Dragon Yugoslav Attack 9.Bc4":"r1bq1rk1/pp2ppbp/2np1np1/8/2BNP3/2N1BP2/PPPQ2PP/R3K2R b KQ - 4 9",
"Botvinnik Semi-Slav":"rnbqkb1r/p4ppp/2p1pn2/1p4B1/2pPP3/2N2N2/PP3PPP/R2QKB1R w KQkq - 0 7",
"Winawer Poisoned Pawn":"rnbqk2r/pp2nppp/4p3/2ppP3/3P2Q1/P1P5/2P2PPP/R1B1KBNR b KQkq - 1 7",
"Najdorf Poisoned Pawn":"rnb1kb1r/1p3ppp/pq1ppn2/6B1/3NPP2/2N5/PPPQ2PP/R3KB1R b KQkq - 2 8",
"King's Gambit":"rnbqkbnr/pppp1ppp/8/4p3/4PP2/8/PPPP2PP/RNBQKBNR b KQkq - 0 2"}

for k in positions.keys():
    board = chess.Board(positions[k])

    root = MoveTree(None, None)
    populateTree(root, board, depth, threshold, engine, engineDepth,
                 maxContinuations)
    listOfRSS = []
    setMeanRSS(root)
    meanLoss = sum(listOfRSS)/len(listOfRSS)
    print("%s: %f" % (k, meanLoss))