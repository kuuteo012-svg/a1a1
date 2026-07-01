@echo off
chcp 65001 >nul
title BOT AUTO CODE v7.5

cd /d "%~dp0"

:: Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [LOI] Khong tim thay Python. Hay cai Python 3.10+ va thu lai.
    pause
    exit /b 1
)

:: Kích hoạt venv nếu có
if exist "venv\Scripts\activate.bat" (
    echo [*] Kich hoat virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo [CANH BAO] Khong tim thay venv - chay voi Python he thong
)

:: Cài toàn bộ dependencies
echo [*] Kiem tra va cai thu vien...
pip install -r requirements.txt -q --disable-pip-version-check

:: Cài Camoufox nếu chưa có
echo [*] Kiem tra Camoufox...
python -c "import camoufox" >nul 2>&1
if errorlevel 1 (
    echo [*] Cai camoufox...
    pip install camoufox[geoip]==0.4.11 -q
    python -m camoufox fetch
)

:: Chạy bot
echo.
echo ============================================================
echo   BOT AUTO CODE v7.5
echo   Camoufox Firefox  ^|  Anti-detection ON  ^|  Bypass Turnstile
echo ============================================================
echo.
echo  Luu y:
echo   - Bot tu dong mo Firefox (Camoufox), KHONG can mo Edge/Chrome truoc
echo   - Lan dau chay: dang nhap Telegram va xu ly Cloudflare thu cong
echo   - Log luu tai: logs\bot_activity.log
echo   - Bam X cua so nay: bot tu dong tat sach (cho toi da 8 giay)
echo.
echo ============================================================
echo.

python main_script.py

:: ✅ Dọn dẹp sau khi bot tắt (dù tắt bằng X hay Ctrl+C)
:: Đóng Firefox/Camoufox nếu còn sót lại
echo [*] Don dep tien trinh con lai...
taskkill /F /IM firefox.exe /T >nul 2>&1
taskkill /F /IM camoufox.exe /T >nul 2>&1

echo.
echo ============================================================
echo   Bot da dung.
echo ============================================================
echo.
pause