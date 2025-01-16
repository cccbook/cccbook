import sympy as sp
from sympy.polys.polytools import LC, degree
from sympy.combinatorics import Permutation, PermutationGroup

# 定義多項式
x = sp.symbols('x')
polynomial = x**4 - 10*x**3 + 35*x**2 - 50*x + 24  # 四次多項式

# 計算多項式的根
roots = sp.solve(polynomial, x)
print("多項式的根:", roots)

# 構建對稱群（S4群），檢查根的對稱性
# 假設根的排列符合S4群的結構
root_list = [root.evalf() for root in roots]
root_list.sort()
print("排序後的根：", root_list)

# 假設這些根的對稱性符合S4群
# S4群的基本置換（例如對應4個元素的對稱群）
# 這裡我們手動構造對應的置換
perm1 = Permutation([0, 1, 2, 3])  # 原始的對稱
perm2 = Permutation([1, 0, 3, 2])  # 另一種對稱

# 構建S4群
group = PermutationGroup([perm1, perm2])
print("群的元素:", group.generators)

# 檢查加羅瓦群的結構，這裡假設S4群反映了加羅瓦群
if group.order() == 24:
    print("該多項式的加羅瓦群是S4群，具有可解性。")
else:
    print("該多項式的加羅瓦群具有更複雜的結構，可能不可解。")
