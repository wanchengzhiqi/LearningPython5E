#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tkinter GUI for the local prompt template database."""

from __future__ import annotations

import argparse
import sqlite3
import sys
import tkinter as tk
from tkinter import messagebox, ttk

from import_test_demo import import_prompt_source
from prompt_store import (
    add_record,
    display_state,
    get_record,
    get_record_readonly,
    hard_delete_record,
    initialize_database,
    list_records,
    lock_record,
    resolve_db_path,
    restore_record,
    soft_delete_record,
    unlock_record,
    update_record,
    validate_database_integrity,
)


class PromptManagerApp:
    def __init__(self, root: tk.Tk, db_path: str | None = None) -> None:
        self.root = root
        self.db_path = db_path
        self.current_record_id: int | None = None
        self.current_record: dict | None = None
        self.show_deleted = tk.BooleanVar(value=False)
        self.status_text = tk.StringVar()
        self.action_buttons: dict[str, ttk.Button] = {}
        self.form_baseline: dict[str, str] = self.empty_form_snapshot()
        self._restoring_selection = False

        try:
            initialize_database(self.db_path)
        except Exception as exc:  # noqa: BLE001 - GUI startup must surface DB errors.
            raise RuntimeError(f"database initialization failed: {exc}") from exc
        self.root.title("Prompt Template Manager")
        self.root.geometry("1220x760")
        self.root.minsize(980, 620)
        self._build_layout()
        self.root.protocol("WM_DELETE_WINDOW", self.request_close)
        if not self.refresh_records(preserve_selection=False):
            return
        self.set_status(f"数据库：{resolve_db_path(self.db_path)}")

    def _build_layout(self) -> None:
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(0, weight=1)

        left = ttk.Frame(self.root, padding=8)
        left.grid(row=0, column=0, sticky="nsew")
        left.rowconfigure(2, weight=1)
        left.columnconfigure(0, weight=1)

        search_bar = ttk.Frame(left)
        search_bar.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        search_bar.columnconfigure(0, weight=1)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_bar, textvariable=self.search_var)
        search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        search_entry.bind("<Return>", lambda _event: self.refresh_records(confirm_discard=True))
        ttk.Button(
            search_bar,
            text="搜索",
            command=lambda: self.refresh_records(confirm_discard=True),
        ).grid(row=0, column=1)

        options = ttk.Frame(left)
        options.grid(row=1, column=0, sticky="ew", pady=(0, 6))
        ttk.Checkbutton(
            options,
            text="显示已删除",
            variable=self.show_deleted,
            command=self.on_show_deleted_toggle,
        ).pack(side="left")

        columns = ("id", "state", "category", "title", "updated_at")
        tree_frame = ttk.Frame(left)
        tree_frame.grid(row=2, column=0, sticky="nsew")
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
        for column, label, width in [
            ("id", "ID", 48),
            ("state", "状态", 78),
            ("category", "分类", 190),
            ("title", "标题", 380),
            ("updated_at", "更新时间", 180),
        ]:
            self.tree.heading(column, text=label)
            self.tree.column(column, width=width, anchor="w")
        self.tree.tag_configure("deleted", foreground="#888888")
        self.tree.tag_configure("locked", foreground="#9a6500")
        self.tree.grid(row=0, column=0, sticky="nsew")
        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        tree_scroll.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=tree_scroll.set)
        self.tree.bind("<<TreeviewSelect>>", self.on_select_record)

        left_buttons = ttk.Frame(left)
        left_buttons.grid(row=3, column=0, sticky="ew", pady=(8, 0))
        for column in range(3):
            left_buttons.columnconfigure(column, weight=1)
        ttk.Button(
            left_buttons,
            text="初始化数据库",
            command=self.initialize_current_database,
        ).grid(row=0, column=0, sticky="ew", padx=(0, 4))
        ttk.Button(
            left_buttons,
            text="刷新",
            command=lambda: self.refresh_records(confirm_discard=True),
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=4,
        )
        ttk.Button(
            left_buttons,
            text="导入内置样例",
            command=self.import_from_builtin_sample,
        ).grid(row=0, column=2, sticky="ew", padx=(4, 0))

        right = ttk.Frame(self.root, padding=8)
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(1, weight=1)
        right.rowconfigure(3, weight=1)

        self.title_text = self.add_text_field(right, row=0, label="标题", height=2)
        self.category_text = self.add_text_field(right, row=1, label="分类", height=2)
        self.tags_text = self.add_text_field(right, row=2, label="标签", height=2)

        ttk.Label(right, text="内容").grid(row=3, column=0, sticky="nw")
        content_frame = ttk.Frame(right)
        content_frame.grid(row=3, column=1, sticky="nsew")
        content_frame.rowconfigure(0, weight=1)
        content_frame.columnconfigure(0, weight=1)
        self.content_text = tk.Text(content_frame, wrap="word", undo=True)
        self.content_text.grid(row=0, column=0, sticky="nsew")
        content_scroll = ttk.Scrollbar(content_frame, orient="vertical", command=self.content_text.yview)
        content_scroll.grid(row=0, column=1, sticky="ns")
        self.content_text.configure(yscrollcommand=content_scroll.set)

        buttons = ttk.Frame(right)
        buttons.grid(row=4, column=1, sticky="ew", pady=(8, 0))
        for column in range(4):
            buttons.columnconfigure(column, weight=1)
        self.add_action_button(buttons, "add", "新增", self.add_current_form, 0, 0)
        self.add_action_button(buttons, "save", "保存修改", self.save_current_record, 0, 1)
        self.add_action_button(buttons, "soft_delete", "软删除", self.delete_current_record, 0, 2)
        self.add_action_button(buttons, "restore", "恢复", self.restore_current_record, 0, 3)
        self.add_action_button(buttons, "lock", "锁定", self.lock_current_record, 1, 0)
        self.add_action_button(buttons, "unlock", "解锁", self.unlock_current_record, 1, 1)
        self.add_action_button(buttons, "hard_delete", "真删除", self.hard_delete_current_record, 1, 2)
        self.add_action_button(buttons, "clear", "清空表单", self.clear_form, 1, 3)
        self.add_action_button(buttons, "safe_exit", "安全退出", self.safe_exit, 2, 3)

        status = ttk.Label(self.root, textvariable=self.status_text, anchor="w", padding=6)
        status.grid(row=1, column=0, columnspan=2, sticky="ew")

        self.update_action_states()

    def add_text_field(self, parent: ttk.Frame, *, row: int, label: str, height: int) -> tk.Text:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="nw", pady=(0, 6))
        widget = tk.Text(parent, height=height, wrap="word", undo=True)
        widget.grid(row=row, column=1, sticky="ew", pady=(0, 6))
        return widget

    def add_action_button(
        self,
        parent: ttk.Frame,
        key: str,
        text: str,
        command,
        row: int,
        column: int,
    ) -> None:
        button = ttk.Button(parent, text=text, command=command)
        button.grid(row=row, column=column, sticky="ew", padx=4, pady=3)
        self.action_buttons[key] = button

    def set_status(self, message: str) -> None:
        self.status_text.set(message)

    def empty_form_snapshot(self) -> dict[str, str]:
        return {"title": "", "category": "", "tags": "", "content": ""}

    def snapshot_from_record(self, record: dict) -> dict[str, str]:
        return {
            "title": str(record["title"]).strip(),
            "category": str(record["category"]).strip(),
            "tags": ", ".join(record["tags"]).strip(),
            "content": str(record["content"]).strip(),
        }

    def remember_form_baseline(self) -> None:
        self.form_baseline = self.get_form_values()

    def has_unsaved_changes(self) -> bool:
        return self.get_form_values() != self.form_baseline

    def confirm_discard_unsaved_changes(self, action: str) -> bool:
        if not self.has_unsaved_changes():
            return True
        return messagebox.askyesno(
            "存在未保存内容",
            f"当前表单存在未保存内容，{action}会丢失这些修改。\n\n确定继续吗？",
        )

    def initialize_current_database(self) -> None:
        if not self.confirm_discard_unsaved_changes("初始化数据库并刷新列表"):
            self.set_status("已取消初始化，未保存内容仍保留在表单中。")
            return
        try:
            path = initialize_database(self.db_path)
        except Exception as exc:  # noqa: BLE001 - GUI should show database errors.
            messagebox.showerror("数据库初始化失败", str(exc))
            self.set_status(f"数据库初始化失败：{exc}")
            return
        if not self.refresh_records():
            return
        self.set_status(f"数据库已初始化：{path}")
        messagebox.showinfo("初始化完成", f"数据库已初始化：\n{path}")

    def get_text(self, widget: tk.Text, *, compact: bool = False) -> str:
        value = widget.get("1.0", "end").strip()
        if compact:
            return " ".join(value.splitlines()).strip()
        return value

    def set_text(self, widget: tk.Text, value: str) -> None:
        old_state = str(widget.cget("state"))
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", value)
        widget.configure(state=old_state)

    def set_form_editable(self, editable: bool) -> None:
        state = "normal" if editable else "disabled"
        for widget in [self.title_text, self.category_text, self.tags_text, self.content_text]:
            widget.configure(state=state)

    def get_form_values(self) -> dict[str, str]:
        return {
            "title": self.get_text(self.title_text, compact=True),
            "category": self.get_text(self.category_text, compact=True),
            "tags": self.get_text(self.tags_text, compact=True),
            "content": self.get_text(self.content_text),
        }

    def clear_form(
        self,
        *,
        update_status: bool = True,
        confirm_discard: bool = True,
    ) -> bool:
        if confirm_discard and not self.confirm_discard_unsaved_changes("清空表单"):
            self.set_status("已取消清空，未保存内容仍保留在表单中。")
            return False
        self.current_record_id = None
        self.current_record = None
        self.set_form_editable(True)
        for widget in [self.title_text, self.category_text, self.tags_text, self.content_text]:
            self.set_text(widget, "")
        self.form_baseline = self.empty_form_snapshot()
        self.tree.selection_remove(self.tree.selection())
        self.update_action_states()
        if update_status:
            self.set_status("表单已清空，可填写后点击“保存新增”。")
        return True

    def refresh_records(
        self,
        *,
        select_id: int | None = None,
        preserve_selection: bool = True,
        confirm_discard: bool = False,
    ) -> bool:
        if confirm_discard and not self.confirm_discard_unsaved_changes("刷新列表"):
            self.set_status("已取消刷新，未保存内容仍保留在表单中。")
            return False
        previous_id = self.current_record_id if preserve_selection else None
        target_id = select_id if select_id is not None else previous_id
        try:
            records = list_records(
                db_path=self.db_path,
                search=self.search_var.get().strip() or None,
                include_deleted=self.show_deleted.get(),
            )
        except Exception as exc:  # noqa: BLE001 - GUI should keep running on DB errors.
            messagebox.showerror("刷新失败", str(exc))
            self.set_status(f"刷新失败：{exc}")
            return False
        for item in self.tree.get_children():
            self.tree.delete(item)
        visible_ids: set[int] = set()
        for record in records:
            state = display_state(record)
            visible_ids.add(int(record["id"]))
            self.tree.insert(
                "",
                "end",
                iid=str(record["id"]),
                values=(
                    record["id"],
                    state,
                    record["category"],
                    record["title"],
                    record["updated_at"],
                ),
                tags=(state,),
            )
        if target_id is not None and target_id in visible_ids:
            self.tree.selection_set(str(target_id))
            self.tree.focus(str(target_id))
            self.load_record(target_id)
        elif target_id is not None:
            self.clear_form(update_status=False, confirm_discard=False)
        else:
            self.update_action_states()
        self.set_status(f"已按 ID 升序加载 {len(records)} 条记录。")
        return True

    def on_show_deleted_toggle(self) -> None:
        new_value = self.show_deleted.get()
        if not self.refresh_records(confirm_discard=True):
            self.show_deleted.set(not new_value)

    def on_select_record(self, _event: tk.Event) -> None:
        if self._restoring_selection:
            return
        selection = self.tree.selection()
        if not selection:
            return
        selected_id = int(selection[0])
        if selected_id == self.current_record_id:
            return
        if not self.confirm_discard_unsaved_changes("切换记录"):
            self._restoring_selection = True
            try:
                self.tree.selection_remove(selection)
                if (
                    self.current_record_id is not None
                    and self.tree.exists(str(self.current_record_id))
                ):
                    self.tree.selection_set(str(self.current_record_id))
                    self.tree.focus(str(self.current_record_id))
            finally:
                self._restoring_selection = False
            self.set_status("已取消切换记录，未保存内容仍保留在表单中。")
            return
        self.load_record(selected_id)

    def load_record(self, record_id: int) -> None:
        record = get_record(record_id, self.db_path)
        if record is None:
            messagebox.showerror("读取失败", f"找不到记录：{record_id}")
            self.clear_form(confirm_discard=False)
            return
        self.current_record_id = record_id
        self.current_record = record
        self.set_form_editable(True)
        self.set_text(self.title_text, record["title"])
        self.set_text(self.category_text, record["category"])
        self.set_text(self.tags_text, ", ".join(record["tags"]))
        self.set_text(self.content_text, record["content"])
        self.remember_form_baseline()
        state = display_state(record)
        self.set_form_editable(state == "active")
        self.update_action_states()
        self.set_status(f"正在查看记录 {record_id}，状态：{state}。")

    def update_action_states(self) -> None:
        state = display_state(self.current_record) if self.current_record else None
        is_active = state == "active"
        is_locked = state == "locked"
        is_deleted = state == "deleted"

        self.action_buttons["add"].configure(
            state="normal",
            text="新增" if self.current_record_id is not None else "保存新增",
        )
        self.action_buttons["save"].configure(state="normal" if is_active else "disabled")
        self.action_buttons["soft_delete"].configure(state="normal" if is_active else "disabled")
        self.action_buttons["restore"].configure(state="normal" if is_deleted else "disabled")
        self.action_buttons["hard_delete"].configure(state="normal" if is_deleted else "disabled")
        self.action_buttons["lock"].configure(state="normal" if is_active else "disabled")
        self.action_buttons["unlock"].configure(state="normal" if is_locked else "disabled")
        self.action_buttons["clear"].configure(state="normal")
        self.action_buttons["safe_exit"].configure(state="normal")

    def add_current_form(self) -> None:
        if self.current_record_id is not None:
            if not self.clear_form(update_status=False, confirm_discard=True):
                return
            self.set_status("已进入新增模式；填写内容后点击“保存新增”。")
            return
        values = self.get_form_values()
        try:
            record = add_record(
                db_path=self.db_path,
                title=values["title"],
                category=values["category"],
                content=values["content"],
                tags=values["tags"],
            )
        except Exception as exc:  # noqa: BLE001 - GUI should show validation errors.
            messagebox.showerror("新增失败", str(exc))
            self.set_status("新增失败，数据库未改变。")
            return
        self.refresh_records(select_id=record["id"])
        self.set_status(f"新增成功：记录 {record['id']}。")
        messagebox.showinfo("新增成功", f"已新增记录 {record['id']}。")

    def save_current_record(self) -> None:
        if self.current_record_id is None or not self.current_record:
            messagebox.showwarning("没有选中记录", "请先选择一条 active 记录，再保存修改。")
            return
        if display_state(self.current_record) != "active":
            messagebox.showwarning("操作无效", "只有未锁定的 active 记录可以保存修改。")
            return
        if not messagebox.askyesno("确认修改", f"确定要修改记录 {self.current_record_id} 吗？"):
            self.set_status("已取消修改。")
            return
        values = self.get_form_values()
        try:
            record = update_record(
                self.current_record_id,
                db_path=self.db_path,
                title=values["title"],
                category=values["category"],
                content=values["content"],
                tags=values["tags"],
            )
        except Exception as exc:  # noqa: BLE001 - GUI should show validation errors.
            messagebox.showerror("保存失败", str(exc))
            self.set_status("保存失败，数据库未改变。")
            return
        self.refresh_records(select_id=record["id"])
        self.set_status(f"修改成功：记录 {record['id']} 已保存，展示位置保持 ID 升序。")
        messagebox.showinfo("修改成功", f"记录 {record['id']} 已保存。")

    def delete_current_record(self) -> None:
        if self.current_record_id is None or not self.current_record:
            messagebox.showwarning("没有选中记录", "请先选择一条未锁定的 active 记录。")
            return
        if display_state(self.current_record) != "active":
            messagebox.showwarning("操作无效", "只有未锁定的 active 记录可以软删除。")
            return
        if not messagebox.askyesno("确认软删除", f"确定要软删除记录 {self.current_record_id} 吗？"):
            self.set_status("已取消软删除。")
            return
        try:
            soft_delete_record(self.current_record_id, self.db_path)
        except Exception as exc:  # noqa: BLE001 - GUI should show validation errors.
            messagebox.showerror("软删除失败", str(exc))
            return
        if not self.refresh_records(preserve_selection=False):
            return
        self.clear_form(update_status=False, confirm_discard=False)
        self.set_status("软删除成功：记录已标记为 deleted。")
        messagebox.showinfo("软删除成功", "记录已标记为 deleted，可勾选显示已删除后恢复或真删除。")

    def restore_current_record(self) -> None:
        if self.current_record_id is None or not self.current_record:
            messagebox.showwarning("没有选中记录", "请先选择一条 deleted 记录。")
            return
        if display_state(self.current_record) != "deleted":
            messagebox.showwarning("操作无效", "只有 deleted 记录可以恢复。")
            return
        try:
            record = restore_record(self.current_record_id, self.db_path)
        except Exception as exc:  # noqa: BLE001 - GUI should show validation errors.
            messagebox.showerror("恢复失败", str(exc))
            return
        self.refresh_records(select_id=record["id"])
        self.set_status(f"恢复成功：记录 {record['id']}，展示位置保持 ID 升序。")
        messagebox.showinfo("恢复成功", f"记录 {record['id']} 已恢复为 active。")

    def hard_delete_current_record(self) -> None:
        if self.current_record_id is None or not self.current_record:
            messagebox.showwarning("没有选中记录", "请先选择一条 deleted 记录。")
            return
        if display_state(self.current_record) != "deleted":
            messagebox.showwarning("操作无效", "只有 deleted 记录可以真删除。")
            return
        record_id = self.current_record_id
        if not messagebox.askyesno(
            "确认真删除",
            f"确定要永久删除记录 {record_id} 吗？此操作不可恢复。",
        ):
            self.set_status("已取消真删除。")
            return
        try:
            hard_delete_record(record_id, self.db_path)
        except Exception as exc:  # noqa: BLE001 - GUI should show validation errors.
            messagebox.showerror("真删除失败", str(exc))
            return
        if not self.refresh_records(preserve_selection=False):
            return
        self.clear_form(update_status=False, confirm_discard=False)
        self.set_status(f"真删除成功：记录 {record_id} 已永久删除。")
        messagebox.showinfo("真删除成功", f"记录 {record_id} 已永久删除。")

    def lock_current_record(self) -> None:
        if self.current_record_id is None or not self.current_record:
            messagebox.showwarning("没有选中记录", "请先选择一条未锁定的 active 记录。")
            return
        if display_state(self.current_record) != "active":
            messagebox.showwarning("操作无效", "只有未锁定的 active 记录可以锁定。")
            return
        try:
            record = lock_record(self.current_record_id, self.db_path)
        except Exception as exc:  # noqa: BLE001 - GUI should show validation errors.
            messagebox.showerror("锁定失败", str(exc))
            return
        self.refresh_records(select_id=record["id"])
        self.set_status(f"锁定成功：记录 {record['id']} 已锁定。")
        messagebox.showinfo("锁定成功", f"记录 {record['id']} 已锁定。")

    def unlock_current_record(self) -> None:
        if self.current_record_id is None or not self.current_record:
            messagebox.showwarning("没有选中记录", "请先选择一条 locked 记录。")
            return
        if display_state(self.current_record) != "locked":
            messagebox.showwarning("操作无效", "只有 locked 记录可以解锁。")
            return
        try:
            record = unlock_record(self.current_record_id, self.db_path)
        except Exception as exc:  # noqa: BLE001 - GUI should show validation errors.
            messagebox.showerror("解锁失败", str(exc))
            return
        self.refresh_records(select_id=record["id"])
        self.set_status(f"解锁成功：记录 {record['id']} 已恢复为 active。")
        messagebox.showinfo("解锁成功", f"记录 {record['id']} 已解锁。")

    def safe_exit(self) -> None:
        self.request_close(run_health_check=True)

    def request_close(self, run_health_check: bool = False) -> None:
        if not self.confirm_discard_unsaved_changes("退出程序"):
            self.set_status("已取消退出，未保存内容仍保留在表单中。")
            return
        if run_health_check and not self.confirm_exit_health_check():
            return
        self.root.destroy()

    def confirm_exit_health_check(self) -> bool:
        issues = self.collect_exit_health_issues()
        if not issues:
            self.set_status("安全退出检查通过，正在退出。")
            return True

        shown_issues = "\n".join(f"- {issue}" for issue in issues[:8])
        if len(issues) > 8:
            shown_issues += f"\n- ... 另有 {len(issues) - 8} 项"
        should_exit = messagebox.askyesno(
            "安全退出检查发现问题",
            "退出前的只读检查发现以下问题：\n\n"
            f"{shown_issues}\n\n"
            "这些问题未被自动修复。是否仍要退出？",
        )
        if not should_exit:
            self.set_status("安全退出检查发现问题，已取消退出。")
            return False
        self.set_status("安全退出检查发现问题，用户确认后退出。")
        return True

    def collect_exit_health_issues(self) -> list[str]:
        issues = validate_database_integrity(self.db_path)
        if self.current_record_id is None:
            return issues

        try:
            db_record = get_record_readonly(self.current_record_id, self.db_path)
        except (FileNotFoundError, sqlite3.Error) as exc:
            issues.append(
                f"当前详情记录 {self.current_record_id} 无法通过只读方式读取：{exc}"
            )
            return issues
        if db_record is None:
            issues.append(f"当前详情记录 {self.current_record_id} 已不在数据库中")
            return issues

        db_snapshot = self.snapshot_from_record(db_record)
        if self.form_baseline != db_snapshot:
            issues.append(
                f"当前详情记录 {self.current_record_id} 与数据库最新值不一致，"
                "可能被外部工具修改"
            )
        return issues

    def import_from_builtin_sample(self) -> None:
        if not self.confirm_discard_unsaved_changes("导入内置样例并刷新列表"):
            self.set_status("已取消导入，未保存内容仍保留在表单中。")
            return
        try:
            result = import_prompt_source(db_path=self.db_path)
        except Exception as exc:  # noqa: BLE001 - GUI should show import errors.
            messagebox.showerror("导入失败", str(exc))
            return
        imported = len(result["imported"])
        skipped = len(result["skipped"])
        if not self.refresh_records(preserve_selection=False):
            return
        message = f"导入完成：新增 {imported} 条，跳过 {skipped} 条。"
        self.set_status(message)
        messagebox.showinfo("导入完成", message)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Launch prompt template manager GUI.")
    parser.add_argument("--db", default=None, help="SQLite database path.")
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Initialize the GUI and exit without opening the event loop.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = tk.Tk()
    if args.smoke:
        root.withdraw()
    try:
        PromptManagerApp(root, db_path=args.db)
    except RuntimeError as exc:
        if not args.smoke:
            messagebox.showerror("数据库初始化失败", str(exc))
        root.destroy()
        print(f"GUI startup failed: {exc}", file=sys.stderr)
        return 1
    if args.smoke:
        root.destroy()
        print("GUI smoke check passed.")
        return 0
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
