# 评测结果（供人工核查忠实度）

核查方法：把每条答案的关键论断，逐条到它引用的块里找依据，打勾/打叉。

## E01 [in_book] 什么是深度学习？
判定：行为✓ / 命中✓ 

**答案**：
深度学习是一种具有多级表示的表征学习方法。它通过简单的函数将每一级的表示变换为更高级的表示，因此深度学习模型可以看作由许多简单函数复合而成的函数；当这些复合函数足够多时，模型可以表达非常复杂的变换，并逐级表示越来越抽象的概念或模式。

引用资料：资料chunk_24

**检索候选**：
- [资料chunk_24] Dive-into-DL-Pytorch（特点）
- [资料chunk_492] Dive-into-DL-Pytorch（5.1.5 互相关运算和卷积运算）
- [资料chunk_556] Dive-into-DL-Pytorch（5.6.1.2 缺失要素二：硬件）
- [资料chunk_30] Dive-into-DL-Pytorch（练习）
- [资料chunk_5] Dive-into-DL-Pytorch（深度学习简介）

---

## E02 [in_book] 什么是过拟合？
判定：行为✓ / 命中✓ 

**答案**：
过拟合是指模型的训练误差远小于它在测试集上的误差的现象。资料还指出，模型复杂度过高时很容易出现过拟合；训练样本不足也与过拟合有关。

引用资料：资料chunk_293、资料chunk_273、资料chunk_291

**检索候选**：
- [资料chunk_293] Dive-into-DL-Pytorch（3.12 权重衰减）
- [资料chunk_273] Dive-into-DL-Pytorch（3.11.3.1 模型复杂度）
- [资料chunk_291] Dive-into-DL-Pytorch（3.11.4.5 训练样本不足（过拟合））
- [资料chunk_275] Dive-into-DL-Pytorch（3.11.4 多项式函数拟合实验）
- [资料chunk_398] Dive-into-DL-Pytorch（4.1.2 `Module`的子类）

---

## E03 [in_book] 什么是丢弃法？
判定：行为✓ / 命中✓ 

**答案**：
丢弃法（dropout）是深度学习模型中常用来应对过拟合的一种方法。资料中本节提到的丢弃法特指**倒置丢弃法（inverted dropout）**。丢弃概率是丢弃法的超参数；训练时隐藏层神经元会随机被清零，从而使输出层的计算无法过度依赖某些隐藏单元，起到正则化作用并应对过拟合；测试模型时为了得到更确定性的结果，一般不使用丢弃法。

引用资料：资料chunk_316、资料chunk_318、资料chunk_319

**检索候选**：
- [资料chunk_316] Dive-into-DL-Pytorch（3.13 丢弃法）
- [资料chunk_809] Dive-into-DL-Pytorch（本函数已保存在d2lzh_pytorch包中方便以后使用）
- [资料chunk_318] Dive-into-DL-Pytorch（3.13.1 方法）
- [资料chunk_319] Dive-into-DL-Pytorch（3.13.1 方法）
- [资料chunk_326] Dive-into-DL-Pytorch（3.13.2.2 定义模型）

---

## E04 [in_book] 卷积运算是什么？
判定：行为✓ / 命中✓ 

**答案**：
卷积运算与互相关运算类似：为了得到卷积运算的输出，需要将核数组左右翻转并上下翻转，再与输入数组做互相关运算。深度学习中，如无特别说明，提到的卷积运算均指互相关运算；并且卷积层无论使用互相关运算还是卷积运算，都不影响模型预测时的输出。二维卷积层的核心计算是二维互相关运算。

引用资料：资料chunk_491、资料chunk_492、资料chunk_495

**检索候选**：
- [资料chunk_492] Dive-into-DL-Pytorch（5.1.5 互相关运算和卷积运算）
- [资料chunk_491] Dive-into-DL-Pytorch（5.1.5 互相关运算和卷积运算）
- [资料chunk_550] Dive-into-DL-Pytorch（小结）
- [资料chunk_495] Dive-into-DL-Pytorch（小结）
- [资料chunk_616] Dive-into-DL-Pytorch（5.9.1 Inception 块）

---

