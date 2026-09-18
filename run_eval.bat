@echo off
chcp 65001 > nul
title StoryboardAI - Evaluation Runner (Run 1)
echo ========================================================
echo  KHOI CHAY EVALUATION RUN 1 (20 CASES GOLDEN SET)
echo  Nhom: K4-3B-E403-BotVN (Hai - Hoang - Dai)
echo ========================================================
echo.
python eval/run_eval.py
pause
