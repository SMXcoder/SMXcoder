"""One command: banner + info card + heatmap + README.   Usage: python scripts/build_all.py [--sample]"""
import sys, subprocess
py = sys.executable
run = lambda *a: subprocess.run([py, *a], check=True)
run("scripts/make_banner_svg.py")
run("scripts/make_info_card.py")
run("scripts/fetch_contributions.py", *(["--sample"] if "--sample" in sys.argv else []))
run("scripts/render_heatmap_svg.py")
run("scripts/build_readme.py")
