##注意事项：

- **本工程中执行 python 脚本时所用的 python 是 `.venv` 下的 python 执行器**，即 `.venv/bin/python`，禁止使用系统或其他 python。

- 在这个项目中编写正式测试代码之前，必须先遵循 Behaviour-Driven Development 的实践，使用 Gherkin Schema，写一个只包含 Given-When-Then 模式的行为注释的和测试函数名的空测试。并试用工具 AskUserQuestion 向用户确认是否继续。禁止在完成行为注释之前，编写任何测试代码。

- 在这个项目中的所有一次性执行代码，和临时代码 都只能放入 @examples/tmp 文件夹下，严禁将零散代码放入随机位置

- 在开发 mtsamples 信息源 相关的 provider 的时候，适当参考 @doc/mtsamples 下的知识点