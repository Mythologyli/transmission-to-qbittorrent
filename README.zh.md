# Transmission to qBittorrent

将 [Transmission](https://transmissionbt.com/) 中的种子全部转移至 [qBittorrent](https://www.qbittorrent.org/)。支持跳过校验。

**警告：谨慎使用！作者不为一切跳检造成的后果负责**

## 使用方法

1. 下载项目。

2. 确保脚本可以访问到 Transmission 的种子文件目录。
   
   种子文件目录包含所有种子文件，文件命名方式为种子 hash.torrent。
   
3. 若 Transmission 和 qBittorrent 运行在 Docker 容器中，还需确保所有种子的下载路径在两个 Docker 容器中的对应路径相同，即将宿主机同一文件夹挂载到两个 Docker 容器的相同目录中。

4. 确保已配置 Python 3 运行环境。

5. 进入项目目录，依照 config.json.template 创建 config.json 文件。各字段如下：

   + skip_check: 填写 true 跳过校验。填写 false 不跳过校验。不可加双引号
   + qbittorrent: qBittorrent 相关配置
     + host: 填写 qBittorrent Web 服务的 IP 地址。一般为本机，填 127.0.0.1
     + port: 填写 qBittorrent Web 服务的 IP 地址。一般为 8080
     + username: 登录用户名
     + password: 登录密码
   + transmission: Transmission 相关配置
     + protocol: 填写 "http" 或 "https"
     + host: 填写 Transmission Web 服务的 IP 地址。一般为本机，填 127.0.0.1
     + port: 填写 Transmission Web 服务的端口。一般为 9091。不可加双引号
     + path: 一般填 "/transmission/"，无需修改
     + username: 登录用户名
     + password: 登录密码
     + torrent_dir: 种子文件目录。应填写**相对于 Python 解释器的路径**

6. 运行脚本：`python3 main.py` 或 `python main.py`。

7. 运行完成后，Transmission 和 qBittorrent 中的所有种子将处于暂停状态，请手动开始种子。

## 感谢

+ [qbittorrent-api](https://github.com/rmartin16/qbittorrent-api)
+ [transmission-rpc](https://github.com/trim21/transmission-rpc)