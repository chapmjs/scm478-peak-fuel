"""
SCM 478 - Unit 1 Checks: Peak Fuel Dashboard (Weeks 1-4)

Current sections:
  - Week 1 In-Class: Ingredient Catalog Viewer
  - Week 1 Homework: Supplier Lookup

Future sections (will be added as released):
  - Week 2 In-Class: Sales & Demand Viewer
  - Week 2 Homework: Inventory Alerts
  - Week 3 In-Class: Monday Morning Dashboard
  - Week 3 Homework: Supplier Performance
"""

import pandas as pd
import os


def _find_file(candidates):
    """Return the first matching filename, or None."""
    for fname in candidates:
        if os.path.exists(fname):
            return fname
    return None


def _read_app_code():
    """Read the main app file and return its contents."""
    for fname in ["app.py", "main.py", "streamlit_app.py"]:
        if os.path.exists(fname):
            with open(fname, "r", encoding="utf-8", errors="replace") as f:
                return f.read()
    return None


# ==================================================================
# SECTION: Week 1 In-Class Exercise
# ==================================================================
def _check_week1_inclass():
    checks = []

    # --- Products & Pricing file ---
    products_file = _find_file([
        "Products___Pricing.csv", "Products_Pricing.csv",
        "products_pricing.csv", "Products & Pricing.csv",
    ])
    products_df = None

    if products_file:
        try:
            products_df = pd.read_csv(products_file)
            if len(products_df) >= 5:
                checks.append((
                    "Products & Pricing file loads",
                    True,
                    "Found %s with %d products." % (products_file, len(products_df)),
                    5,
                ))
            else:
                checks.append((
                    "Products & Pricing file loads",
                    False,
                    "Found file but only %d rows - expected 5." % len(products_df),
                    5,
                ))
        except Exception as e:
            checks.append((
                "Products & Pricing file loads",
                False,
                "File found but error loading: %s" % str(e)[:80],
                5,
            ))
    else:
        checks.append((
            "Products & Pricing file loads",
            False,
            "File not found. Upload Products___Pricing.csv to your repo.",
            5,
        ))

    # --- Products required columns ---
    req_prod = ["SKU", "Product Name", "Retail Price"]
    if products_df is not None:
        missing = [c for c in req_prod if c not in products_df.columns]
        if not missing:
            checks.append((
                "Products file has required columns",
                True,
                "Columns present: %s." % ", ".join(req_prod),
                5,
            ))
        else:
            checks.append((
                "Products file has required columns",
                False,
                "Missing: %s." % ", ".join(missing),
                5,
            ))
    else:
        checks.append((
            "Products file has required columns",
            False,
            "Cannot check - file not loaded.",
            5,
        ))

    # --- Ingredient Catalog file ---
    ingredient_file = _find_file([
        "Ingredient_Catalog.csv", "ingredient_catalog.csv",
        "Ingredient Catalog.csv",
    ])
    ingredient_df = None

    if ingredient_file:
        try:
            ingredient_df = pd.read_csv(ingredient_file)
            if len(ingredient_df) >= 30:
                checks.append((
                    "Ingredient Catalog file loads",
                    True,
                    "Found %s with %d ingredients." % (ingredient_file, len(ingredient_df)),
                    5,
                ))
            else:
                checks.append((
                    "Ingredient Catalog file loads",
                    False,
                    "Only %d rows - expected at least 30." % len(ingredient_df),
                    5,
                ))
        except Exception as e:
            checks.append((
                "Ingredient Catalog file loads",
                False,
                "Error loading: %s" % str(e)[:80],
                5,
            ))
    else:
        checks.append((
            "Ingredient Catalog file loads",
            False,
            "File not found. Upload Ingredient_Catalog.csv.",
            5,
        ))

    # --- Ingredient required columns ---
    req_ing = [
        "Ingredient SKU", "Description", "Order Unit",
        "Cost Per Unit", "MOQ", "Primary Supplier ID",
        "Primary Supplier Name",
    ]
    if ingredient_df is not None:
        missing = [c for c in req_ing if c not in ingredient_df.columns]
        if not missing:
            checks.append((
                "Ingredient Catalog has required columns",
                True,
                "All %d columns present." % len(req_ing),
                5,
            ))
        else:
            checks.append((
                "Ingredient Catalog has required columns",
                False,
                "Missing: %s." % ", ".join(missing),
                5,
            ))
    else:
        checks.append((
            "Ingredient Catalog has required columns",
            False,
            "Cannot check - file not loaded.",
            5,
        ))

    # --- Cost data numeric and valid ---
    if ingredient_df is not None and "Cost Per Unit" in ingredient_df.columns:
        costs = pd.to_numeric(ingredient_df["Cost Per Unit"], errors="coerce")
        valid = costs.dropna()
        if len(valid) == len(ingredient_df) and valid.min() > 0:
            checks.append((
                "Cost data is numeric and valid",
                True,
                "Range: $%.2f - $%.2f." % (valid.min(), valid.max()),
                5,
            ))
        else:
            checks.append((
                "Cost data is numeric and valid",
                False,
                "%d rows have missing or non-numeric costs." % (len(ingredient_df) - len(valid)),
                5,
            ))
    else:
        checks.append((
            "Cost data is numeric and valid",
            False,
            "Cannot check - missing Cost Per Unit column.",
            5,
        ))

    # --- Supplier names available for filtering ---
    if ingredient_df is not None and "Primary Supplier Name" in ingredient_df.columns:
        n = ingredient_df["Primary Supplier Name"].dropna().nunique()
        if n >= 5:
            checks.append((
                "Supplier data available for filtering",
                True,
                "%d unique suppliers in catalog." % n,
                5,
            ))
        else:
            checks.append((
                "Supplier data available for filtering",
                False,
                "Only %d suppliers - expected at least 5." % n,
                5,
            ))
    else:
        checks.append((
            "Supplier data available for filtering",
            False,
            "No Primary Supplier Name column found.",
            5,
        ))

    # --- App has sidebar navigation ---
    app_code = _read_app_code()
    if app_code:
        has_sidebar = "sidebar" in app_code.lower()
        has_nav = any(
            kw in app_code.lower()
            for kw in ["radio", "selectbox", "page", "navigation"]
        )
        if has_sidebar and has_nav:
            checks.append((
                "App has sidebar navigation",
                True,
                "Sidebar navigation detected in app code.",
                5,
            ))
        elif has_sidebar:
            checks.append((
                "App has sidebar navigation",
                True,
                "Sidebar detected (navigation method may vary).",
                5,
            ))
        else:
            checks.append((
                "App has sidebar navigation",
                False,
                "No sidebar navigation found. Use st.sidebar.radio() or similar.",
                5,
            ))
    else:
        checks.append((
            "App has sidebar navigation",
            False,
            "No app.py found.",
            5,
        ))

    # --- App displays data ---
    if app_code:
        has_display = any(
            kw in app_code.lower()
            for kw in ["dataframe", "table", "plotly", "write("]
        )
        if has_display:
            checks.append((
                "App displays data (table or chart)",
                True,
                "Data display component found in app code.",
                5,
            ))
        else:
            checks.append((
                "App displays data (table or chart)",
                False,
                "No st.dataframe(), st.table(), or chart found.",
                5,
            ))
    else:
        checks.append((
            "App displays data (table or chart)",
            False,
            "No app.py found.",
            5,
        ))

    return checks, ingredient_df, products_df


