"""
Contains action handlers like:
- goto
- click
- fill
- wait_for
- screenshot
- download
- notify

Each handler receives a Playwright Page and the step dict.
"""

from __future__ import annotations

from typing import Any

from playwright.sync_api import Page


# ── Action handlers ─────────────────────────────────────────────────
# Each function takes (page, step) and performs ONE browser action.
# Fill in the Playwright calls yourself — the Page API docs are your
# best friend:  https://playwright.dev/python/docs/api/class-page


def do_goto(page: Page, step: dict[str, Any]) -> None:
    """Navigate to step['url']."""
    url = step["url"]
    # TODO: use page.goto(...)
    raise NotImplementedError("Implement do_goto with page.goto()")


def do_click(page: Page, step: dict[str, Any]) -> None:
    """Click the element matching step['selector']."""
    selector = step["selector"]
    # TODO: use page.click(...) or page.locator(...).click()
    raise NotImplementedError("Implement do_click")


def do_fill(page: Page, step: dict[str, Any]) -> None:
    """Type step['value'] into the element matching step['selector']."""
    selector = step["selector"]
    value = step["value"]  # already resolved by workflow.resolve_env_values()
    # TODO: use page.fill(...)
    raise NotImplementedError("Implement do_fill")


def do_wait_for(page: Page, step: dict[str, Any]) -> None:
    """Wait until step['selector'] appears on the page."""
    selector = step["selector"]
    timeout = step.get("timeout_ms")  # optional override
    # TODO: use page.wait_for_selector(...) or page.locator(...).wait_for(...)
    raise NotImplementedError("Implement do_wait_for")


def do_screenshot(page: Page, step: dict[str, Any]) -> None:
    """Save a screenshot to step['path']."""
    path = step["path"]
    # TODO: use page.screenshot(path=...)
    raise NotImplementedError("Implement do_screenshot")


def do_download(page: Page, step: dict[str, Any]) -> None:
    """Handle a download triggered by clicking step['selector']."""
    selector = step.get("selector", "")
    save_as = step.get("path", "downloads/file")
    # TODO: This one's trickier — look into page.expect_download()
    #       with page.expect_download() as download_info:
    #           page.click(selector)
    #       download = download_info.value
    #       download.save_as(save_as)
    raise NotImplementedError("Implement do_download")


def do_select(page: Page, step: dict[str, Any]) -> None:
    """Select an option from a native <select> element by value."""
    selector = step["selector"]
    value = step["value"]
    # TODO: use page.select_option(...)
    raise NotImplementedError("Implement do_select with page.select_option()")


def do_notify(page: Page, step: dict[str, Any]) -> None:
    """Print a message (no Playwright needed here)."""
    message = step["message"]
    print(f"[notify] {message}")


# ── Dispatch table ──────────────────────────────────────────────────
# Maps action name → handler function.  The runner uses this.

ACTION_DISPATCH: dict[str, Any] = {
    "goto":       do_goto,
    "click":      do_click,
    "fill":       do_fill,
    "wait_for":   do_wait_for,
    "screenshot": do_screenshot,
    "download":   do_download,
    "select":     do_select,
    "notify":     do_notify,
}