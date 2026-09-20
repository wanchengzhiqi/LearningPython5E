import sys

print("sys.version   :", sys.version.replace("\n", " | "))
print("sys.executable:", sys.executable)
print()

# ---------- 原题 ----------
settings = {"locale": "en-US"}

def label(key, saved=settings):
    return f"{saved['locale']}:{key}"

settings["locale"] = "ja-JP"          # 修改字典（原地）
settings = {"locale": "fr-FR"}        # 重新绑定名字

print("A) 第一行:", label("menu.start"))           # 默认值 -> 旧字典
print("B) 第二行:", label("menu.start", settings))  # 显式实参覆盖默认（仅本次）
print("C) 第三行:", label("menu.quit"))            # 默认值仍指向旧字典
print()

# ---------- 旁证1：默认值对象直接观察 ----------
print("D) label.__defaults__        :", label.__defaults__)
print("   label.__defaults__[0]     :", label.__defaults__[0])
print("   defaults[0] is settings   :", label.__defaults__[0] is settings)   # False
print("   defaults[0]['locale']     :", label.__defaults__[0]["locale"])     # 'ja-JP'
print()

# ---------- 旁证2：第二次调用没有“改写”默认值 ----------
print("E) 显式传参之后 defaults[0]['locale'] :", label.__defaults__[0]["locale"])
print()

# ---------- 旁证3：调用时读“当前”配置的替代写法 ----------
def label_now(key, saved=None):
    saved = settings if saved is None else saved
    return f"{saved['locale']}:{key}"

print("F) label_now('menu.start')   :", label_now("menu.start"))   # 跟随当前 settings -> fr-FR
print()

# ---------- 旁证4：经典“可变默认值”共享状态 ----------
def label_log(key, log=[]):
    log.append(key)
    return log

print("G) label_log('a') ->", label_log("a"))
print("   label_log('b') ->", label_log("b"))   # 同一个默认列表被复用
