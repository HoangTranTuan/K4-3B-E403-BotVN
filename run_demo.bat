@echo off
chcp 65001 > nul
title StoryboardAI - Live Web App Server
echo ========================================================
echo  🎬 KHOI CHAY GIAO DIEN STORYBOARD AI (TRACK C)
echo  Nhom: K4-3B-E403-BotVN (Hai - Hoang - Dai)
echo  Dia chi truy cap: http://localhost:8501
echo  Dang tu dong mo trinh duyet...
echo ========================================================
echo.
python codebase/app_server.py
pause
