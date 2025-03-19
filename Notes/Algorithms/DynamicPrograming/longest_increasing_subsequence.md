这段代码计算的是给定数组的最长递增子序列（LIS）的长度。它的时间复杂度是 $O(n^2)$，因为有两个嵌套的循环。为了简化时间复杂度，我们可以使用二分查找来优化内层循环，将时间复杂度降低到 $O(n \log n)$。

**优化思路**

1.  **维护一个辅助数组 `tails`：** `tails[i]` 存储长度为 `i+1` 的递增子序列的最小尾部元素。
2.  **遍历原数组 `array`：**
    * 如果当前元素 `x` 大于 `tails` 数组中的所有元素，则将其添加到 `tails` 数组的末尾，表示找到了一个更长的递增子序列。
    * 否则，使用二分查找在 `tails` 数组中找到第一个大于等于 `x` 的元素，并将其替换为 `x`。这样做可以保持 `tails` 数组的递增性，并确保每个长度的递增子序列的尾部元素尽可能小。

**Python 代码实现**

```python
import bisect

def longest_increasing_subsequence(array):
    """
    使用二分查找优化后的最长递增子序列

    参数:
    array: 输入数组

    返回:
    最长递增子序列的长度
    """

    tails = []  # 存储长度为 i+1 的递增子序列的最小尾部元素

    for x in array:
        i = bisect.bisect_left(tails, x)  # 二分查找第一个大于等于 x 的位置
        if i == len(tails):
            tails.append(x)  # x 大于 tails 中的所有元素，添加到末尾
        else:
            tails[i] = x  # 替换第一个大于等于 x 的元素

    return len(tails)

# 输入处理
n = int(input())
array = list(map(int, input().split()))

# 计算并输出结果
result = longest_increasing_subsequence(array)
print(result)
```

**代码解释**

1.  **导入 `bisect` 模块：** `bisect` 模块提供了二分查找的功能。
2.  **初始化 `tails` 数组：** 创建一个空数组 `tails`。
3.  **遍历 `array` 数组：**
    * `i = bisect.bisect_left(tails, x)`：使用 `bisect_left` 函数在 `tails` 数组中查找第一个大于等于 `x` 的位置 `i`。
    * `if i == len(tails)`：如果 `i` 等于 `tails` 数组的长度，说明 `x` 大于 `tails` 数组中的所有元素，将其添加到 `tails` 数组的末尾。
    * `else`：否则，将 `tails[i]` 替换为 `x`。
4.  **返回 `tails` 数组的长度：** `tails` 数组的长度即为最长递增子序列的长度。

**时间复杂度分析**

* 外层循环遍历 `array` 数组，时间复杂度为 $O(n)$。
* 内层使用 `bisect_left` 函数进行二分查找，时间复杂度为 $O(\log n)$。
* 因此，总的时间复杂度为 $O(n \log n)$。

**总结**

通过使用二分查找优化内层循环，我们将最长递增子序列问题的求解时间复杂度从 $O(n^2)$ 降低到了 $O(n \log n)$。
