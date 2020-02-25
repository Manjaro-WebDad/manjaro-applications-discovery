from flask import render_template
import pamac
get = pamac.Get()


def get_categories():
    return {'title': 'Featured', 'href': '/'},\
           {'title': 'Applications', 'href': 'applications'},\
           {'title': 'Packages', 'href': 'packages'},\
           {'title': 'Snaps', 'href': 'snaps'}, \
           {'title': 'Flatpaks', 'href': 'flatpaks'}        


def get_appstream_app_list(category):
    return get.appstream_category(category)


def appstream_template(category):
    template = "featured.html"
    apps = get_appstream_app_list(category)
    return render_template(template, apps=apps, nav=get_categories(), title=category)


def pkgs_template(title):
    
    if title == "Applications":
        template = "applications.html"
    else:
        template = "packages.html"

    apps = get.all_repo_pkgs(title)
    return render_template(template, apps=apps, nav=get_categories(), title=title, total=len(apps))


def external_repos_template(title):

    if title == "Snaps":
        template = "snaps.html"
    else:
        template = "flatpaks.html"

    categories = get.external_repos()[0]
    pamac_database = get.external_repos()[1]
    return render_template(template, categories=categories, nav=get_categories(), title=title, database=pamac_database)


def search_package_template(pkg_name, pkg_format):

    pkg = get.search_single_package(pkg_name, pkg_format)
    title = pkg.get_app_name()

    if not title:
        title = pkg.get_name()

    if pkg_format == "Snap":
        template = "single-snap.html"
    elif pkg_format == "Flatpak":
        template = "single-flatpak.html"
    elif pkg_format == "Native":
        template = "single-package.html"

    return render_template(template, nav=get_categories(), pkg=pkg, title=title, pkg_format=pkg_format)

