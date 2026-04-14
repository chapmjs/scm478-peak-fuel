"""
SCM 478 — Self-Check Module
Peak Fuel Foods Supply Chain System

Add this file and the checks/ folder to your GitHub repo.
Then add "Self-Check" to your app's sidebar navigation.

This module checks whether your app meets the requirements
for each unit's assignments. New check files are released
each unit — add them to the checks/ folder as they're assigned.

Your score on Self-Check is what you'll be graded on.
Fix issues until you reach 100%, then submit your URL.


Add this file and the checks/ folder to your GitHub repo.
Then add Self-Check to your app sidebar navigation.
"""

import streamlit as st


def run_self_check():
    """Main self-check page. Call this from your app."""

    st.title("Self-Check: Peak Fuel Foods")
    st.caption(
        "Run these checks as you build. Fix one issue at a time, "
        "commit, wait for redeploy, and check again. Your goal is 100%."
    )

    # Discover which unit check modules are available
    available_units = []
    unit_modules = [
        ("Unit 1 - Peak Fuel Dashboard (Weeks 1-4)", "checks.unit1_checks"),
        ("Unit 2 - Forecasting Module (Weeks 5-7)", "checks.unit2_checks"),
        ("Unit 3 - Planning + Inventory (Weeks 8-10)", "checks.unit3_checks"),
        ("Unit 4 - MRP / Purchasing (Weeks 11-12)", "checks.unit4_checks"),
    ]

    for label, module_path in unit_modules:
        try:
            mod = __import__(module_path, fromlist=["run_checks"])
            if hasattr(mod, "run_checks"):
                available_units.append((label, mod))
        except (ImportError, ModuleNotFoundError):
            pass
        except Exception:
            pass

    if not available_units:
        st.error(
            "No check modules found. Make sure the checks/ folder "
            "is in your repo with __init__.py and unit1_checks.py."
        )
        st.info(
            "Your repo should have:\n"
            "- checks/__init__.py\n"
            "- checks/unit1_checks.py"
        )
        return

    # Run each available unit's checks
    grand_passed = 0
    grand_total = 0

    for label, mod in available_units:
        st.divider()
        st.header(label)

        try:
            sections = mod.run_checks()
        except Exception as e:
            st.error(f"Error running checks: {e}")
            continue

        for section_name, checks in sections:
            st.subheader(section_name)

            section_earned = 0
            section_possible = 0

            for name, passed, detail, points in checks:
                section_possible += points
                if passed:
                    section_earned += points
                    st.markdown(
                        f"**PASS** - **{name}** ({points} pts)  \n{detail}"
                    )
                else:
                    st.markdown(
                        f"**FAIL** - **{name}** ({points} pts)  \n{detail}"
                    )

            pct = (
                int(section_earned / section_possible * 100)
                if section_possible > 0
                else 0
            )

            if pct == 100:
                st.success(
                    f"{section_name}: {pct}% - All checks passed!"
                )
            elif pct >= 75:
                st.warning(
                    f"{section_name}: {pct}% - "
                    f"{section_possible - section_earned} point(s) remaining."
                )
            else:
                st.error(
                    f"{section_name}: {pct}% - "
                    f"{section_possible - section_earned} point(s) remaining."
                )

            grand_passed += section_earned
            grand_total += section_possible

    # Overall summary
    st.divider()
    st.header("Overall Summary")

    overall_pct = (
        int(grand_passed / grand_total * 100) if grand_total > 0 else 0
    )
    st.metric("Total Score", f"{overall_pct}%", f"{grand_passed}/{grand_total} pts")

    if overall_pct == 100:
        st.balloons()
        st.success(
            "All checks passed! Your app is ready to submit. "
            "Copy your Streamlit URL and submit it on Canvas."
        )

    st.divider()
    st.caption(
        "This checker validates data files and app structure. "
        "It cannot verify that filters, charts, and metrics display "
        "correctly - verify those yourself by clicking through your app."
    )
