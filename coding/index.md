---
title: 编程开发概述
description: 编程开发相关的技术笔记和最佳实践
---

# 编程开发概述

编程是将人类思维转化为计算机可执行指令的过程。

## 技术栈

### 前端开发

前端开发涉及用户界面和交互：

```typescript
// React 组件示例
import { useState } from 'react'

interface Props {
  title: string
}

export function Counter({ title }: Props) {
  const [count, setCount] = useState(0)

  return (
    <div>
      <h1>{title}</h1>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        增加
      </button>
    </div>
  )
}
```

### 后端开发

后端处理数据和业务逻辑。

### DevOps

自动化部署和运维。

## 开发工具

- **编辑器**: VS Code, Neovim
- **版本控制**: Git
- **包管理**: pnpm, npm, yarn
- **构建工具**: Vite, Webpack, esbuild

## 代码规范

```javascript
// 好的命名
const getUserProfile = (userId) => {
  // ...
}

// 避免的命名
const getUserData123 = (id) => {
  // ...
}
```

> 代码是写给人看的，只是恰好能被机器执行。
