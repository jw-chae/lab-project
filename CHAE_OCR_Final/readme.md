# README.md

## 用于PaddleOCR的Anaconda安装和环境设置

### 安装Anaconda

1. 访问Anaconda发行版页面 https://www.anaconda.com/distribution/。
2. 选择适用于您的操作系统的版本（Windows，macOS，Linux）。
3. 下载Anaconda的Python 3.9版本。
4. 运行安装程序并按照屏幕上的提示进行操作。在安装设置中记得勾选"将Anaconda添加到我的PATH环境变量"的选项。

### ⚠️ 警告

- 确保在您的系统变量中不存在可能与Anaconda Python冲突的其他Python路径。Anaconda应该是您系统变量中唯一的Python路径。
- 该设置假定您正在使用Python 3.9。其他版本可能导致不同的结果或错误。


`requirements.txt`文件列出了您的项目所依赖的所有Python库和它们的版本。您可以使用这个文件一次性安装所有的库。首先，您需要在已激活的Python环境或虚拟环境中运行以下命令：

```shell
pip install -r requirements.txt
```

这个命令将安装`requirements.txt`文件中列出的所有库及其对应的版本。
### 在PyCharm中选择Anaconda环境

1. 打开PyCharm。
2. 转到`File` -> `Settings` -> `Project:YourProjectName` -> `Python Interpreter`。
3. 点击齿轮图标，然后点击`Add`。
4. 在左窗格中，选择`Conda Environment` -> `Existing environment`。
5. 点击`...`按钮并导航到您的Anaconda目录（通常在主目录或Windows上的`C:\Users\your-username\Anaconda3\envs\`）。在`paddleocr`环境中选择`python.exe`文件。
6. 点击`OK`。

现在，PyCharm将使用您刚刚创建的`paddleocr`环境中的Python解释器。

## 额外说明：设置摄像头和模板、调整OCR网格和特征匹配

1. **CaptureThread类**：这个类负责图像捕获。它可以用于从特定的摄像头捕获图像并保存到输出文件夹。可以通过`cv2.CAP_PROP_FRAME_WIDTH`和`cv2.CAP_PROP_FRAME_HEIGHT`来调整图像的分辨率。如果想要调整图像的大小，修改代码中对应的部分。

2. **模板选择**：`front_templates`和`behind_templates`是包含图像分析中使用的模板路径的列表。这些模板用于在图像中找到特定的模式或对象。如果摄像头编号改变，你需要更改这些以匹配适当的模板。

3. **在OCR_Thread中调整网格**：在`OCR_Thread`中，你可以通过更改`x_grid`和`y_grid`的值来调整作为OCR处理结果生成的csv文件的大小。这些值用于将OCR结果划分为网格。

4. **在debug_preprocess.py中进行特征匹配**：在`debug_preprocess.py`中，可以将特征匹配的结果显示为图像。你可以根据这个图像调整特征和匹配比例，以获得最佳结果，从而提高算法的性能。

每个修改都可以通过更改代码中的相应部分来进行，这样你就可以根据你的需求调整程序的功能和性能。