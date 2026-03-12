# Study Python — 給 iOS / Web 開發者的 Python 學習筆記

> 本倉庫面向有 **Swift (iOS)** 和 **JavaScript / TypeScript (Web)** 經驗的開發者，透過類比你已經熟悉的概念來快速掌握 Python。

## 目錄結構

```
docs/
├── 01-basics/           # 基礎篇 — 快速入門
│   ├── 01-setup.md          環境設置與開發工具
│   ├── 02-syntax.md         基本語法（對比 Swift / JS）
│   ├── 03-data-types.md     資料型別
│   ├── 04-control-flow.md   流程控制
│   └── 05-functions.md      函數
│
├── 02-intermediate/     # 進階篇 — 深入核心
│   ├── 01-oop.md            物件導向程式設計（對比 Swift / JS class）
│   ├── 02-modules.md        模組與套件
│   ├── 03-error-handling.md 錯誤處理（對比 try-catch）
│   ├── 04-file-io.md        檔案操作
│   └── 05-iterators.md      迭代器與生成器
│
├── 03-practical/        # 實用篇 — 工程實踐
│   ├── 01-stdlib.md         常用標準庫
│   ├── 02-package-mgmt.md   虛擬環境與套件管理（對比 npm / CocoaPods）
│   ├── 03-networking.md     網路請求（對比 URLSession / fetch）
│   └── 04-database.md       資料庫操作
│
├── 04-web-dev/          # Web 開發篇
│   ├── 01-flask.md          Flask 入門
│   └── 02-rest-api.md       REST API 開發（對比 Express / Vapor）
│
└── 05-advanced/         # 進階主題
    ├── 01-decorators.md     裝飾器
    ├── 02-async.md          非同步程式設計（對比 async/await）
    └── 03-type-hints.md     型別提示（對比 TypeScript / Swift 強型別）
```

## 閱讀建議

| 你的背景 | 建議路線 |
|---------|---------|
| 想快速上手寫程式 | 01-basics → 02-intermediate → 挑需要的看 |
| 想用 Python 做後端 | 01-basics → 02-intermediate → 04-web-dev |
| 想做資料處理/自動化 | 01-basics → 03-practical |
| 想全面學習 | 按順序從 01 到 05 |

## 概念對照速查

| 概念 | Swift | JavaScript | Python |
|-----|-------|------------|--------|
| 套件管理 | SPM / CocoaPods | npm / yarn | pip / poetry |
| 專案隔離 | Xcode workspace | node_modules | venv / virtualenv |
| 型別系統 | 強型別（編譯期） | 弱型別（動態） | 強型別（動態） |
| 空值 | `nil` / `Optional` | `null` / `undefined` | `None` |
| 字串插值 | `"\(variable)"` | `` `${variable}` `` | `f"{variable}"` |
| 介面/協議 | `protocol` | `interface` (TS) | `ABC` / `Protocol` |
| 非同步 | `async/await` | `async/await` / Promise | `asyncio` / `async/await` |
| 閉包 | `{ }` closure | `() => {}` arrow fn | `lambda` / 一般函數 |
| 列舉 | `enum` | 無原生 / TS `enum` | `Enum` class |

## 環境需求

- Python 3.10+（建議 3.12）
- 推薦編輯器：VS Code + Python 擴充套件 / Cursor
