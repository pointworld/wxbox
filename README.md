# Django —— 微信消息推送

参考：https://github.com/hyyc554/wxbox

## 前言

微信公众号的分类

  - 订阅号

  - 服务号

  - 企业号

基于：微信认证服务号 主动推送微信消息
前提：关注服务号
环境：沙箱环境

沙箱环境地址： https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login


## 流程：

1. 注册开发者账号

  获得：appID、appsecret

  网页授权获取用户基本信息：IP 或 域名 

2. 关注公众号（已认证的服务号）

3. 生成二维码，用户扫描
  将用户信息发送给微信，微信再将数据发送给设置 redirect_uri 地址(md5 值)

4. 回调地址：xxx/callback/

  - 授权 
  - 用户 md5
  - 获取 wx_id 
    在数据库中更新设置：wx_id 

5. 发送消息（模板消息）
  - wx_id 

  - access_token（2小时有效期）


## 功能演示

1 登陆

2 用户扫码关注我们的公众号


为了获得用户的微信 ID，我们需要用户再次扫码，向微信授权把 ID 给我们

