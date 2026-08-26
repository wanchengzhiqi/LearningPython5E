import dis


def call_site():
    resolve_builder()(
        evaluate("key", "menu.quit"),
        locale=fail_locale(),
        options=evaluate("options", shared_options),
    )


dis.dis(call_site)
