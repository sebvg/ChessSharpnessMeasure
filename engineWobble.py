# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 15:54:01 2021

@author: sebas
"""

import chess
import chess.engine

def complexity(board, engine, minDepth=2, maxDepth=16):
    c=0
    bestMove = engine.analyse(board, chess.engine.Limit(depth=minDepth))["pv"][0]
    
    for i in range(minDepth+2, maxDepth+1, 2):
        analysis = engine.analyse(board, chess.engine.Limit(depth= i ), multipv=2)
        if analysis[0]["pv"][0] != bestMove:
            bestMove = analysis[0]["pv"][0]
            c += analysis[0]["score"].relative.score() - analysis[1]["score"].relative.score()
            
    return c


sf12Path = "stockfish_13_win_x64_bmi2/stockfish_13_win_x64_bmi2.exe"
sf8Path = "stockfish-8-win/Windows/stockfish_8_x64.exe"

engine = chess.engine.SimpleEngine.popen_uci(sf8Path)

position = chess.Board("rnbqk1nr/pp3ppp/4p3/b1ppP3/3P4/P1N5/1PP2PPP/R1BQKBNR w KQkq - 1 6")