## E05 [in_book] 什么是梯度下降？
判定：行为✓ / 命中✓ 

**答案**：
梯度下降是一种优化算法：在每次迭代中，它根据自变量当前位置，沿着当前位置的梯度更新自变量。由于目标函数有关自变量的梯度代表了目标函数在自变量当前位置下降最快的方向，因此梯度下降也叫作最陡下降（steepest descent）。资料还指出，沿着梯度反方向更新自变量可能降低目标函数值；但如果迭代方向仅取决于自变量当前位置，也可能带来一些问题。

引用资料：资料chunk_958、资料chunk_913

**检索候选**：
- [资料chunk_958] Dive-into-DL-Pytorch（7.4 动量法）
- [资料chunk_913] Dive-into-DL-Pytorch（7.2 梯度下降和随机梯度下降）
- [资料chunk_932] Dive-into-DL-Pytorch（7.2.4 随机梯度下降）
- [资料chunk_921] Dive-into-DL-Pytorch（7.2.3 多维梯度下降）
- [资料chunk_943] Dive-into-DL-Pytorch（7.3.2 从零开始实现）

---

## E06 [in_book] 什么是循环神经网络？
判定：行为✓ / 命中✗ 

**答案**：
循环神经网络是使用循环计算的网络。它的隐藏状态可以捕捉截至当前时间步的序列历史信息，并且模型参数数量不随时间步增加而增长。还可以基于字符级循环神经网络创建语言模型。

引用资料：资料chunk_726

**检索候选**：
- [资料chunk_726] Dive-into-DL-Pytorch（小结）
- [资料chunk_550] Dive-into-DL-Pytorch（小结）
- [资料chunk_477] Dive-into-DL-Pytorch（5.1 二维卷积层）
- [资料chunk_893] Dive-into-DL-Pytorch（小结）
- [资料chunk_888] Dive-into-DL-Pytorch（6.9 深度循环神经网络）

---

## E07 [in_book] 什么是权重衰减？
判定：行为✓ / 命中✓ 

**答案**：
权重衰减等价于 L2 范数正则化。正则化通过在模型损失函数中添加惩罚项，使学出的模型参数值较小，是应对过拟合的常用手段；权重衰减通常会使学到的权重参数的元素较接近 0，并且可以通过优化器中的 `weight_decay` 超参数来指定。

引用资料：资料chunk_294、资料chunk_315

**检索候选**：
- [资料chunk_294] Dive-into-DL-Pytorch（3.12.1 方法）
- [资料chunk_309] Dive-into-DL-Pytorch（3.12.3.5 使用权重衰减）
- [资料chunk_310] Dive-into-DL-Pytorch（3.12.4 简洁实现）
- [资料chunk_300] Dive-into-DL-Pytorch（3.12.2 高维线性回归实验）
- [资料chunk_315] Dive-into-DL-Pytorch（小结）

---

## E08 [out_book] 今天天气怎么样？
判定：行为✓ / 命中— 

**答案**：
很抱歉，我没有相关内容的资料，请你换一个问题试试吧。

**检索候选**：

---

## E09 [out_book] Python 和 Java 哪个更适合初学者？
判定：行为✓ / 命中— 

**答案**：
很抱歉，我没有相关内容的资料，请你换一个问题试试吧。

**检索候选**：

---

## E10 [out_book] 给我推荐一部最近上映的电影？
判定：行为✓ / 命中— 

**答案**：
很抱歉，我没有相关内容的资料，请你换一个问题试试吧。

**检索候选**：

---

## E11 [greeting] 你好
判定：行为✓ / 命中— 

**答案**：
你好，我是d2l知识库问答助手，有什么关于《Dive into Deep Learning（动手学深度学习）》的问题都可以问我哦。

**检索候选**：

---

## E12 [greeting] 你叫什么名字？
判定：行为✓ / 命中— 

**答案**：
你好，我是d2l知识库问答助手，有什么关于《Dive into Deep Learning（动手学深度学习）》的问题都可以问我哦。

**检索候选**：

---

## E13 [mixed] 你好，什么是过拟合？
判定：行为✓ / 命中✓ 

