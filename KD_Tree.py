# -*- coding: utf-8 -*-
"""
静态KD树
@author:    Allen Oris
"""
import copy
import queue


def sqr(x):
    return x * x


class Node:
    def __init__(self, axes=None):
        self.x = copy.deepcopy(axes)

    def axes_in(self, axes):
        if self.x:
            self.x.clear()
        self.x = copy.deepcopy(axes)


class DAN:
    def __init__(self, dis=0.0, num=0):
        """记录距离，与点下标"""
        self.dis = dis
        self.num = num

    def __cmp__(self, other):
        return -1 if self.dis > other.dis else 1 if self.dis < other.dis else 0

    def __lt__(self, other):
        return self.dis > other.dis


class KDTree:
    def __init__(self, nodes=None):
        """传入向量矩阵即可"""
        self.N = len(nodes)  # 静态点数
        self.node = [Node(nod) for nod in nodes]
        self.K = self.tree_dimension()
        self.sz = [0 for i in range(self.N << 2)]  # size数组
        self.p = self.open_array()
        self.idx = 0
        self.q_sz = 0
        self.que = queue.PriorityQueue()
        self.target = Node()
        self.build_kd(1, 0, self.N - 1, 0)
        pass

    def build_kd(self, i, l, r, dep):
        """构建kd树，传入树下标(初始为1)，左端点(0)，右端点(N-1)，深度(0)"""
        if l > r:
            return  # 树底结束
        mid = (l + r) >> 1
        lc = i << 1
        rc = i << 1 | 1
        idx = dep % self.K  # 该层维度
        self.sz[i] = r - l
        self.sz[lc] = self.sz[rc] = -1
        # nth_element(node + l, node + mid, node + r + 1) pyhton没有nth_element需要自己写，会比直接sort快，留坑
        self.sort_node(l, r + 1, idx)
        self.p[i] = self.node[mid]
        self.build_kd(lc, l, mid - 1, dep + 1)
        self.build_kd(rc, mid + 1, r, dep + 1)

    def query_kd(self, m, a):
        """查询最邻近的m个点",m:查询个数，a:查询向量，结果返回一个向量列表"""
        if len(a) != self.K:
            raise RuntimeError("相似度传入维数错误")
        self.que_clear()
        self.target.axes_in(a)
        self.query(1, m, 0)
        res = []
        while not self.que.empty():
            res.append(self.que.get())
        ans = []
        for nod in reversed(res):
            ans.append(self.p[nod.num].x)
        return ans

    def query(self, i, m, dep):
        if self.sz[i] == -1:
            return
        tmp = DAN(0, i)
        lc, rc, idx, flag = i << 1, i << 1 | 1, dep % self.K, False
        for j, xj in enumerate(self.target.x):
            tmp.dis += sqr(xj - self.p[i].x[j])
        if self.target.x[idx] >= self.p[i].x[idx]:
            lc, rc = rc, lc
        self.query(lc, m, dep + 1)
        if self.q_sz < m:
            self.que.put(tmp)
            flag = True
            self.q_sz += 1
        else:
            backup = self.que.get()
            if tmp.dis < backup.dis:
                self.que.put(tmp)
                backup = tmp
            else:
                self.que.put(backup)
            if sqr(self.target.x[idx] - self.p[i].x[idx]) < backup.dis:
                flag = True
        self.query(rc, m, dep + 1)

    def tree_dimension(self):
        if len(self.node) == 0:
            return 0
        k = len(self.node[0].x)
        for nod in self.node:
            if len(nod.x) != k:
                raise RuntimeError("维度失衡!")
        return k

    def open_array(self):
        arr = []
        for i in range(self.N << 2):
            arr.append(Node())
            arr[i].x = [0 for i in range(self.K)]
        return arr

    def sort_node(self, l, r, idx):
        tmp = []
        for i in range(l, r):
            tmp.append(self.node[i])
        sorted(tmp, key=lambda x: x.x[idx], reverse=False)
        j = 0
        for i in range(l, r):
            self.node[i] = tmp[j]
            j += 1

    def que_clear(self):
        while not self.que.empty():
            self.que.get()
        self.q_sz = 0


def solve():
    n = int(input())
    a = [[0, 0] for i in range(n)]
    for i in range(n):
        a[i] = list(map(int, input().split()))
    kdt = KDTree(a)
    for nod in a:
        res = kdt.query_kd(2, nod)
        ans = 0
        for j in range(2):
            ans += sqr(nod[j] - res[1][j])
        print(ans)


if __name__ == '__main__':
    """测试HDU2966,静态KD树模板题"""
    T = int(input())
    for i in range(0, T):
        solve()
