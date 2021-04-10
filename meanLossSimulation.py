# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 18:37:18 2021

@author: sebas
"""

import chess
import chess.engine
import random



def simulateWithMeanLoss(board, threshold, depth, maxContinuations, engine,
                         engineDepth=10, checkmateLoss = 1800):
    #Problem of checkmate loss. Here, as in the other program, it is given
    # as doubly worse than losing a queen. Ideally it would be -infinity, 
    # however this makes it impossible to compute some loss function.
    moves = []
    losses = []
    
    for i in range(depth):
        
        if board.is_game_over():
            return moves, sum(losses)/len(losses)
        
        anal = engine.analyse(board,chess.engine.Limit(depth=engineDepth),
                              multipv=maxContinuations)
        consideredMoves = []
        for j in range(len(anal)):
            consideredMoves.append([anal[j]["pv"][0], 
                                    anal[j]["score"].relative])
        
        for i in range(len(consideredMoves)):
            if consideredMoves[i][1].is_mate():
                if consideredMoves[i][1].mate() >= 0:
                    consideredMoves[i][1] = checkmateLoss
                else:
                    consideredMoves[i][1] = -checkmateLoss
            else:
                consideredMoves[i][1] = consideredMoves[i][1].score()
        meanEval = sum([x[1] for x in consideredMoves]) / len(consideredMoves)
        
        stopPoint = 0
        for j in range(len(consideredMoves)):
            if consideredMoves[0][1] - consideredMoves[j][1] > threshold:
                stopPoint = j
                break
        if stopPoint != 0:
            consideredMoves = consideredMoves[:stopPoint]
        
        loss = (consideredMoves[0][1] - meanEval)
        chosenMove = random.choice(consideredMoves)
        losses.append(loss)
        moves.append(chosenMove[0])
        board.push(chosenMove[0])
        
    return moves, sum(losses)/len(losses)


enginePath = "stockfish_13_win_x64_bmi2/stockfish_13_win_x64_bmi2.exe"
position = chess.Board("rnbqkb1r/p4ppp/2p1pn2/1p2P1B1/2pP4/2N2N2/PP3PPP/R2QKB1R b KQkq - 0 7")
threshold = 30
depth = 20
S = 100
maxContinuations = 8

engine = chess.engine.SimpleEngine.popen_uci(enginePath)

positions = {"Four Knights English Opening":"r1bqkb1r/pppp1ppp/2n2n2/4p3/2P5/2N2N2/PP1PPPPP/R1BQKB1R w KQkq - 4 4",
"Giuoco Piano":"r1bqk1nr/pppp1ppp/2n5/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4",
"Accelerated Dragon Maroczy Bind":"r1bqk1nr/pp1pppbp/2n3p1/8/2PNP3/8/PP3PPP/RNBQKB1R w KQkq - 1 6",
"Benko Gambit Fully Accepted":"rnbqkb1r/3ppp1p/P4np1/2pP4/8/8/PP2PPPP/RNBQKBNR w KQkq - 0 6",
"Dragon Yugoslav Attack 9.Bc4":"r1bq1rk1/pp2ppbp/2np1np1/8/2BNP3/2N1BP2/PPPQ2PP/R3K2R b KQ - 4 9",
"Botvinnik Semi-Slav":"rnbqkb1r/p4ppp/2p1pn2/1p4B1/2pPP3/2N2N2/PP3PPP/R2QKB1R w KQkq - 0 7",
"Winawer Poisoned Pawn":"rnbqk2r/pp2nppp/4p3/2ppP3/3P2Q1/P1P5/2P2PPP/R1B1KBNR b KQkq - 1 7",
"Najdorf Poisoned Pawn":"rnb1kb1r/1p3ppp/pq1ppn2/6B1/3NPP2/2N5/PPPQ2PP/R3KB1R b KQkq - 2 8",
"King's Gambit":"rnbqkbnr/pppp1ppp/8/4p3/4PP2/8/PPPP2PP/RNBQKBNR b KQkq - 0 2"}

for k in positions.keys():
    position = chess.Board(positions[k])
    games = []
    losses = []
    for i in range(S):
        sim = simulateWithMeanLoss(position.copy(), threshold, depth, maxContinuations, engine)
        games.append(sim[0])
        losses.append(sim[1])
       
    meanLoss = sum(losses)/len(losses)
    print("%s: %f" % (k, meanLoss))