**答案**：
过拟合是指模型的训练误差远小于它在测试集上的误差。也就是说，模型在训练数据上表现很好，但在测试数据上表现较差。模型复杂度过高时很容易出现过拟合，训练样本不足时也会出现过拟合。

引用资料：资料chunk_293、资料chunk_273、资料chunk_291

**检索候选**：
- [资料chunk_275] Dive-into-DL-Pytorch（3.11.4 多项式函数拟合实验）
- [资料chunk_291] Dive-into-DL-Pytorch（3.11.4.5 训练样本不足（过拟合））
- [资料chunk_273] Dive-into-DL-Pytorch（3.11.3.1 模型复杂度）
- [资料chunk_293] Dive-into-DL-Pytorch（3.12 权重衰减）
- [资料chunk_809] Dive-into-DL-Pytorch（本函数已保存在d2lzh_pytorch包中方便以后使用）

---

## E15 [variant] 你好，什么是深度学习？
判定：行为✓ / 命中✓ 引用一致性:✓ 本方['chunk_24'] vs 对方['chunk_24']

**答案**：
深度学习是机器学习中一种具有多级表示的表征学习方法。它从原始数据开始，每一级通过简单函数将该级表示变换为更高级的表示，因此深度学习模型也可以看作由许多简单函数复合而成的函数；当这些复合函数足够多时，模型可以表达非常复杂的变换，并逐级表示越来越抽象的概念或模式。例如图像可逐级表示为边缘、花纹、特定部位的模式等，最终完成物体识别等任务。

引用资料：资料chunk_24

**检索候选**：
- [资料chunk_492] Dive-into-DL-Pytorch（5.1.5 互相关运算和卷积运算）
- [资料chunk_30] Dive-into-DL-Pytorch（练习）
- [资料chunk_24] Dive-into-DL-Pytorch（特点）
- [资料chunk_5] Dive-into-DL-Pytorch（深度学习简介）
- [资料chunk_25] Dive-into-DL-Pytorch（特点）

---

## E16 [in_book] 丢弃法的代码怎么写？
判定：行为✓ / 命中✓ 

**答案**：
资料中给出的丢弃法代码写法是在模型前向传播中，训练时使用丢弃法：

```python
if is_training:  # 只在训练模型时使用丢弃法
    H1 = dropout(H1, drop_prob1)  # 在第一层全连接后添加丢弃层
H2 = (torch.matmul(H1, W2) + b2).relu()
if is_training:
    H2 = dropout(H2, drop_prob2)  # 在第二层全连接后添加丢弃层
return torch.matmul(H2, W3) + b3
```

资料还指出，对模型评估的时候不应该进行丢弃。

引用资料：资料chunk_326

**检索候选**：
- [资料chunk_326] Dive-into-DL-Pytorch（3.13.2.2 定义模型）
- [资料chunk_329] Dive-into-DL-Pytorch（本函数已保存在d2lzh_pytorch）
- [资料chunk_1025] Dive-into-DL-Pytorch（8.1 命令式和符号式混合编程）
- [资料chunk_1389] Dive-into-DL-Pytorch（10.12.2.3 含注意力机制的解码器）
- [资料chunk_1357] Dive-into-DL-Pytorch（10.11.1.1 矢量化计算）

---

## E17 [in_book] 什么是线性回归？
判定：行为✓ / 命中✓ 

**答案**：
线性回归是一种输出连续值的模型，适用于回归问题，例如预测房屋价格、气温、销售额等连续值问题。资料以房屋价格预测为例说明线性回归的基本要素：假设房价只取决于房屋面积和房龄两个因素，并探索价格与这两个因素的关系。对于索引为 \(i\) 的房屋，其线性回归模型的价格预测表达式为  
\[
\hat{y}^{(i)} = x_1^{(i)} w_1 + x_2^{(i)} w_2 + b
\]
其中 \(x_1^{(i)}\)、\(x_2^{(i)}\) 是输入特征，\(w_1\)、\(w_2\) 是权重，\(b\) 是偏差。资料还指出，线性回归和 softmax 回归都是单层神经网络，它们涉及的概念和技术同样适用于大多数深度学习模型。

