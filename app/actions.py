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


def do_goto(page: Page, step: dict[str, Any], timeout: int = 10000) -> None:
    """Navigate to step['url']."""
    url = step["url"]
    page.goto(url, wait_until="domcontentloaded", timeout=timeout)


def do_click(page: Page, step: dict[str, Any]) -> None:
    """Click the element matching step['selector']."""
    selector = step["selector"]
    locator = page.locator(selector)
    locator.click()


def do_fill(page: Page, step: dict[str, Any]) -> None:
    """Type step['value'] into the element matching step['selector']."""
    selector = step["selector"]
    value = step["value"]  # already resolved by workflow.resolve_env_values()
    page.fill(selector, value)


def do_wait_for(page: Page, step: dict[str, Any]) -> None:
    """Wait until step['selector'] appears on the page."""
    selector = step["selector"]
    timeout = step.get("timeout_ms")  # optional override
    page.wait_for_selector(selector, timeout=timeout)


def do_screenshot(page: Page, step: dict[str, Any]) -> None:
    """Save a screenshot to step['path']."""
    path = step["path"]
    page.screenshot(path=path)


def do_download(page: Page, step: dict[str, Any]) -> None:
    """Handle a download triggered by clicking step['selector']."""
    selector = step.get("selector", "")
    save_as = step.get("path", "downloads/file")
    with page.expect_download() as download_info:
        page.click(selector)
    download = download_info.value
    download.save_as(save_as)


def do_select(page: Page, step: dict[str, Any]) -> None:
    """Select an option from a native <select> element by value."""
    selector = step["selector"]
    value = step["value"]
    page.select_option(selector, value)


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