@echo off
echo 启动崩坏星穹铁道角色管理系统...
echo.

echo 启动Flask后端服务器（端口5000）...
start "Flask Backend" cmd /k "cd /d %~dp0backend && python app.py"

echo 等待2秒...
timeout /t 2 /nobreak >nul

echo 启动HTTP文件服务器（端口8080）...
start "HTTP Server" cmd /k "cd /d %~dp0 && python -m http.server 8080"

echo.
echo 服务器启动完成！
echo 请等待几秒钟，然后访问：
echo   - 数据维护页面: http://localhost:8080/frontend/data_maintain.html
echo   - 简单测试页面: http://localhost:8080/frontend/test_simple.html
echo.
echo 按任意键关闭此窗口...
pause >nul 