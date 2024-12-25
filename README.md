# 学生管理系统 (Yueosa-StudentSystemWeb)

时间2024年12月，老师要求制作学生管理系统的Web版本，于是我便开始了这个项目的开发。
这个项目是一个基于 Python 搭建的 Web 应用程序，前端由 HTML、CSS、JavaScript 编写，后端使用 Flask 框架实现。

## 功能
- **用户注册**：用户可以通过注册页面创建新账户。
- **查看信息**：注册的用户可以登录并查看所有学生信息。
- **管理员功能**：管理员用户可以对学生信息和用户账户进行增、删、查、改等操作。
- **密码加密**：用户密码在数据库中加密保存（使用 SHA256 算法），保证用户信息安全。

## 项目克隆

要将该项目下载到你的本地仓库，请执行以下步骤：

1. **克隆项目**：
   打开终端（命令行），并运行以下命令将项目克隆到本地：

   ```bash
   git clone https://github.com/Yueosa/Yueosa-StudentSystemWeb.git
   ```

   或者使用 Git 克隆项目。

   ```bash
   git clone git@github.com:Yueosa/Yueosa-StudentSystemWeb.git
   ```
### 运行 Web 服务器

2. **启动 Web 应用程序**  
   在安装完所有依赖之后，运行 `app.py` 启动 Flask 开发 Web 服务器：

   ```bash
   python app.py
3. **开放到局域网**  
   如果你希望让局域网中的其他设备也能访问这个 Web 服务器，你需要修改 app.py 文件中的 app.run() 配置，将 host 设置为 '0.0.0.0'，这样 Web 服务器就会监听所有的 IP 地址(项目中已配置)：

   ```python
   app.run(host='0.0.0.0', port=5000)
   ```
   在这种配置下，其他设备可以通过你计算机的局域网 IP 地址加上端口号访问该 Web 服务器。例如，如果你的计算机局域网 IP 地址是 192.168.1.5，那么可以通过 http://192.168.1.5:5000 在其他设备的浏览器中访问该网站。
