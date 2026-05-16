"""
Loops through the workflow steps and executes them.

This is the bridge between workflow.py (data) and actions.py (browser calls).
"""

from __future__ import annotations

import logging
from typing import Any

from playwright.sync_api import Browser, Page, sync_playwright

from app.actions import ACTION_DISPATCH
from app.workflow import resolve_env_values

log = logging.getLogger(__name__)


def run_workflow(data: dict[str, Any], head: bool = False, pause: bool = False) -> None:
    """
    Execute all steps of a parsed workflow dict.

    Handles browser lifecycle (launch → new page → close) and iterates
    through each step, dispatching to the matching action handler.
    """
    name = data.get("name", "unnamed")
    browser_opts = data.get("browser", {})

    # If --head is passed (head=True), override YAML config and run with a head (headless=False)
    yaml_headless = browser_opts.get("headless", True)
    actual_headless = False if head else yaml_headless

    timeout_ms = browser_opts.get("timeout_ms", 30_000)

    steps = resolve_env_values(data["steps"])

    log.info(
        "Running workflow: %s (%d steps, headless=%s)",
        name,
        len(steps),
        actual_headless,
    )

    # ── Launch browser ──────────────────────────────────────────
    with sync_playwright() as pw:
        browser: Browser = pw.chromium.launch(headless=actual_headless)
        page: Page = browser.new_page()
        page.set_default_timeout(timeout_ms)

        try:
            for i, step in enumerate(steps, start=1):
                action = step["action"]
                handler = ACTION_DISPATCH.get(action)
                if handler is None:
                    log.warning("Step %d: unknown action '%s', skipping", i, action)
                    continue

                log.info("Step %d: %s", i, action)
                handler(page, step)

                if pause:
                    page.pause()

        except Exception:
            # Save a failure screenshot so you can see what went wrong
            page.screenshot(path=f"screenshots/error_{name}.png")
            log.exception("Workflow '%s' failed at step %d", name, i)
            raise

        finally:
            browser.close()

    log.info("Workflow '%s' completed successfully", name)
