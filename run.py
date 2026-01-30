#!/usr/bin/env python3
"""
Pokemon API 启动脚本
"""
import os
import sys
import subprocess

def check_dependencies():
    """检查依赖是否已安装"""
    try:
        import fastapi
        import uvicorn
        return True
    except ImportError:
        print("依赖包未安装！")
        print("请先运行安装脚本安装依赖：")
        if sys.platform == "win32":
            print("  Windows: install.bat")
        else:
            print("  其他系统: sh install.sh")
        return False

def main():
    """主函数"""
    if not check_dependencies():
        sys.exit(1)
    
    print("=========================================")
    print("  Pokemon API - 启动服务")
    print("========================================")
    print()
    
    # 检查.env文件
    if not os.path.exists('.env'):
        print("警告：未找到.env文件！")
        print("建议先复制.env.example为.env：")
        print("  cp .env.example .env")
        print()
        response = input("是否现在复制.env.example为.env？(y/n): ")
        if response.lower() == 'y':
            import shutil
            shutil.copy('.env.example', '.env')
            print("已复制.env.example为.env")
        else:
            print("请先配置.env文件")
            return
    
    print("启动FastAPI开发服务器...")
    print()
    print("访问地址：")
    print("  - API文档: http://localhost:8000/docs")
    print("  - 管理后台: http://localhost:8000/admin")
    print()
    
    # 启动服务器
    try:
        subprocess.run([sys.executable, "-m", "uvicorn", "app.main:app", 
                      "--host", "0.0.0.0", "--port", "8000", "--reload"])
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"\n启动失败：{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()