引用资料：资料chunk_89、资料chunk_90、资料chunk_94

**检索候选**：
- [资料chunk_103] Dive-into-DL-Pytorch（3.1.2 线性回归的表示方法）
- [资料chunk_89] Dive-into-DL-Pytorch（3.1 线性回归）
- [资料chunk_163] Dive-into-DL-Pytorch（3.4.2 softmax回归模型）
- [资料chunk_90] Dive-into-DL-Pytorch（3.1.1 线性回归的基本要素）
- [资料chunk_94] Dive-into-DL-Pytorch（(1) 训练数据）

---

## E18 [in_book] 什么是softmax回归？
判定：行为✓ / 命中✓ 

**答案**：
softmax回归是一种用于多类别分类的模型。它和线性回归一样，将输入特征与权重做线性叠加；但与线性回归的主要不同在于，softmax回归的输出值个数等于标签里的类别数，因此可用于多类别分类。它同样是一个单层神经网络。

在计算上，softmax运算会先对输出元素做指数运算，再对同一行元素求和，最后让该行每个元素除以该行元素之和，从而表达样本预测各个输出的概率。训练softmax回归的步骤与线性回归非常相似：获取并读取数据、定义模型和损失函数，并使用优化算法训练模型。

引用资料：资料chunk_163、资料chunk_199、资料chunk_216

**检索候选**：
- [资料chunk_163] Dive-into-DL-Pytorch（3.4.2 softmax回归模型）
- [资料chunk_195] Dive-into-DL-Pytorch（3.6 softmax回归的从零开始实现）
- [资料chunk_199] Dive-into-DL-Pytorch（3.6.3 实现softmax运算）
- [资料chunk_208] Dive-into-DL-Pytorch（3.6.7 训练模型）
- [资料chunk_216] Dive-into-DL-Pytorch（小结）

---

## E19 [in_book] 什么是多层感知机？
判定：行为✓ / 命中✓ 

**答案**：
多层感知机是含有至少一个隐藏层的、由全连接层组成的神经网络，且每个隐藏层的输出会通过激活函数进行变换。多层感知机的层数和各隐藏层中隐藏单元个数都是超参数。它通常在输出层与输入层之间加入一个或多个全连接隐藏层，常用激活函数包括ReLU函数、sigmoid函数和tanh函数。

引用资料：资料chunk_242、资料chunk_244

**检索候选**：
- [资料chunk_245] Dive-into-DL-Pytorch（3.9 多层感知机的从零开始实现）
- [资料chunk_262] Dive-into-DL-Pytorch（小结）
- [资料chunk_242] Dive-into-DL-Pytorch（3.8.3 多层感知机）
- [资料chunk_256] Dive-into-DL-Pytorch（3.10 多层感知机的简洁实现）
- [资料chunk_244] Dive-into-DL-Pytorch（小结）

---

## E20 [in_book] 什么是长短期记忆（LSTM）？
判定：行为✓ / 命中✓ 

**答案**：
长短期记忆（LSTM）是一种常用的门控循环神经网络，它比门控循环单元（GRU）的结构稍微复杂一点。LSTM 中引入了 3 个门，即输入门、遗忘门和输出门，以及与隐藏状态形状相同的记忆细胞，从而记录额外的信息。LSTM 还会计算候选记忆细胞，其计算使用值域在 \([-1, 1]\) 的 tanh 函数作为激活函数。

引用资料：资料chunk_858、资料chunk_859、资料chunk_864

**检索候选**：
- [资料chunk_864] Dive-into-DL-Pytorch（6.8.1.2 候选记忆细胞）
- [资料chunk_876] Dive-into-DL-Pytorch（6.8.4 定义模型）
- [资料chunk_869] Dive-into-DL-Pytorch（6.8.2 读取数据集）
- [资料chunk_858] Dive-into-DL-Pytorch（6.8 长短期记忆（LSTM））
- [资料chunk_859] Dive-into-DL-Pytorch（6.8.1 长短期记忆）

---

## E21 [in_book] 什么是注意力机制？
判定：行为✓ / 命中✓ 

