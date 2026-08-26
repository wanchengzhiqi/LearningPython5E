import dis


def call_site():
    target(
        *positional_source(),
        dry_run=explicit_flag(),
        **mapping_source(),
    )


dis.dis(call_site)
