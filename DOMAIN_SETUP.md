# 自定义域名绑定指南

## 📋 前提条件

- 已在 Streamlit Cloud 成功部署应用
- 拥有自己的域名(如 `example.com`)
- 可以访问域名的 DNS 管理面板

> ⚠️ **重要提示**: Streamlit Community Cloud (免费版) **不支持自定义域名**功能。
> 
> 如需使用自定义域名,您需要:
> - 升级到 **Streamlit Cloud Teams** 或 **Enterprise** 计划
> - 或使用其他部署方案(见下方替代方案)

## 🔧 绑定步骤

### 1. 在 Streamlit Cloud 配置自定义域名

**最新步骤 (2024+ 界面):**

1. 登录 [Streamlit Cloud](https://share.streamlit.io/)
2. 找到您的应用,点击应用右侧的 **⋮** (三个点) 菜单
3. 选择 **Settings** (设置)
4. 在左侧菜单中找到 **Domains** 或 **Custom domains**
5. 点击 **Add domain** 或 **Connect domain**
6. 输入您的域名,例如:
   - `dashboard.yourdomain.com` (推荐使用子域名)
   - 或 `yourdomain.com` (使用主域名)

**如果找不到设置:**
- 确保您的应用已成功部署
- 某些免费账户可能需要升级才能使用自定义域名
- 尝试访问: `https://share.streamlit.io/` 查看应用列表

### 2. 获取 DNS 配置信息

Streamlit Cloud 会提供需要添加的 DNS 记录,通常是:

**使用子域名 (推荐)**
```
类型: CNAME
名称: dashboard (或您想要的子域名)
值: your-app.streamlit.app
```

**使用主域名**
```
类型: A
名称: @
值: Streamlit Cloud 提供的 IP 地址
```

### 3. 配置 DNS 记录

#### 常见域名服务商配置方法:

**阿里云 (Aliyun)**
1. 登录 [阿里云控制台](https://dns.console.aliyun.com)
2. 进入 **域名解析** → 选择您的域名
3. 点击 **添加记录**
4. 填写:
   - 记录类型: `CNAME`
   - 主机记录: `dashboard` (子域名前缀)
   - 记录值: `your-app.streamlit.app`
   - TTL: `10分钟` (默认)
5. 点击 **确认**

**腾讯云 (Tencent Cloud)**
1. 登录 [DNSPod 控制台](https://console.dnspod.cn)
2. 选择域名 → **添加记录**
3. 配置同上

**Cloudflare**
1. 登录 Cloudflare Dashboard
2. 选择域名 → **DNS** → **Records**
3. 点击 **Add record**
4. 填写:
   - Type: `CNAME`
   - Name: `dashboard`
   - Target: `your-app.streamlit.app`
   - Proxy status: 关闭 (灰色云朵)
5. 保存

**GoDaddy**
1. 登录 GoDaddy 账户
2. **我的产品** → **DNS**
3. 添加 CNAME 记录

### 4. 验证配置

DNS 配置生效通常需要 **5-30 分钟**,最长可能需要 48 小时。

**检查方法:**

```bash
# 检查 DNS 是否生效
nslookup dashboard.yourdomain.com

# 或使用 dig 命令
dig dashboard.yourdomain.com
```

### 5. 在 Streamlit Cloud 完成绑定

1. 返回 Streamlit Cloud 设置页面
2. 点击 **Verify** (验证)
3. 等待验证通过
4. 绑定成功后,访问您的自定义域名即可

## 🌐 推荐配置

### 使用子域名 (最佳实践)
```
dashboard.yourdomain.com  →  房产成交数据看板
api.yourdomain.com        →  API 服务
www.yourdomain.com        →  官网
```

### 启用 HTTPS

Streamlit Cloud 自动为自定义域名提供免费的 SSL 证书 (Let's Encrypt),无需额外配置。

## ⚠️ 常见问题

### DNS 配置后无法访问?
- 等待 DNS 传播 (5-30 分钟)
- 清除浏览器缓存
- 使用无痕模式测试
- 检查 DNS 记录是否正确

### Cloudflare 用户注意
- 必须关闭 **Proxy** (代理) 功能
- 云朵图标应为 **灰色** (DNS only)

### 域名已被其他服务使用?
- 使用子域名,如 `data.yourdomain.com`
- 避免与现有服务冲突

## 📊 完整示例

假设您的域名是 `example.com`,应用名是 `hangzhou-real-estate-dashboard`:

1. **Streamlit Cloud 提供的默认地址:**
   ```
   https://hangzhou-real-estate-dashboard.streamlit.app
   ```

2. **配置自定义域名:**
   ```
   dashboard.example.com
   ```

3. **DNS 配置 (阿里云示例):**
   ```
   记录类型: CNAME
   主机记录: dashboard
   记录值: hangzhou-real-estate-dashboard.streamlit.app
   TTL: 600
   ```

4. **最终访问地址:**
   ```
   https://dashboard.example.com
   ```

## 🎉 完成

配置成功后,您可以通过自定义域名访问应用,同时保留原始的 `.streamlit.app` 域名作为备用。

---

## 🆓 免费替代方案

如果您使用的是 Streamlit Community Cloud (免费版),可以通过以下方式使用自定义域名:

### 方案 1: Cloudflare Workers (推荐,完全免费)

使用 Cloudflare Workers 作为反向代理:

1. **注册 Cloudflare 并添加域名**
   - 访问 https://cloudflare.com
   - 添加您的域名并更新 NS 记录

2. **创建 Worker**
   ```javascript
   addEventListener('fetch', event => {
     event.respondWith(handleRequest(event.request))
   })
   
   async function handleRequest(request) {
     const url = new URL(request.url)
     url.hostname = 'your-app.streamlit.app'
     
     const modifiedRequest = new Request(url, {
       method: request.method,
       headers: request.headers,
       body: request.body
     })
     
     return fetch(modifiedRequest)
   }
   ```

3. **绑定自定义域名**
   - 在 Worker 设置中添加自定义域名
   - Cloudflare 自动配置 DNS

### 方案 2: Vercel/Netlify 反向代理

虽然不能直接部署 Streamlit,但可以用作反向代理:

**Vercel 配置 (`vercel.json`):**
```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "https://your-app.streamlit.app/$1"
    }
  ]
}
```

### 方案 3: 自建服务器 + Nginx

如果您有 VPS 或云服务器:

**Nginx 配置:**
```nginx
server {
    listen 80;
    server_name dashboard.yourdomain.com;
    
    location / {
        proxy_pass https://your-app.streamlit.app;
        proxy_set_header Host your-app.streamlit.app;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 方案 4: Railway/Render (支持自定义域名)

**Railway.app (推荐):**
- 免费额度: $5/月
- 支持自定义域名
- 部署步骤:
  1. 连接 GitHub 仓库
  2. 添加启动命令: `streamlit run app.py --server.port=$PORT`
  3. 在设置中添加自定义域名

**Render.com:**
- 免费层可用
- 支持自定义域名
- 自动 HTTPS

## 💰 费用对比

| 方案 | 费用 | 自定义域名 | 难度 |
|------|------|-----------|------|
| Streamlit Community Cloud | 免费 | ❌ | ⭐ |
| Streamlit Teams | $20+/月 | ✅ | ⭐ |
| Cloudflare Workers | 免费 | ✅ | ⭐⭐ |
| Railway | $5/月额度 | ✅ | ⭐⭐ |
| Render | 免费 | ✅ | ⭐⭐ |
| 自建 VPS + Nginx | $5+/月 | ✅ | ⭐⭐⭐ |

---

**需要帮助?** 
- [Streamlit 官方文档](https://docs.streamlit.io/)
- [Cloudflare Workers 文档](https://developers.cloudflare.com/workers/)
- [Railway 部署指南](https://docs.railway.app/)
- [DNS 配置教程](https://www.cloudflare.com/learning/dns/dns-records/dns-cname-record/)