**答案**：
注意力机制本质上能够为表征中较有价值的部分分配较多的计算资源。广义上，它的输入包括查询项以及一一对应的键项和值项，其中值项是需要加权平均的一组项，权重来自查询项与该值项对应的键项的计算。

以循环神经网络为例，注意力机制通过对编码器所有时间步的隐藏状态做加权平均来得到背景变量；解码器在每一时间步调整这些注意力权重，从而能够在不同时间步分别关注输入序列中的不同部分，并编码进相应时间步的背景变量。因此，可以在解码器的每个时间步使用不同的背景变量，并且注意力机制也可以采用更高效的矢量化计算。

引用资料：资料chunk_1365、资料chunk_1363、资料chunk_1349、资料chunk_1356

**检索候选**：
- [资料chunk_1365] Dive-into-DL-Pytorch（小结）
- [资料chunk_1363] Dive-into-DL-Pytorch（10.11.3 发展）
- [资料chunk_1349] Dive-into-DL-Pytorch（10.11 注意力机制）
- [资料chunk_1356] Dive-into-DL-Pytorch（10.11.1.1 矢量化计算）
- [资料chunk_1362] Dive-into-DL-Pytorch（10.11.2 更新隐藏状态）

---

## E22 [in_book] 什么是动量法？
判定：行为✓ / 命中✓ 

**答案**：
动量法是一种优化算法。它在小批量随机梯度下降的基础上引入速度变量：在时间步0将速度变量初始化为0，在时间步 \(t>0\) 按  
\[
\boldsymbol{v}_t \leftarrow \gamma \boldsymbol{v}_{t-1}+\eta_t \boldsymbol{g}_t,\quad
\boldsymbol{x}_t \leftarrow \boldsymbol{x}_{t-1}-\boldsymbol{v}_t
\]
更新，其中动量超参数 \(\gamma\) 满足 \(0\le \gamma<1\)。当 \(\gamma=0\) 时，动量法等价于小批量随机梯度下降。动量法使用了指数加权移动平均的思想，将过去时间步的梯度做加权平均，且权重按时间步指数衰减，并使相邻时间步的自变量更新在方向上更加一致。

引用资料：资料chunk_962、资料chunk_963、资料chunk_977

**检索候选**：
- [资料chunk_977] Dive-into-DL-Pytorch（小结）
- [资料chunk_963] Dive-into-DL-Pytorch（7.4.2 动量法）
- [资料chunk_1011] Dive-into-DL-Pytorch（7.8 Adam算法）
- [资料chunk_962] Dive-into-DL-Pytorch（7.4.2 动量法）
- [资料chunk_971] Dive-into-DL-Pytorch（7.4.3 从零开始实现）

---

## E23 [in_book] 什么是池化层？
判定：行为✓ / 命中✓ 

**答案**：
池化层是对输入数据的一个固定形状窗口（池化窗口）中的元素计算输出。它不同于卷积层计算输入和核的互相关性，而是直接计算池化窗口内元素的最大值或平均值，分别称为最大池化和平均池化。池化窗口会从输入数组最左上方开始，按从左往右、从上往下的顺序依次滑动。池化层的一个主要作用是缓解卷积层对位置的过度敏感性，并且可以指定填充和步幅；池化层的输出通道数跟输入通道数相同。

引用资料：资料chunk_521、资料chunk_531、资料chunk_526

**检索候选**：
- [资料chunk_550] Dive-into-DL-Pytorch（小结）
- [资料chunk_531] Dive-into-DL-Pytorch（小结）
- [资料chunk_521] Dive-into-DL-Pytorch（5.4.1 二维最大池化层和平均池化层）
- [资料chunk_526] Dive-into-DL-Pytorch（5.4.2 填充和步幅）
- [资料chunk_1064] Dive-into-DL-Pytorch（9.1.1.1 翻转和裁剪）

---

## E24 [out_book] 法国的首都是哪里？
判定：行为✓ / 命中— 

**答案**：
很抱歉，我没有相关内容的资料，请你换一个问题试试吧。

**检索候选**：

---

## E25 [out_book] 1+1等于几？
判定：行为✓ / 命中— 

**答案**：
很抱歉，我没有相关内容的资料，请你换一个问题试试吧。

**检索候选**：

