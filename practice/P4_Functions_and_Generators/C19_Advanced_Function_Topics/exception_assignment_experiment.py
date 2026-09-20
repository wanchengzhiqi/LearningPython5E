import sys

print("sys.version   :", sys.version.replace("\n", " | "))
print("sys.executable:", sys.executable)
print()

# ---------- 原题 ----------
def strip_text(text):
    return text.strip()

def normalize_case(text):
    return text.casefold()

def run_pipeline(text, rules, *, on_success, events):
    current = text
    for rule in rules:
        events.append(f"before:{rule.__name__}")
        current = rule(current)
        events.append(f"after:{rule.__name__}")
    on_success(current)
    return current

notices = []

def fail_notice(value):
    notices.append(value)
    raise RuntimeError("notice failed")

events = []
result = "old"

try:
    result = run_pipeline(
        " Menu.Start ",
        (strip_text, normalize_case),
        on_success=fail_notice,
        events=events,
    )
except RuntimeError:
    pass

print("A) result  =", repr(result))
print("B) notices =", notices)
print("C) events  =", events)
print()

# ---------- 旁证1：赋值只发生在 RHS 完整求值之后 ----------
def boom():
    raise RuntimeError("boom")

y = "keep"
try:
    y = boom()
except RuntimeError:
    pass
print("D) y =", repr(y))          # 保持旧值 'keep'

# ---------- 旁证2：若原本没有旧绑定，名字根本不存在 ----------
try:
    z = boom()
except RuntimeError:
    pass
try:
    print("E) z =", z)
except NameError as e:
    print("E) z 未绑定 ->", type(e).__name__)

# ---------- 旁证3：on_success 不抛时，同一管线正常赋值 ----------
events2 = []
result2 = "old"

def ok_notice(value):
    notices.append("ok:" + value)

try:
    result2 = run_pipeline(" Menu.Start ", (strip_text, normalize_case),
                           on_success=ok_notice, events=events2)
except RuntimeError:
    pass
print("F) result2 =", repr(result2))   # 'menu.start'
print()

# ---------- 旁证4：工程修复——把易失败的“通知”与返回值解耦 ----------
notices4 = []

def fail_notice4(value):
    notices4.append(value)
    raise RuntimeError("notice failed")

def run_pipeline_safe(text, rules, *, on_success, events):
    current = text
    for rule in rules:
        events.append(f"before:{rule.__name__}")
        current = rule(current)
        events.append(f"after:{rule.__name__}")
    try:
        on_success(current)
    except RuntimeError as e:
        events.append(f"notify-failed:{e}")
    return current

events3 = []
result3 = run_pipeline_safe(" Menu.Start ", (strip_text, normalize_case),
                            on_success=fail_notice4, events=events3)
print("G) result3 =", repr(result3), "| notices4 =", notices4)
print("   events3 =", events3)
print()

# ---------- 旁证5：casefold 比 lower 更强（本地化边界） ----------
print("H) 'ß'.lower()    :", repr("ß".lower()))
print("   'ß'.casefold() :", repr("ß".casefold()))
print("   'İ'.casefold() :", repr("İ".casefold()))
print()
print("   notices 最终 =", notices)
