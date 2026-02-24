# 使用 GitHub Actions 编译手机端和电视端 App

本文档说明如何把当前项目接入 **GitHub Actions 自动编译 APK**。

## 1. 目录约定

工作流默认按下面目录寻找 Android 工程：

- 手机端：`apps/mobile-android`
- 电视端：`apps/tv-android`

每个目录至少需要：

- `gradlew`
- `settings.gradle` 或 `settings.gradle.kts`
- 可执行构建任务：`assembleRelease`

> 你目前仓库主要是架构代码与文档，还没有完整 Android 工程。要真正产出 APK，需要先把手机端/电视端 Android 项目放到上述目录。

## 2. 已添加的工作流

已添加：`.github/workflows/android-build.yml`

功能：
- 支持手动触发（`workflow_dispatch`）
- 支持按代码变更自动触发（push / pull_request）
- 可选择仅编译 mobile、仅编译 tv 或全部
- 自动上传 APK 产物（Artifacts）
- 若对应 Android 工程目录尚未就绪，会给出 warning 并跳过，不再直接失败

## 3. 手动触发编译

1. 打开 GitHub 仓库页面。
2. 进入 **Actions**。
3. 选择 **Build Android Apps (Mobile + TV)**。
4. 点击 **Run workflow**。
5. 选择 `target`：
   - `all`：手机端 + 电视端
   - `mobile`：仅手机端
   - `tv`：仅电视端
6. 运行完成后，在该次任务的 **Artifacts** 下载：
   - `mobile-release-apk`
   - `tv-release-apk`

## 4. 签名建议（发布到商店前）

当前工作流执行 `assembleRelease`，但是否签名取决于你的 Gradle 配置。

建议在 GitHub Secrets 中配置：
- `ANDROID_KEYSTORE_BASE64`
- `ANDROID_KEYSTORE_PASSWORD`
- `ANDROID_KEY_ALIAS`
- `ANDROID_KEY_PASSWORD`

然后在 workflow 中新增“解码 keystore + 写入 `local.properties`/环境变量”的步骤，并在 `build.gradle` 中读取这些变量进行 release 签名。

## 5. 常见失败原因

1. **找不到 `gradlew`**
   - 现在会在 Actions 日志中给出 warning，并跳过对应端构建。
   - 说明 Android 工程还未放到 `apps/mobile-android` 或 `apps/tv-android`。
2. **找不到 release APK**
   - 说明模块任务或输出路径和默认不一致，需要调整 artifact 路径。
3. **JDK 版本不匹配**
   - 可把 workflow 中 Java 版本从 17 调整为你项目要求的版本。

## 6. 下一步落地建议

1. 先创建两个 Android 工程骨架（mobile/tv）。
2. 把当前 Python 架构逻辑迁移为 Android 可用模块（Kotlin）。
3. 首先打通“连接 + 遥控 + DDNS 状态”基础链路，再接入 WebRTC 看屏。
