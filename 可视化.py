import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class VisualNaturalMergeSort:
    def __init__(self, arr):
        self.original = arr.copy()
        self.arr = arr.copy()
        self.history = []  # 记录每个步骤（数组状态，颜色）
        self.colors = ['lightgray'] * len(arr)
        self.positions = {id(val): i for i, val in enumerate(arr)}  # 解决重复值问题
        
    def record(self, highlights=None):
        """记录当前状态快照"""
        if highlights:
            colors = ['lightgray'] * len(self.arr)
            for idx, color in highlights.items():
                if 0 <= idx < len(colors):
                    colors[idx] = color
            self.colors = colors
        self.history.append((self.arr.copy(), self.colors.copy()))
        
    def build_trend_cache(self):
        """构建趋势缓存"""
        return [self.arr[i] <= self.arr[i+1] for i in range(len(self.arr)-1)] if len(self.arr) > 1 else []
    
    def optimized_split_strict(self):
        """严格趋势分割（带可视化）"""
        cache = self.build_trend_cache()
        runs = []
        i = 0
        n = len(self.arr)
        
        while i < n:
            start = i
            if i >= n-1:
                runs.append(self.arr[start:i+1])
                break
                
            # 标记扫描区域
            self._update_color(range(start, min(i+2, n)), 'lightblue')
            is_asc = cache[i]
            
            while i < n-1 and cache[i] == is_asc:
                i += 1
                self._update_color([i], 'lightblue')
                
            # 处理降序序列
            if not is_asc:
                self._update_color(range(start, i+1), 'salmon')
                runs.append(self.arr[start:i+1][::-1])
            else:
                runs.append(self.arr[start:i+1])
            
            # 重置颜色
            self._reset_colors()
            i += 1
            
        return runs
    
    def merge_sublists(self, sublists):
        """合并子系统"""
        while len(sublists) > 1:
            sublists = self.dynamic_merge_strategy(sublists)
        return sublists[0] if sublists else []
    
    def dynamic_merge_strategy(self, sublists):
        """动态合并策略（完整实现）"""
        new_sublists = []
        merged = False
        i = 0
        
        # 第一轮：直接连接合并
        while i < len(sublists):
            if i+1 < len(sublists) and sublists[i][-1] <= sublists[i+1][0]:
                # 标记合并区间
                self._highlight_sublist(sublists[i], '#a8d8ef')
                self._highlight_sublist(sublists[i+1], '#ffb347')
                
                # 执行合并
                merged_sub = self.preallocated_merge(sublists[i], sublists[i+1])
                new_sublists.append(merged_sub)
                
                # 显示合并结果
                self._highlight_sublist(merged_sub, '#77dd77')
                i += 2
                merged = True
            else:
                new_sublists.append(sublists[i])
                i += 1
        
        # 第二轮：普通合并
        if not merged:
            temp_sublists = []
            for i in range(0, len(sublists), 2):
                if i+1 < len(sublists):
                    self._highlight_sublist(sublists[i], '#a8d8ef')
                    self._highlight_sublist(sublists[i+1], '#ffb347')
                    merged_sub = self.preallocated_merge(sublists[i], sublists[i+1])
                    self._highlight_sublist(merged_sub, '#77dd77')
                    temp_sublists.append(merged_sub)
                else:
                    temp_sublists.append(sublists[i])
            new_sublists = temp_sublists
        
        # 更新数组状态
        self.arr = []
        for sub in new_sublists:
            self.arr.extend(sub)
        self._reset_colors()
        return new_sublists
    
    def preallocated_merge(self, a, b):
        """可视化合并过程"""
        merged = []
        i = j = 0
        
        while i < len(a) and j < len(b):
            # 高亮比较元素
            idx_a = self._find_index(a[i])
            idx_b = self._find_index(b[j])
            self._update_color([idx_a, idx_b], '#ff6961')
            
            if a[i] <= b[j]:
                merged.append(a[i])
                self._update_color([idx_a], '#77dd77')
                i += 1
            else:
                merged.append(b[j])
                self._update_color([idx_b], '#77dd77')
                j += 1
                
        # 处理剩余元素
        while i < len(a):
            idx = self._find_index(a[i])
            self._update_color([idx], '#77dd77')
            merged.append(a[i])
            i += 1
            
        while j < len(b):
            idx = self._find_index(b[j])
            self._update_color([idx], '#77dd77')
            merged.append(b[j])
            j += 1
            
        return merged
    
    def sort(self):
        """执行完整排序流程"""
        self.record()  # 初始状态
        runs = self.optimized_split_strict()
        self.merge_sublists(runs)
        self.record()  # 最终状态
        return self.arr
    
    # 辅助方法 --------------------------------------------------
    def _find_index(self, value):
        """安全查找元素索引"""
        for i in range(len(self.arr)):
            if self.arr[i] == value and self.colors[i] != '#77dd77':
                return i
        return self.arr.index(value)  # 备用方案
    
    def _highlight_sublist(self, sublist, color):
        """高亮显示子序列"""
        for val in sublist:
            idx = self._find_index(val)
            if idx is not None:
                self.colors[idx] = color
        self.record()
    
    def _update_color(self, indices, color):
        """更新指定位置颜色"""
        for idx in indices:
            if 0 <= idx < len(self.colors):
                self.colors[idx] = color
        self.record()
    
    def _reset_colors(self):
        """重置颜色状态"""
        self.colors = ['lightgray'] * len(self.arr)
        self.record()

def visualize_sorting(arr):
    """可视化主函数"""
    # 初始化排序器
    sorter = VisualNaturalMergeSort(arr)
    sorted_arr = sorter.sort()
    
    # 创建可视化窗口
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_title("Natural Merge Sort Visualization")
    ax.set_xticks([])
    ax.set_yticks([])
    
    # 创建图例
    legend_elements = [
        plt.Rectangle((0,0),1,1,fc='lightgray', label='未处理'),
        plt.Rectangle((0,0),1,1,fc='lightblue', label='扫描中'),
        plt.Rectangle((0,0),1,1,fc='salmon', label='反转操作'),
        plt.Rectangle((0,0),1,1,fc='#a8d8ef', label='合并序列1'),
        plt.Rectangle((0,0),1,1,fc='#ffb347', label='合并序列2'),
        plt.Rectangle((0,0),1,1,fc='#ff6961', label='元素比较'),
        plt.Rectangle((0,0),1,1,fc='#77dd77', label='已排序')
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    # 初始化条形图
    bars = ax.bar(range(len(arr)), sorter.history[0][0], 
                 color=sorter.history[0][1], edgecolor='black')
    
    # 动画更新函数
    def animate(frame):
        arr_state, colors = sorter.history[frame]
        for bar, height, color in zip(bars, arr_state, colors):
            bar.set_height(height)
            bar.set_color(color)
        return bars
    
    # 创建动画
    ani = FuncAnimation(fig, animate, frames=len(sorter.history),
                       interval=200, blit=False, repeat=False)
    
    plt.show()
    return ani

if __name__ == "__main__":
    # 配置参数
    ARRAY_LENGTH = 30   # 数组长度
    ANIMATION_INTERVAL = 200  # 动画帧间隔（毫秒）
    
    # 生成测试数据（确保唯一性）
    arr = random.sample(range(1, 100), ARRAY_LENGTH)
    arr = [x + random.random() for x in arr]  # 添加小数部分确保唯一
    
    # 执行可视化排序
    visualize_sorting(arr)