---

## E26 [out_book] 今天有什么新闻？
判定：行为✓ / 命中— 

**答案**：
很抱歉，我没有相关内容的资料，请你换一个问题试试吧。

**检索候选**：

---

## E27 [greeting] 在吗
判定：行为✓ / 命中— 

**答案**：
你好，我是d2l知识库问答助手，有什么关于《Dive into Deep Learning（动手学深度学习）》的问题都可以问我哦。

**检索候选**：

---

## E28 [greeting] 早上好
判定：行为✓ / 命中— 

**答案**：
你好，我是d2l知识库问答助手，有什么关于《Dive into Deep Learning（动手学深度学习）》的问题都可以问我哦。

**检索候选**：

---

## E29 [mixed] 你好，什么是长短期记忆？
判定：行为✓ / 命中✓ 

**答案**：
长短期记忆的隐藏层输出包括隐藏状态和记忆细胞，并且只有隐藏状态会传递到输出层。它的输入门、遗忘门和输出门可以控制信息的流动；长短期记忆可以应对循环神经网络中的梯度衰减问题，并更好地捕捉时间序列中时间步距离较大的依赖关系。此外，候选记忆细胞的计算使用值域在 \([-1,1]\) 的 tanh 函数作为激活函数，隐藏状态则由输出门控制从记忆细胞到隐藏状态的信息流动。

引用资料：资料chunk_887、资料chunk_864、资料chunk_868

**检索候选**：
- [资料chunk_864] Dive-into-DL-Pytorch（6.8.1.2 候选记忆细胞）
- [资料chunk_869] Dive-into-DL-Pytorch（6.8.2 读取数据集）
- [资料chunk_876] Dive-into-DL-Pytorch（6.8.4 定义模型）
- [资料chunk_887] Dive-into-DL-Pytorch（小结）
- [资料chunk_868] Dive-into-DL-Pytorch（6.8.1.4 隐藏状态）

---

## E14 [mixed] 什么是深度学习？明天天气怎么样？
判定：行为✓ / 命中✓ 

**答案**：
深度学习是具有多级表示的表征学习方法：它通过简单的函数将每一级的表示变换为更高级的表示，因此深度学习模型也可以看作是由许多简单函数复合而成的函数；当这些复合函数足够多时，模型可以表达非常复杂的变换，并能逐级表示越来越抽象的概念或模式。

关于“明天天气怎么样”，很抱歉，我没有相关内容的资料，请你换一个问题试试吧。

引用资料：资料chunk_24

**检索候选**：
- [资料chunk_492] Dive-into-DL-Pytorch（5.1.5 互相关运算和卷积运算）
- [资料chunk_30] Dive-into-DL-Pytorch（练习）
- [资料chunk_435] Dive-into-DL-Pytorch（4.4 自定义层）
- [资料chunk_24] Dive-into-DL-Pytorch（特点）
- [资料chunk_556] Dive-into-DL-Pytorch（5.6.1.2 缺失要素二：硬件）

---

## E30 [mixed] 什么是线性回归？明天天气怎么样？
判定：行为✓ / 命中✓ 

**答案**：
线性回归是一种输出连续值的模型，适用于回归问题，例如预测房屋价格、气温、销售额等连续值问题。以房屋价格预测为例，可以假设价格只取决于房屋面积和房龄两个因素，其预测表达式可写为  
\(\hat{y}^{(i)} = x_1^{(i)} w_1 + x_2^{(i)} w_2 + b\)。

关于“明天天气怎么样”，很抱歉，我没有相关内容的资料，请你换一个问题试试吧。

引用资料：资料chunk_89、资料chunk_90、资料chunk_94

**检索候选**：
- [资料chunk_103] Dive-into-DL-Pytorch（3.1.2 线性回归的表示方法）
- [资料chunk_94] Dive-into-DL-Pytorch（(1) 训练数据）
- [资料chunk_90] Dive-into-DL-Pytorch（3.1.1 线性回归的基本要素）
- [资料chunk_161] Dive-into-DL-Pytorch（3.4 softmax回归）
- [资料chunk_89] Dive-into-DL-Pytorch（3.1 线性回归）

---