# ==================================================================
# SECTION: Week 1 Homework - Supplier Lookup
# ==================================================================
def _check_week1_homework(ingredient_df, products_df):
    checks = []

    # --- Vendor Contacts file ---
    vendor_file = _find_file([
        "Vendor_Contacts___Terms.csv", "Vendor_Contacts_Terms.csv",
        "vendor_contacts_terms.csv", "Vendor Contacts & Terms.csv",
    ])
    vendor_df = None

    if vendor_file:
        try:
            vendor_df = pd.read_csv(vendor_file)
            if len(vendor_df) >= 20:
                checks.append((
                    "Vendor Contacts file loads",
                    True,
                    "Found %s with %d suppliers." % (vendor_file, len(vendor_df)),
                    5,
                ))
            else:
                checks.append((
                    "Vendor Contacts file loads",
                    False,
                    "Only %d rows - expected at least 20." % len(vendor_df),
                    5,
                ))
        except Exception as e:
            checks.append((
                "Vendor Contacts file loads",
                False,
                "Error loading: %s" % str(e)[:80],
                5,
            ))
    else:
        checks.append((
            "Vendor Contacts file loads",
            False,
            "File not found. Upload Vendor_Contacts___Terms.csv.",
            5,
        ))

    # --- Vendor required columns ---
    req_vendor = [
        "Supplier ID", "Company Name",
        "Lead Time (weeks)", "Payment Terms",
    ]
    if vendor_df is not None:
        missing = [c for c in req_vendor if c not in vendor_df.columns]
        if not missing:
            checks.append((
                "Vendor file has required columns",
                True,
                "Key columns present.",
                5,
            ))
        else:
            checks.append((
                "Vendor file has required columns",
                False,
                "Missing: %s." % ", ".join(missing),
                5,
            ))
    else:
        checks.append((
            "Vendor file has required columns",
            False,
            "Cannot check - file not loaded.",
            5,
        ))

    # --- Shared key links correctly ---
    if ingredient_df is not None and vendor_df is not None:
        ing_col = "Primary Supplier ID"
        ven_col = "Supplier ID"
        if ing_col in ingredient_df.columns and ven_col in vendor_df.columns:
            ing_ids = set(ingredient_df[ing_col].dropna().unique())
            ven_ids = set(vendor_df[ven_col].dropna().unique())
            matched = ing_ids.intersection(ven_ids)
            unmatched = ing_ids - ven_ids
            if matched and not unmatched:
                checks.append((
                    "Supplier ID shared key links correctly",
                    True,
                    "All %d catalog suppliers found in vendor file." % len(ing_ids),
                    10,
                ))
            elif matched:
                extras = ", ".join(list(unmatched)[:3])
                checks.append((
                    "Supplier ID shared key links correctly",
                    True,
                    "%d matched, %d unmatched: %s." % (len(matched), len(unmatched), extras),
                    10,
                ))
            else:
                checks.append((
                    "Supplier ID shared key links correctly",
                    False,
                    "No IDs match. Check that both files use same format (e.g., SUP-108).",
                    10,
                ))
        else:
            checks.append((
                "Supplier ID shared key links correctly",
                False,
                "Missing '%s' in catalog or '%s' in vendor file." % (ing_col, ven_col),
                10,
            ))
    else:
        checks.append((
            "Supplier ID shared key links correctly",
            False,
            "Cannot check - one or both files not loaded.",
            10,
        ))

    # --- Lead time data valid ---
    if vendor_df is not None and "Lead Time (weeks)" in vendor_df.columns:
        lt = pd.to_numeric(vendor_df["Lead Time (weeks)"], errors="coerce")
        valid = lt.dropna()
        if len(valid) == len(vendor_df) and valid.min() >= 1:
            checks.append((
                "Lead time data is valid",
                True,
                "Range: %d-%d weeks." % (int(valid.min()), int(valid.max())),
                5,
            ))
        else:
            checks.append((
                "Lead time data is valid",
                False,
                "Some lead times are missing or invalid.",
                5,
            ))
    else:
        checks.append((
            "Lead time data is valid",
            False,
            "Cannot check - missing column.",
            5,
        ))

    # --- App references supplier/vendor data ---
    app_code = _read_app_code()
    if app_code:
        has_ref = any(
            kw in app_code.lower()
            for kw in ["vendor", "supplier", "lead time", "lead_time", "payment terms"]
        )
        if has_ref:
            checks.append((
                "App references supplier data",
                True,
                "Supplier/vendor references found in app code.",
                5,
            ))
        else:
            checks.append((
                "App references supplier data",
                False,
                "No vendor/supplier references in app.py. Load and display vendor contact info.",
                5,
            ))
    else:
        checks.append((
            "App references supplier data",
            False,
            "No app.py found.",
            5,
        ))

    # --- App has metric display ---
    if app_code:
        if "metric" in app_code.lower():
            checks.append((
                "App displays summary metric(s)",
                True,
                "st.metric() or metric display found.",
                5,
            ))
        else:
            checks.append((
                "App displays summary metric(s)",
                False,
                "No st.metric() found. Add total minimum reorder cost (sum of Cost x MOQ).",
                5,
            ))
    else:
        checks.append((
            "App displays summary metric(s)",
            False,
            "No app.py found.",
            5,
        ))

    # --- Reorder cost calculation ---
    if ingredient_df is not None:
        cost_col = "Cost Per Unit"
        moq_col = "MOQ"
        if cost_col in ingredient_df.columns and moq_col in ingredient_df.columns:
            costs = pd.to_numeric(ingredient_df[cost_col], errors="coerce")
            moqs = pd.to_numeric(ingredient_df[moq_col], errors="coerce")
            total = (costs * moqs).sum()
            if total > 0:
                checks.append((
                    "Reorder cost calculation is feasible",
                    True,
                    "Expected total minimum reorder cost: $%s. Verify your app shows this." % format(total, ",.2f"),
                    5,
                ))
            else:
                checks.append((
                    "Reorder cost calculation is feasible",
                    False,
                    "Calculates to $0 - check that Cost and MOQ are numeric.",
                    5,
                ))
        else:
            checks.append((
                "Reorder cost calculation is feasible",
                False,
                "Missing Cost Per Unit or MOQ columns.",
                5,
            ))
    else:
        checks.append((
            "Reorder cost calculation is feasible",
            False,
            "Cannot calculate - Ingredient Catalog not loaded.",
            5,
        ))

    # --- All three files loaded ---
    files_loaded = sum(1 for df in [products_df, ingredient_df, vendor_df] if df is not None)
    if files_loaded == 3:
        checks.append((
            "All three data files loaded",
            True,
            "Products (%d), Ingredients (%d), Vendors (%d)." % (
                len(products_df), len(ingredient_df), len(vendor_df)),
            5,
        ))
    else:
        missing = []
        if products_df is None:
            missing.append("Products & Pricing")
        if ingredient_df is None:
            missing.append("Ingredient Catalog")
        if vendor_df is None:
            missing.append("Vendor Contacts")
        checks.append((
            "All three data files loaded",
            False,
            "Missing: %s." % ", ".join(missing),
            5,
        ))

    return checks


# ==================================================================
# PUBLIC INTERFACE
# ==================================================================
def run_checks():
    """
    Return a list of (section_name, checks) tuples.
    Each checks list contains (name, passed, detail, points) tuples.
    """
    inclass_checks, ingredient_df, products_df = _check_week1_inclass()
    hw_checks = _check_week1_homework(ingredient_df, products_df)

    return [
        ("Week 1 In-Class: Ingredient Catalog Viewer", inclass_checks),
        ("Week 1 Homework: Supplier Lookup", hw_checks),
    ]
