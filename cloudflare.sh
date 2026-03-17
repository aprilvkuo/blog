#!/bin/bash
# Cloudflare Pages 构建脚本

# 安装 pnpm
npm install -g pnpm

# 安装依赖
pnpm install

# 构建
pnpm run docs:build
