// POST /api/analyze - 提交股票分析任务
// 请求体：{ "symbol": "多氟多", "stock_code?: "002594.SZ" }
// 返回：{ "task_id": "xxx", "status": "pending" }

import type { PagesFunction } from '@cloudflare/workers-types'

interface Env {
  TASKS_KV: KVNamespace
}

interface Task {
  id: string
  symbol: string
  stock_code?: string
  status: 'pending' | 'running' | 'completed' | 'failed'
  created_at: number
  updated_at: number
  result?: {
    report_path?: string
    error?: string
  }
}

export const onRequest: PagesFunction<Env> = async ({ request, env }) => {

  try {
    const body = await request.json()
    const { symbol, stock_code } = body

    if (!symbol) {
      return new Response(JSON.stringify({ error: 'Missing symbol' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      })
    }

    // 生成任务 ID
    const taskId = `task_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`
    const now = Date.now()

    // 创建任务对象
    const task: Task = {
      id: taskId,
      symbol,
      stock_code,
      status: 'pending',
      created_at: now,
      updated_at: now,
    }

    // 存入 KV
    await env.TASKS_KV.put(`task:${taskId}`, JSON.stringify(task))

    // 更新任务列表索引（方便轮询）
    const pendingKey = `pending:${taskId}`
    await env.TASKS_KV.put(pendingKey, JSON.stringify({ symbol, stock_code, created_at: now }))

    return new Response(JSON.stringify({
      task_id: taskId,
      status: 'pending',
      message: '任务已提交，等待处理',
    }), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    })
  } catch (error) {
    console.error('Error creating task:', error)
    return new Response(JSON.stringify({ error: 'Internal server error' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    })
  }
}
